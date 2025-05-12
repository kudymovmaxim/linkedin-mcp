import os
from dotenv import load_dotenv

from mcp_server.phantombuster.profile import PhantomCredentials, PhantomAgentProfile



load_dotenv()

PHANTOMBUSTER_API_KEY = os.environ.get("PHANTOMBUSTER_API_KEY")
LINKEDIN_COOKIE_LI = os.environ.get("LINKEDIN_COOKIE_LI")
LINKEDIN_BROWSER_AGENT = os.environ.get("LINKEDIN_BROWSER_AGENT")

credentials = PhantomCredentials(
    phantombuster_key=PHANTOMBUSTER_API_KEY,
    session_cookie=LINKEDIN_COOKIE_LI,
    user_agent=LINKEDIN_BROWSER_AGENT
)

linkedin = "https://www.linkedin.com/in/maxim-kudymov/"

inbox_agent = PhantomAgentProfile(credentials=credentials)
threads, success = inbox_agent.run_and_get_data(linkedin)
if threads:
    print(f"[scrap_profile]: {threads}")