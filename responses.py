from pydantic import BaseModel
from typing import List, Optional
class WebsiteSchemaFieldResponse(BaseModel):
    name: str
    selector: str
    type: str
    attribute: Optional[str]
    fields: Optional[List['WebsiteSchemaFieldResponse']] = None
    class Config:
        from_attributes= True
class WebsiteSchemaResponse(BaseModel):
    name: str
    baseSelector: str
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