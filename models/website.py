from models.db_model import DbModel
from models.website_schema import WebsiteSchema, WebsiteSchemaField
from web_requests import WebsiteRequest
from uuid import uuid4

class Website(DbModel):
    def __init__(self, id: str, url: str, name: str, website_schema: WebsiteSchema, pagination_schema: WebsiteSchema):
        self.id = id if id else str(uuid4())
        self.url = url
        self.name = name
        self.website_schema = website_schema
        self.pagination_schema = pagination_schema

    def to_dict(self): 
        """Convert object to a dictionary so it can be inserted in MongoDB."""
        return {
            "_id": self.id,
            "url": self.url,
            "name": self.name,
            "website_schema": self.website_schema.to_dict(),
            "pagination_schema": self.pagination_schema.to_dict(),
            **self.get_audit_dict()
        }

    @classmethod
    def from_dict(cls, data): 
        """Create the Website object from MongoDB data/dictionary"""
        return cls(
            id=str(data.get("_id")),
            url=data["url"],
            name=data["name"],
            website_schema=WebsiteSchema.from_dict(data["website_schema"]),
            pagination_schema=WebsiteSchema.from_dict(data["pagination_schema"])
        )

    @staticmethod
    def create_schema_fields(fields):
        if not fields:
            return None
        return [WebsiteSchemaField(
            name=field.name,
            selector=field.selector,
            attribute=field.attribute,
            type=field.type,
            fields=Website.create_schema_fields(field.fields)
        ) for field in fields]

    @classmethod
    def from_request(cls, request: WebsiteRequest):
        return cls(
            id=None,
            name=request.name,
            url=request.url,
            website_schema=WebsiteSchema(
                name=request.website_schema.name,
                base_selector=request.website_schema.baseSelector,
                fields=Website.create_schema_fields(request.website_schema.fields)
            ),
            pagination_schema=WebsiteSchema(
                name=request.pagination_schema.name,
                base_selector=request.pagination_schema.baseSelector,
                fields=Website.create_schema_fields(request.pagination_schema.fields)
            )
        )