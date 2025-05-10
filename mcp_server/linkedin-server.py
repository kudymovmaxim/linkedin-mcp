# linkedin-server.py
import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from typing import List, Optional
from mcp_server.phantombuster.profile import PhantomAgentProfile, Profile, PhantomCredentials
from mcp_server.phantombuster.company import PhantomAgentCompany, Company
from mcp_server.phantombuster.messages import PhantomAgentInbox, PhantomAgentThread, Thread, Message


load_dotenv()

PHANTOMBUSTER_API_KEY = os.environ.get("PHANTOMBUSTER_API_KEY")
LINKEDIN_COOKIE_LI = os.environ.get("LINKEDIN_COOKIE_LI")
LINKEDIN_BROWSER_AGENT = os.environ.get("LINKEDIN_BROWSER_AGENT")

# Initialize the MCP server with a friendly name
mcp = FastMCP("Linkedin server")

@mcp.tool()
def scrap_profile(linkedin: str) -> Optional[Profile]:
    """Scrapes a LinkedIn profile (name, location, experience, etc). Takes a profile link as input."""

    credentials = PhantomCredentials(
        phantombuster_key=PHANTOMBUSTER_API_KEY,
        session_cookie=LINKEDIN_COOKIE_LI,
        user_agent=LINKEDIN_BROWSER_AGENT
    )
    profile_agent = PhantomAgentProfile(credentials=credentials)
    profile, success = profile_agent.run_and_get_data(linkedin)
    if success:
        return profile
    
    return None

@mcp.tool()
def scrap_company(linkedin: str) -> Optional[Company]:
    """Scrapes a LinkedIn company page (name, industry, size, etc). Takes a company link as input."""

    credentials = PhantomCredentials(
        phantombuster_key=PHANTOMBUSTER_API_KEY,
        session_cookie=LINKEDIN_COOKIE_LI,
        user_agent=LINKEDIN_BROWSER_AGENT
    )
    company_agent = PhantomAgentCompany(credentials=credentials)
    company, success = company_agent.run_and_get_data(linkedin)
    if success:
        return company
    
    return None


@mcp.tool()
def scrap_inbox(count_to_scrape: int = 10, inbox_filter: str = "all") -> List[Thread]:
    """Scrapes LinkedIn inbox threads. Parameters:
    - count_to_scrape: number of threads to fetch (default 10)
    - inbox_filter: filter for threads ('all', 'archived', 'myconnections', 'unread', 'inmail', 'spam')
    Returns a list of threads.
    """

    credentials = PhantomCredentials(
        phantombuster_key=PHANTOMBUSTER_API_KEY,
        session_cookie=LINKEDIN_COOKIE_LI,
        user_agent=LINKEDIN_BROWSER_AGENT
    )

    inbox_agent = PhantomAgentInbox(credentials=credentials)
    threads, success = inbox_agent.run_and_get_data(count_to_scrape, inbox_filter)
    if success:
        return threads
    
    return None


@mcp.tool()
def scrap_thread(thread_link: str) -> List[Message]:
    """Scrapes all messages from a LinkedIn thread. Takes a thread link as input. Returns a list of messages."""

    credentials = PhantomCredentials(
        phantombuster_key=PHANTOMBUSTER_API_KEY,
        session_cookie=LINKEDIN_COOKIE_LI,
        user_agent=LINKEDIN_BROWSER_AGENT
    )

    thread_agent = PhantomAgentThread(credentials=credentials)
    messages, success = thread_agent.run_and_get_data(thread_link)
    if success:
        return messages
    
    return None

# Run the MCP server locally
if __name__ == '__main__':
    mcp.run()