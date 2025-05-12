import json
from typing import List, Optional
from mcp_server.phantombuster.base import PhantomAgentBase, PhantomCredentials
from mcp_server.phantombuster.models import Profile, Job

class PhantomAgentProfile(PhantomAgentBase):
    def __init__(
            self, 
            credentials: PhantomCredentials, 
            agent_id: Optional[str] = None, 
            max_retries: int = 20, 
            retry_delay: int = 10
        ):

        super().__init__(credentials, agent_id, max_retries, retry_delay)
        self.script_id = "3112"
        self.script = "LinkedIn Profile Scraper.js"
        self.name = "LinkedIn Profile Scraper (API)"

    def run(self, linkedin_url: str) -> bool:
        """Start phantom task to scrape profile"""
        data = {
            "id": self.agent_id,
            "argument": {
                "userAgent": self.credentials.user_agent,
                "sessionCookie": self.credentials.session_cookie,
                "spreadsheetUrl": linkedin_url,
                "takeScreenshot": False,
                "updateCrmContacts": False,
                "numberOfAddsPerLaunch": 10,
                "takePartialScreenshot": False,
                "saveImg": False
            }
        }
        return self._post(self.lanch_url, data)

    def get_data(self, filter_field: Optional[str] = None, filter_value: Optional[str] = None) -> Optional[Profile]:
        """Get processed profile data from phantom task
        
        Args:
            filter_field: Optional field name to filter results by
            filter_value: Optional value that the field should match
            
        Returns:
            Profile object if data is found and matches filter criteria, None otherwise
        """
        result = self.get_raw_data()
        result_obj = json.loads(result.get("resultObject"))
        if result_obj:
            for value in result_obj:
                # Apply filtering if specified
                if filter_field is not None and filter_value is not None:
                    field_value = value.get(filter_field)
                    if field_value != filter_value:
                        continue

                # Process jobs
                jobs = []
                # Current job
                jobs.append(Job(
                    company_url=value.get("linkedinCompanyUrl", ""),
                    company_name=value.get("companyName", ""),
                    title=value.get("linkedinJobTitle", ""),
                    date_range=value.get("dateRange", ""),
                    started_since=value.get("startedSince", ""),
                    description=value.get("linkedinJobDescription", ""), 
                    location=value.get("linkedinJobLocation", "")
                ))
                # Previous job
                jobs.append(Job(
                    company_url=value.get("linkedinPreviousCompanyUrl", ""),
                    company_name=value.get("linkedinPreviousCompanyName", ""),
                    title=value.get("linkedinPreviousJobTitle", ""),
                    date_range=value.get("linkedinPreviousJobDateRange", ""),
                    started_since=value.get("linkedinPreviousStartedSince", ""),
                    description=value.get("linkedinPreviousJobDescription", ""), 
                    location=value.get("linkedinPreviousJobLocation", "")
                ))

                # Convert skills from string to list if needed
                skills = value.get("linkedinSkillsLabel", [])
                if isinstance(skills, str):
                    skills = [skill.strip() for skill in skills.split(',')]

                return Profile(
                    linkedin_url=value.get("linkedinProfileUrl", ""),
                    first_name=value.get("firstName", ""),
                    last_name=value.get("lastName", ""),
                    headline=value.get("linkedinHeadline", ""),
                    location=value.get("location", ""),
                    company=value.get("companyName", ""),
                    job_title=value.get("linkedinJobTitle", ""),
                    about=value.get("linkedinDescription", ""),
                    skills=skills,
                    jobs=jobs,
                    company_industry=value.get('companyIndustry'),
                    linkedin_user_id=value.get('linkedinProfileId'),
                    linkedin_urn=value.get('linkedinProfileUrn'),
                    raw_data=value
                )
        return None

class PhantomAgentSalesNavigatorProfile(PhantomAgentBase):
    def __init__(
            self, 
            credentials: PhantomCredentials, 
            agent_id: Optional[str] = None, 
            max_retries: int = 20, 
            retry_delay: int = 10, 
            nb_result: int = 20
        ):

        super().__init__(credentials, agent_id, max_retries, retry_delay)
        self.script_id = "6988"
        self.script = "Sales Navigator Search Export.js"
        self.name = "Sales Navigator Search Export (API)"
        self.nb_result = nb_result

    def run(self, search_url: str) -> bool:
        """Start phantom task to search profiles in Sales Navigator
        Args:
            search_url: Sales Navigator search URL
        """
        data = {
            "id": self.agent_id,
            "argument": {
                "userAgent": self.credentials.user_agent,
                "sessionCookie": self.credentials.session_cookie,
                "salesNavigatorSearchUrl": search_url,
                "inputType": "salesNavigatorSearchUrl",
                "numberOfProfiles": 2500,
                "numberOfLinesPerLaunch": 20,
                "removeDuplicateProfiles": False,
                "numberOfResultsPerSearch": self.nb_result
            }
        }
        return self._post(self.lanch_url, data)

    def get_data(self) -> List[Profile]:
        """Get processed profiles from phantom task"""
        profiles = []
        result = self.get_raw_data()
        result_obj = json.loads(result.get("resultObject"))
        if result_obj:
            for value in result_obj:
                if value.get('defaultProfileUrl'):
                    profile = Profile(
                        linkedin_url=value.get('defaultProfileUrl', ""),
                        first_name=value.get('firstName', ""),
                        last_name=value.get('lastName', ""),
                        headline=value.get('title', ""),  # Using title as headline
                        location=value.get('location', ""),
                        company=value.get('companyName', ""),
                        job_title=value.get('title', ""),
                        about=value.get('summary', "") or value.get('titleDescription', ""),
                        skills=[],  # Sales Navigator search doesn't provide skills
                        jobs=[],  # Sales Navigator search doesn't provide detailed job info
                        raw_data=value
                    )
                    profiles.append(profile)
        return profiles 