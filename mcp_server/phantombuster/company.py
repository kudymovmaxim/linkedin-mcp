from typing import List, Optional, Union
from mcp_server.phantombuster.base import PhantomAgentBase, PhantomCredentials
from mcp_server.phantombuster.models import Company


class PhantomAgentCompany(PhantomAgentBase):
    def __init__(
            self, 
            credentials: PhantomCredentials, 
            agent_id: Optional[str] = None, 
            max_retries: int = 20, 
            retry_delay: int = 10
        ):

        super().__init__(credentials, agent_id, max_retries, retry_delay)
        self.script_id = "3296"
        self.script = "LinkedIn Company Scraper.js"
        self.name = "LinkedIn Company Scraper (API)"

    def run(self, linkedin_url: str) -> bool:
        """Start phantom task to scrape company"""
        data = {
            "id": self.agent_id,
            "argument": {
                "userAgent": self.credentials.user_agent,
                "sessionCookie": self.credentials.session_cookie,
                "spreadsheetUrl": linkedin_url,
                "delayBetween": 2
            }
        }
        return self._post(self.lanch_url, data)

    def get_data(self, query: Optional[str] = None) -> Optional[Company]:
        """
        Get processed company data from phantom task
        Args:
            query: Optional query to filter company by
        Returns:
            Company object if found, None otherwise
        """
        result = self.get_raw_data()
        if result:
            for value in result:
                if query is not None:
                    if query != value.get("query"):
                        continue
                
                return Company(
                    name=value.get('name', ""),
                    description=value.get('description'),
                    tag_line=value.get('tagLine'),
                    website=value.get('website'),
                    location=value.get('location'),
                    country=value.get('country'),
                    city=value.get('city'),
                    geographic_area=value.get('geographicArea', value.get("companyAddress")),
                    year_founded=value.get('yearFounded', value.get("founded")),
                    currency=value.get('currency'),
                    min_revenue=value.get('minRevenue'),
                    max_revenue=value.get('maxRevenue'),
                    growth_6mth=value.get('growth6Mth'),
                    growth_1yr=value.get('growth1Yr'),
                    growth_2yr=value.get('growth2Yr'),
                    industry=value.get('industry'),
                    size=value.get('companySize'),
                    specialties=value.get('specialties'),
                    ld_id=value.get("mainCompanyID", value.get('linkedinID')),
                    employees=value.get('employeesOnLinkedIn'),
                    linkedin=value.get('companyUrl'),
                    phone=value.get('phone'),
                    linkedin_sn=value.get('salesNavigatorCompanyUrl', value.get("salesNavigatorLink"))
                )
        return None