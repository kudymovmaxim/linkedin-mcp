import os
from dotenv import load_dotenv

from mcp_server.phantombuster.activities import PhantomAgentActivities, PhantomCredentials, Activity



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
max_activities = 10
activities_to_scrape = ["Post", "Article"]

sender_agent = PhantomAgentActivities(
    credentials=credentials,
    nb_max_posts=max_activities,
    activities_to_scrape=activities_to_scrape,
    date_after=30
)
activities, success = sender_agent.run_and_get_data(linkedin)
if success:
    count_activities = len(activities)
    print(f"[scrap_activities]: {count_activities}")

