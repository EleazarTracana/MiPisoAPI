from pydantic import BaseModel
from models import WebsiteSchema

class WebsiteRequest(BaseModel):
    name: str
    url: str
    website_schema: WebsiteSchema
    page_query_parameter: str