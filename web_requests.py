from pydantic import BaseModel
from typing import List, Optional

class WebsiteSchemaFieldRequest(BaseModel):
    name: str
    selector: str
    type: str
    attribute: Optional[str] = None
    fields: Optional[List['WebsiteSchemaFieldRequest']] = None

class WebsiteSchemaRequest(BaseModel):
    name: str
    baseSelector: str
    fields: List[WebsiteSchemaFieldRequest]

class WebsiteRequest(BaseModel):
    name: str
    url: str
    website_schema: WebsiteSchemaRequest
    page_query_parameter: str