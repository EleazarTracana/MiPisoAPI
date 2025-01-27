from pydantic import BaseModel
from typing import List

class WebsiteSchemaFieldRequest(BaseModel):
    name: str
    selector: str
    type: str
class WebsiteSchemaRequest(BaseModel):
    name: str
    base_selector: str
    fields: List[WebsiteSchemaFieldRequest]

class WebsiteRequest(BaseModel):
    name: str
    url: str
    website_schema: WebsiteSchemaRequest
    page_query_parameter: str