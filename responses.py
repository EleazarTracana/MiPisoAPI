from pydantic import BaseModel
from typing import List
class WebsiteSchemaFieldResponse(BaseModel):
    name: str
    selector: str
    type: str
    class Config:
        from_attributes= True
class WebsiteSchemaResponse(BaseModel):
    name: str
    base_selector: str
    fields: List[WebsiteSchemaFieldResponse]
    class Config:
        from_attributes= True

class WebsiteResponse(BaseModel):
    id: str
    name: str
    page_query_parameter: str
    website_schema: WebsiteSchemaResponse
    class Config:
        from_attributes= True