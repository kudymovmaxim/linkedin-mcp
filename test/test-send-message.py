import os
from dotenv import load_dotenv

from mcp_server.phantombuster.messages import PhantomCredentials, PhantomAgentMessageSender



load_dotenv()

PHANTOMBUSTER_API_KEY = os.environ.get("PHANTOMBUSTER_API_KEY")
LINKEDIN_COOKIE_LI = os.environ.get("LINKEDIN_COOKIE_LI")
LINKEDIN_BROWSER_AGENT = os.environ.get("LINKEDIN_BROWSER_AGENT")

credentials = PhantomCredentials(
    phantombuster_key=PHANTOMBUSTER_API_KEY,
    session_cookie=LINKEDIN_COOKIE_LI,
    user_agent=LINKEDIN_BROWSER_AGENT
)

linkedin = "<linkedin>"
message = "HI, Max"

sender_agent = PhantomAgentMessageSender(credentials=credentials)
status, success = sender_agent.run_and_get_data(linkedin, message)
if success:
    print(f"[send_message]: {status}")

