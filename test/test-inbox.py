import os
from dotenv import load_dotenv

from mcp_server.phantombuster.messages import PhantomCredentials, PhantomAgentInbox



load_dotenv()

PHANTOMBUSTER_API_KEY = os.environ.get("PHANTOMBUSTER_API_KEY")
LINKEDIN_COOKIE_LI = os.environ.get("LINKEDIN_COOKIE_LI")
LINKEDIN_BROWSER_AGENT = os.environ.get("LINKEDIN_BROWSER_AGENT")

credentials = PhantomCredentials(
    phantombuster_key=PHANTOMBUSTER_API_KEY,
    session_cookie=LINKEDIN_COOKIE_LI,
    user_agent=LINKEDIN_BROWSER_AGENT
)

inbox_agent = PhantomAgentInbox(credentials=credentials)
threads, success = inbox_agent.run_and_get_data(inbox_filter="unread")
if threads:
    print(f"[scrap_inbox]:")
    for thread in threads:
        print(f"{thread.last_message_author_name}: {thread.last_message}")