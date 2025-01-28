
from uuid import uuid4
from typing import List, Optional
from datetime import datetime
from web_requests import WebsiteRequest

class DbModel:
    id: str
    date_time_created: str
    date_time_modified: str
    date_time_deleted: str
    deleted: bool

    def set_audit_fields(cls):
        cls.date_time_created = datetime.utcnow()
        cls.date_time_modified = datetime.utcnow()

class User(DbModel):
    def __init__(self, id, email, name):
        self.id = id if id else str(uuid4())
        self.email = email
        self.name = name
        
class WebsiteSchemaField:
    def __init__(self, name: str, selector: str, type: str,  fields: Optional[List['WebsiteSchemaField']] = None, attribute=None):
        self.name = name
        self.selector = selector
        self.type = type
        self.attribute = attribute
        self.fields = fields if fields is not None else []

    def to_dict(self):
        """Convert WebsiteSchemaField object to a dictionary."""
        return {
            "name": self.name,
            "selector": self.selector,
            "attribute": self.attribute,
            "type": self.type,
            "fields": [field.to_dict() for field in self.fields]
        }
    
    @classmethod
    def from_dict(cls, data): 
        """Create the WebsiteSchemaFiled object from MongoDB data/dictionary"""
        return cls(
            name=data["name"],
            type=data["type"],
            attribute=data["attribute"],
            selector=data["selector"],
            fields=[WebsiteSchemaField.from_dict(field) for field in data.get("fields")]
        )


class WebsiteSchema: 
    name: str
    baseSelector: str
    fields: List[WebsiteSchemaField]
    def __init__(self, name, base_selector, fields):
        self.name = name
        self.baseSelector = base_selector
        self.fields = fields

    def to_dict(self): 
        """Convert object to a dictionary so it can be inserted in MongoDB."""
        return {
            "name": self.name,
            "baseSelector": self.baseSelector,
            "fields": [field.to_dict() for field in self.fields]
        }

    @classmethod
    def from_dict(cls, data): 
        """Create the WebsiteSchema object from MongoDB data/dictionary"""
        return cls(
            name=data["name"],
            base_selector=data["baseSelector"],
            fields=[WebsiteSchemaField.from_dict(field) for field in data["fields"]]
        )

class Website(DbModel):
    def __init__(self, id: str, url: str, name: str, page_query_parameter: str, website_schema: WebsiteSchema):
        self.id = id if id else str(uuid4())
        self.url = url
        self.name = name
        self.page_query_parameter = page_query_parameter
        self.website_schema= website_schema

    def to_dict(self): 
        """Convert object to a dictionary so it can be inserted in MongoDB."""
        return {
            "_id": self.id,
            "url": self.url,
            "name": self.name,
            "page_query_parameter": self.page_query_parameter,
            "website_schema": self.website_schema.to_dict(),
            "date_time_created": self.date_time_created,
            "date_time_modified": self.date_time_modified
        }

    @classmethod
    def from_dict(cls, data): 
        """Create the Website object from MongoDB data/dictionary"""
        return cls(
            id=str(data.get("_id")),
            url=data["url"],
            name=data["name"],
            page_query_parameter=data["page_query_parameter"],
            website_schema=WebsiteSchema.from_dict(data["website_schema"])
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
            page_query_parameter=request.page_query_parameter
        )
class House(DbModel):
    id: str
    external_id: str
    address: str
    price: float
    currency: str
    square_meters: int
    website_id: str
    external_id: str
    description: str

    def __init__(self, id: str, price: float, address: str, currency: str, square_meters: int, website_id: str, external_id: str, description: str):
        self.id = id if id else str(uuid4())
        self.price = price
        self.currency = currency
        self.square_meters = square_meters
        self.external_id = external_id
        self.website_id = website_id
        self.description = description
        self.address = address

    def to_dict(self): 
        """Convert object to a dictionary so it can be inserted in MongoDB."""
        return {
            "_id": self.id,
            "external_id": self.external_id,
            "address": self.address,
            "price": self.price,
            "currency" :self.currency,
            "square_meters": self.square_meters,
            "website_id": self.website_id,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data): 
        """Create the House object from MongoDB data/dictionary"""
        return cls(
            id=data.get("_id"),
            external_id=data["external_id"],
            currency=data["currency"],
            price=data["price"],
            square_meters=data["square_meters"],
            website_id=data["website_id"],
            description=data["description"]
        )

