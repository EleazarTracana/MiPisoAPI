from pydantic import BaseModel

class WebsiteSchemaFieldRequest(BaseModel):
    name: str
    selector: str
    type: str
class WebsiteSchemaRequest(BaseModel):
    name: str
    base_selector: str
    fields: list[WebsiteSchemaFieldRequest]

class WebsiteRequest(BaseModel):
    name: str
    url: str
    website_schema: WebsiteSchemaRequest
    page_query_parameter: str