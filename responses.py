from pydantic import BaseModel
from models import WebsiteSchema

class WebsiteResponse(BaseModel):
    id: str
    name: str
    description: str
    page_query_parameter: str
    schema: WebsiteSchema
    class Config:
        from_attributes= True