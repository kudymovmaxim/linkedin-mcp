from typing import List, Optional
from mcp_server.base_model.MarkdownModel import MarkdownModel


class Thread(MarkdownModel):
    """LinkedIn message thread model"""
    thread_id: str
    participants: List[str]
    last_message: str
    last_message_date: str
    last_message_author_name: str
    timestamp: str
    is_last_message_from_me: bool
    read_status: bool
    linkedin_url: str


class Message(MarkdownModel):
    """LinkedIn message model"""
    date: str
    author: str
    message: str
    connection_degree: Optional[str] = None


class Job(MarkdownModel):
    """LinkedIn job experience model"""
    company_url: str
    company_name: str
    title: str
    date_range: str
    started_since: str
    description: str
    location: str


class Profile(MarkdownModel):
    """LinkedIn profile model"""
    linkedin_url: str
    first_name: str
    last_name: str
    headline: str
    location: str
    company: str
    job_title: str
    about: str
    skills: List[str]
    jobs: List[Job]
    company_industry: Optional[str] = None
    linkedin_user_id: Optional[str] = None
    linkedin_urn: Optional[str] = None
    raw_data: Optional[dict] = None


class Activity(MarkdownModel):
    """LinkedIn activity/post model"""
    url: Optional[str] = None
    attached_url: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    repost_count: Optional[int] = None
    date: Optional[str] = None
    profile_url: Optional[str] = None
    timestamp: Optional[str] = None
    comment: Optional[str] = None
    platform: str = "linkedin"


class Company(MarkdownModel):
    """LinkedIn company model"""
    name: str
    description: Optional[str] = None
    tag_line: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    geographic_area: Optional[str] = None
    year_founded: Optional[str] = None
    currency: Optional[str] = None
    min_revenue: Optional[str] = None
    max_revenue: Optional[str] = None
    growth_6mth: Optional[str] = None
    growth_1yr: Optional[str] = None
    growth_2yr: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    specialties: Optional[str] = None
    ld_id: Optional[str] = None
    employees: Optional[str] = None
    linkedin: Optional[str] = None
    phone: Optional[str] = None
    linkedin_sn: Optional[str] = None


class Connection(MarkdownModel):
    """LinkedIn connection model"""
    linkedin_url: str
    first_name: str
    last_name: str
    full_name: str
    job_title: Optional[str] = None
    date_connected: Optional[str] = None 