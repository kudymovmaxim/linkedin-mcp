# linkedin-server.py
import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import logging

from typing import List, Optional
from mcp_server.phantombuster.profile import PhantomAgentProfile, Profile, PhantomCredentials
from mcp_server.phantombuster.company import PhantomAgentCompany, Company
from mcp_server.phantombuster.messages import PhantomAgentInbox, PhantomAgentThread, PhantomAgentMessageSender, Thread, Message
from mcp_server.phantombuster.activities import PhantomAgentActivities, Activity


load_dotenv()

PHANTOMBUSTER_API_KEY = os.environ.get("PHANTOMBUSTER_API_KEY")
LINKEDIN_COOKIE_LI = os.environ.get("LINKEDIN_COOKIE_LI")
LINKEDIN_BROWSER_AGENT = os.environ.get("LINKEDIN_BROWSER_AGENT")

# Initialize the MCP server with a friendly name
mcp = FastMCP("Linkedin server")

@mcp.tool()
def scrap_profile(linkedin: str) -> Optional[Profile]:
    """
    Scrapes a LinkedIn profile (name, location, experience, etc). Takes a profile link as input.

    Args:
        linkedin: URL of the LinkedIn profile

    Returns:
        Profile object with scraped data, or None if failed
    """

    if not (PHANTOMBUSTER_API_KEY and LINKEDIN_COOKIE_LI and LINKEDIN_BROWSER_AGENT):
        return {"error": True, "message": "PHANTOMBUSTER_API_KEY, LINKEDIN_COOKIE_LI or LINKEDIN_BROWSER_AGENT are not set in environment variables"}

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
    """
    Scrapes a LinkedIn company page (name, industry, size, etc). Takes a company link as input.

    Args:
        linkedin: URL of the LinkedIn company page

    Returns:
        Company object with scraped data, or None if failed
    """

    if not (PHANTOMBUSTER_API_KEY and LINKEDIN_COOKIE_LI and LINKEDIN_BROWSER_AGENT):
        return {"error": True, "message": "PHANTOMBUSTER_API_KEY, LINKEDIN_COOKIE_LI or LINKEDIN_BROWSER_AGENT are not set in environment variables"}

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
    """
    Scrapes LinkedIn inbox threads.

    Args:
        count_to_scrape: Number of threads to fetch (default 10)
        inbox_filter: Filter for threads ('all', 'archived', 'myconnections', 'unread', 'inmail', 'spam')

    Returns:
        List of threads, or None if failed
    """

    if not (PHANTOMBUSTER_API_KEY and LINKEDIN_COOKIE_LI and LINKEDIN_BROWSER_AGENT):
        return {"error": True, "message": "PHANTOMBUSTER_API_KEY, LINKEDIN_COOKIE_LI or LINKEDIN_BROWSER_AGENT are not set in environment variables"}

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
    """
    Scrapes all messages from a LinkedIn thread.

    Args:
        thread_link: URL of the LinkedIn thread

    Returns:
        List of messages, or None if failed
    """

    if not (PHANTOMBUSTER_API_KEY and LINKEDIN_COOKIE_LI and LINKEDIN_BROWSER_AGENT):
        return {"error": True, "message": "PHANTOMBUSTER_API_KEY, LINKEDIN_COOKIE_LI or LINKEDIN_BROWSER_AGENT are not set in environment variables"}

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


@mcp.tool()
def send_message(linkedin: str, message: str, message_control: str = "none") -> bool:
    """
    Sends a message to a LinkedIn thread or user.

    Args:
        linkedin: LinkedIn thread or user link to send the message to.
        message: The message text to send.
        message_control: Controls when the message is sent. Options:
            - none: Always send the message.
            - sendOnlyIfLastWasRecipient: Send only if the last message was from the recipient.
            - dontSendIfLastWasRecipient: Don't send if the last message was from the recipient.
            - sendOnlyIfLastWasRecipientOrNoMessage: Send if last was recipient or if there are no messages.
            - sendOnlyIfLastWasMeOrNoMessage: Send if last was me or if there are no messages.
            - sendOnlyIfNoMessage: Send only if there are no messages in the thread.
            - sendOnlyIfNoReply: Send only if there was no reply from the recipient.

    Returns:
        True if the message was sent, False otherwise. Or an error dict if something went wrong
    """
    if not (PHANTOMBUSTER_API_KEY and LINKEDIN_COOKIE_LI and LINKEDIN_BROWSER_AGENT):
        return {"error": True, "message": "PHANTOMBUSTER_API_KEY, LINKEDIN_COOKIE_LI or LINKEDIN_BROWSER_AGENT are not set in environment variables"}

    credentials = PhantomCredentials(
        phantombuster_key=PHANTOMBUSTER_API_KEY,
        session_cookie=LINKEDIN_COOKIE_LI,
        user_agent=LINKEDIN_BROWSER_AGENT
    )

    sender_agent = PhantomAgentMessageSender(credentials=credentials)
    status, success = sender_agent.run_and_get_data(linkedin, message, message_control)

    return success


@mcp.tool()
def scrap_activities(
     linkedin: str, 
     max_activities: int = 10, 
     activities_to_scrape: list = ["Posts", "Article"],
     date_after: int = 30
     ) -> list[Activity]:

    """
    Scrapes activities for a LinkedIn profile or company.

    Args:
        linkedin: URL of the LinkedIn profile or company.
        max_activities: Maximum number of activities to scrape (default: 10).
        activities_to_scrape: List of activity types to scrape. Possible values:
            - "Posts"
            - "Article"
            - "Comments"
            - "Reactions"
            - "Documents"
            - "Newsletters"
            - "Events"
        date_after: Number of days from today to scrape activities for (default: 30).

    Returns:
        List of Activity objects with scraped data, or an error if data could not be retrieved.
    """
    if not (PHANTOMBUSTER_API_KEY and LINKEDIN_COOKIE_LI and LINKEDIN_BROWSER_AGENT):
        return {"error": True, "message": "PHANTOMBUSTER_API_KEY, LINKEDIN_COOKIE_LI or LINKEDIN_BROWSER_AGENT are not set in environment variables"}

    credentials = PhantomCredentials(
        phantombuster_key=PHANTOMBUSTER_API_KEY,
        session_cookie=LINKEDIN_COOKIE_LI,
        user_agent=LINKEDIN_BROWSER_AGENT
    )

    sender_agent = PhantomAgentActivities(
         credentials=credentials,
         nb_max_posts=max_activities,
         activities_to_scrape=activities_to_scrape,
         date_after=date_after
    )
    status, success = sender_agent.run_and_get_data(linkedin)

    return success
    
# Run the MCP server locally
if __name__ == '__main__':
    mcp.run()