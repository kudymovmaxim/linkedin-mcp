from typing import List, Optional, Tuple
from mcp_server.phantombuster.base import PhantomAgentBase, PhantomCredentials
from mcp_server.phantombuster.models import Thread, Message

class PhantomAgentInbox(PhantomAgentBase):
    def __init__(
            self, 
            credentials: PhantomCredentials, 
            agent_id: Optional[str] = None, 
            max_retries: int = 20, 
            retry_delay: int = 10
        ):

        super().__init__(credentials, agent_id, max_retries, retry_delay)
        self.script_id = "532696507966746"
        self.script = "LinkedIn Inbox Scraper.js"
        self.name = "LinkedIn Inbox Scraper (API)"

    def run(self, count_to_scrape=100, inbox_filter="all") -> bool:
        """Start phantom task to scrape inbox"""
        data = {
            "id": self.agent_id,
            "argument": {
                "userAgent": self.credentials.user_agent,
                "sessionCookie": self.credentials.session_cookie,
                "inboxFilter": inbox_filter,
                "numberOfThreadsToScrape": count_to_scrape
            }
        }
        
        return self._post(self.lanch_url, data)

    def get_data(self) -> List[Thread]:
        """Get processed threads from phantom task"""
        result = self.get_raw_data().get("resultObject")
        # result = THREADS_TEST
        threads = []
        if result:
            for value in result:
                thread_link = value.get('threadUrl')
                linkedInUrls = value.get('linkedInUrls', [])
                if thread_link and linkedInUrls:
                    first_name_from = value.get('firstnameFrom', "")
                    last_name_from = value.get('lastnameFrom', "")
                    thread = Thread(
                        thread_id=thread_link,
                        participants=[value.get('firstnameFrom', "") + " " + value.get('lastnameFrom', "")],
                        last_message=value.get('message', ""),
                        last_message_date=value.get('lastMessageDate'),
                        timestamp=value.get('timestamp'),
                        is_last_message_from_me=value.get('isLastMessageFromMe'),
                        last_message_author_name=f"{first_name_from} {last_name_from}",
                        read_status=value.get('readStatus'),
                        linkedin_url=linkedInUrls[0]
                    )
                    threads.append(thread)
        return threads
    
    
class PhantomAgentThread(PhantomAgentBase):
    def __init__(
            self, 
            credentials: PhantomCredentials, 
            agent_id: Optional[str] = None, 
            max_retries: int = 20, 
            retry_delay: int = 10
        ):
        
        super().__init__(credentials, agent_id, max_retries, retry_delay)
        self.script_id = "9387"
        self.script = "LinkedIn Message Thread Scraper.js"
        self.name = "LinkedIn Message Thread Scraper (API)"



    def run(self, thread_link: str) -> bool:
        """Start phantom task to scrape messages from a thread"""
        data = {
            "id": self.agent_id,
            "argument": {
                "userAgent": self.credentials.user_agent,
                "sessionCookie": self.credentials.session_cookie,
                "spreadsheetUrl": thread_link
            }
        }
        return self._post(self.lanch_url, data)



    def get_data(self) -> List[Message]:
        """Get processed messages from phantom task"""
        result = self.get_raw_data().get("resultObject")
        # result = MESSAGES_TEST
        messages = []
        seen = set()
        if result:
            for value in result:
                thread_messages = value.get("messages", [])
                for msg in thread_messages:
                    key = (msg.get('date'), msg.get('author'), msg.get('message'))
                    if key in seen:
                        continue
                    seen.add(key)
                    message = Message(
                        date=msg.get('date'),
                        author=msg.get('author'),
                        message=msg.get('message'),
                        connection_degree=msg.get('connectionDegree')
                    )
                    messages.append(message)
        return messages 
    

    
class PhantomAgentMessageSender(PhantomAgentBase):
    def __init__(
            self, 
            credentials: PhantomCredentials, 
            agent_id: Optional[str] = None
        ):
        
        super().__init__(credentials, agent_id)
        self.script_id = "9227"
        self.script = "LinkedIn Message Sender.js"
        self.name = "LinkedIn Message Sender (API)"



    def run(self, linkedin: str, message: str, message_control: str = "none") -> bool:
        """
        message_control:
           - none
           - sendOnlyIfLastWasRecipient
           - dontSendIfLastWasRecipient
           - sendOnlyIfLastWasRecipientOrNoMessage
           - sendOnlyIfLastWasMeOrNoMessage
           - sendOnlyIfNoMessage
           - sendOnlyIfNoReply
        """
        data = {
            "id": self.agent_id,
            "argument": {
                "userAgent": self.credentials.user_agent,
                "sessionCookie": self.credentials.session_cookie,
                "spreadsheetUrl": linkedin,
                "message": str(message),
                "messageControl": message_control
            }
        }

        return self._post(self.lanch_url, data)



    def get_data(self) -> str:
        """Return only status string for message sending task"""
        result = self.raw_data
        if not result:
            result = self.get_raw_data()
        if not result:
            return {"status": None}
        return result.get("status")
