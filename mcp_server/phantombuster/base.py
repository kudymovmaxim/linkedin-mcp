import requests
import json
import time
from typing import Optional, Tuple
from mcp_server.base_model.MarkdownModel import MarkdownModel


class PhantomCredentials(MarkdownModel):
    """Credentials for authentication with Phantom services"""
    user_agent: str
    session_cookie: str
    phantombuster_key: str


class PhantomAgentBase:
    def __init__(
            self, 
            credentials: PhantomCredentials, 
            agent_id: Optional[str] = None, 
            max_retries: int = 20, 
            retry_delay: int = 10
        ):
        self.raw_data = None
        self.credentials = credentials
        self.agent_id = agent_id
        self.container_id = None
        self.lanch_url = "https://api.phantombuster.com/api/v2/agents/launch"
        self._max_retries = max_retries
        self._retry_delay = retry_delay  # seconds
        
        # Required for agent creation
        self.script_id = None  # Must be set by subclasses
        self.script = None     # Must be set by subclasses
        self.name = None       # Must be set by subclasses
        self.argument = None   # Can be set by subclasses or in run method

    def create(self) -> bool:
        """Create a new Phantom agent"""
        if not all([self.script_id, self.script, self.name]):
            raise ValueError("script_id, script and name must be set before creating an agent")
            
        url = "https://api.phantombuster.com/api/v2/agents/save"
        
        new_agent = {
            "scriptId": self.script_id,
            "script": self.script,
            "branch": "master",
            "environment": "release",
            "org": "phantombuster",
            "name": self.name,
            "fileMgmt": "mix",
            "argument": self.argument,
            "launchType": "manually",
            "maxParallelism": 1
        }
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Phantombuster-Key": self.credentials.phantombuster_key
        }
        
        response = requests.post(url, json=new_agent, headers=headers)
        if response.ok:
            response_json = response.json()
            self.agent_id = response_json.get("id")
            return bool(self.agent_id)
        return False

    def delete(self) -> bool:
        """Delete the current Phantom agent"""
        if not self.agent_id:
            return False
            
        url = "https://api.phantombuster.com/api/v2/agents/delete"
        
        payload = {"id": self.agent_id}
        headers = {
            "content-type": "application/json",
            "X-Phantombuster-Key": self.credentials.phantombuster_key
        }
        
        response = requests.post(url, json=payload, headers=headers)
        return response.ok

    def _post(self, url, data, headers=None):
        if headers is None:
            headers = {
                'Content-Type': 'application/json',
                'x-phantombuster-key': self.credentials.phantombuster_key,
            }

        response = requests.post(url, headers=headers, json=data)
        if response:
            response_json = response.json()
            container_id = response_json.get("containerId")
            if container_id:
                self.container_id = container_id
                return True
        return False

    def is_finished(self) -> bool:
        """Check if the phantom task is finished"""
        if not self.agent_id:
            return False
            
        url = f"https://api.phantombuster.com/api/v2/agents/fetch-output?id={self.agent_id}"
        headers = {
            "accept": "application/json",
            "X-Phantombuster-Key": self.credentials.phantombuster_key
        }
        try:
            response = requests.get(url, headers=headers)
            if response not in ["", None]:
                response_json = response.json()
                status = response_json.get("status")
                if status == 'finished':
                    return True
        except:
            return None
        return False

    def wait_until_finished(self) -> bool:
        """Wait until phantom task is finished or max retries reached"""
        for _ in range(self._max_retries):
            if self.is_finished():
                return True
            time.sleep(self._retry_delay)
        return False

    async def wait_until_finished_async(self) -> bool:
        """Async version of wait_until_finished"""
        import asyncio
        for _ in range(self._max_retries):
            if self.is_finished():
                return True
            await asyncio.sleep(self._retry_delay)
        return False

    def get_raw_data(self):
        """Get raw data from phantom container"""
        if not self.container_id:
            return None
            
        url = f"https://api.phantombuster.com/api/v2/containers/fetch?id={self.container_id}&withResultObject=1&withOutput=1"
        headers = {
            "accept": "application/json",
            "X-Phantombuster-Key": self.credentials.phantombuster_key
        }
        response = requests.get(url, headers=headers)
        self.raw_data  = response.json()
        return self.raw_data

    def get_data(self, filter_field: Optional[str] = None, filter_value: Optional[str] = None):
        """Get processed data from phantom task. Should be implemented by subclasses.
        
        Args:
            filter_field: Optional field name to filter results by
            filter_value: Optional value that the field should match
        """
        raise NotImplementedError("Subclasses must implement get_data()")

    def run_and_get_data(self, *args, **kwargs) -> Tuple[Optional[any], bool]:
        """Run complete phantom task lifecycle and get data
        
        This method handles the complete lifecycle:
        1. Creates the agent
        2. Runs the task
        3. Waits for completion and gets data
        4. Deletes the agent
        
        Returns:
            Tuple[data, success]: The processed data and whether all operations succeeded
        """
        success = False
        data = None
        
        try:
            if self.create():
                if self.run(*args, **kwargs):
                    if self.wait_until_finished():
                        data = self.get_data()
                        success = True
        finally:
            # Always try to delete the agent, even if something failed
            if self.agent_id:
                self.delete()
                
        return data, success

    async def run_and_get_data_async(self, *args, **kwargs) -> Tuple[Optional[any], bool]:
        """Async version of run_and_get_data"""
        success = False
        data = None
        
        try:
            if self.create():
                if self.run(*args, **kwargs):
                    if await self.wait_until_finished_async():
                        data = self.get_data()
                        success = True
        finally:
            # Always try to delete the agent, even if something failed
            if self.agent_id:
                self.delete()
                
        return data, success 