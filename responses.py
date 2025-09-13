from pydantic import BaseModel
from models.website_runnable import WebsiteRunnableStatus
from typing import List, Optional
class WebsiteSchemaFieldResponse(BaseModel):
    name: str
    selector: str
    type: str
    attribute: Optional[str]
    fields: Optional[List['WebsiteSchemaFieldResponse']] = None
    class Config:
        from_attributes= True

class WebsiteRunnableResponse(BaseModel):
    id: str
    website_id: str
    urls: List[str]
    status: WebsiteRunnableStatus
    class Config:
        from_attributes= True

class WebsiteSchemaResponse(BaseModel):
    name: str
    baseSelector: str
    type: Optional[str] = None
    attribute: Optional[str] = None
    fields: List[WebsiteSchemaFieldResponse]
    class Config:
        from_attributes= True

class WebsiteResponse(BaseModel):
    id: str
    name: str
    pagination_schema: WebsiteSchemaResponse
    website_schema: WebsiteSchemaResponse
    class Config:
        from_attributes= True