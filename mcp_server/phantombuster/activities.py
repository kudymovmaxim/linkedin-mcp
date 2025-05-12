import json
from typing import List, Optional
from datetime import datetime, timedelta
from mcp_server.phantombuster.base import PhantomAgentBase, PhantomCredentials
from mcp_server.phantombuster.models import Activity


class PhantomAgentActivities(PhantomAgentBase):
    def __init__(self, 
                 credentials: PhantomCredentials, 
                 agent_id: Optional[str] = None, 
                 max_retries: int = 20, 
                 retry_delay: int = 10, 
                 nb_max_posts: int = 20, 
                 activities_to_scrape: List[str] = None, 
                 date_after: Optional[int] = None
        ):

        super().__init__(credentials, agent_id, max_retries, retry_delay)
        self.script_id = "9136"
        self.script = "LinkedIn Activity Extractor.js"
        self.name = "LinkedIn Activity Extractor (API)"
        
        self.nb_max_posts = nb_max_posts
        self.activities_to_scrape = activities_to_scrape or ["Post", "Article"]
        self.date_after = date_after

    def run(self, linkedin_url: str) -> bool:
        """Start phantom task to scrape activities"""

        data = {
            "id": self.agent_id,
            "argument": {
                "userAgent": self.credentials.user_agent,
                "sessionCookie": self.credentials.session_cookie,
                "spreadsheetUrl": linkedin_url,
                "numberMaxOfPosts": self.nb_max_posts,
                "activitiesToScrape": self.activities_to_scrape
            }
        }

        if self.date_after is not None:
            current_date = datetime.now()
            target_date = current_date - timedelta(days=self.date_after)
            data["argument"]["dateAfter"] = target_date.strftime("%m-%d-%Y")
            data["argument"]["onlyRetrieveActivitiesAfterDate"] = True

        return self._post(self.lanch_url, data)

    def get_data(self) -> List[Activity]:
        """Get processed activities from phantom task"""
        
        result = self.get_raw_data()
        result_obj = json.loads(result.get("resultObject"))
        activities = []
        if result_obj:
            for value in result_obj:
                activity = Activity(
                    url=value.get('postUrl', ""),
                    attached_url=value.get('imgUrl'),
                    type=value.get('type', ""),
                    text=value.get('postContent'),
                    like_count=value.get('likeCount'),
                    comment_count=value.get('commentCount'),
                    repost_count=value.get('repostCount'),
                    date=value.get('postDate'),
                    profile_url=value.get('profileUrl'),
                    timestamp=value.get('timestamp'),
                    comment=value.get('commentContent')
                )
                activities.append(activity)
        return activities 