import json
from typing import List, Optional
from mcp_server.phantombuster.base import PhantomAgentBase, PhantomCredentials
from mcp_server.phantombuster.models import Connection


class PhantomAgentConnections(PhantomAgentBase):
    def __init__(
            self, 
            credentials: PhantomCredentials, 
            agent_id: Optional[str] = None, 
            max_retries: int = 20, 
            retry_delay: int = 10
        ):
        
        super().__init__(credentials, agent_id, max_retries, retry_delay)
        self.script_id = "12670"
        self.script = "LinkedIn Connections Export.js"
        self.name = "LinkedIn Connections Export (API)"

    def run(self, count_to_scrape: int = 100, sort: str = "Recently added") -> bool:
        """Start phantom task to scrape connections
        Args:
            count_to_scrape: Number of connections to scrape
            sort: Sort order for connections ("Recently added" by default)
        """
        data = {
            "id": self.agent_id,
            "argument": {
                "userAgent": self.credentials.user_agent,
                "sessionCookie": self.credentials.session_cookie,
                "sortBy": sort,
                "numberOfProfiles": count_to_scrape
            }
        }
        return self._post(self.lanch_url, data)

    def get_data(self) -> List[Connection]:
        """Get processed connections from phantom task"""
        connections = []
        raw_data = self.get_raw_data()
        if not raw_data:
            return connections 
        
        result_obj = json.loads(raw_data.get("resultObject"))
        if not result_obj:
            return connections 
        
        for value in result_obj:
            connection = Connection(
                linkedin_url=value.get('profileUrl', ""),
                first_name=value.get('firstName', ""),
                last_name=value.get('lastName', ""),
                full_name=value.get('fullName', ""),
                job_title=value.get('title'),
                date_connected=value.get('connectionSince')
            )
            connections.append(connection)
        return connections 