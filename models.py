
from uuid import uuid4
from typing import List

class DbModel:
    id: str
    date_time_created: str
    date_time_modified: str
    date_time_deleted: str
    deleted: bool

class User(DbModel):
    def __init__(self, id, email, name):
        self.id = id if id else str(uuid4())
        self.email = email
        self.name = name
        
class WebsiteSchemaField:
    def __init__(self, name: str, selector: str, type: str):
        self.name = name
        self.selector = selector
        self.type = type

    def to_dict(self):
        """Convert WebsiteSchemaField object to a dictionary."""
        return {
            "name": self.name,
            "selector": self.selector,
            "type": self.type
        }
    
    @classmethod
    def from_dict(cls, data): 
        """Create the WebsiteSchemaFiled object from MongoDB data/dictionary"""
        return cls(
            name=data["name"],
            type=data["type"],
            selector=data["selector"]
        )


class WebsiteSchema: 
    name: str
    base_selector: str
    fields: List[WebsiteSchemaField]
    def __init__(self, name, base_selector, fields):
        self.name = name
        self.base_selector = base_selector
        self.fields = fields

    def to_dict(self): 
        """Convert object to a dictionary so it can be inserted in MongoDB."""
        return {
            "name": self.name,
            "base_selector": self.base_selector,
            "fields": [field.to_dict() for field in self.fields]
        }

    @classmethod
    def from_dict(cls, data): 
        """Create the WebsiteSchema object from MongoDB data/dictionary"""
        return cls(
            name=data["name"],
            base_selector=data["base_selector"],
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
            "website_schema": self.website_schema.to_dict()
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

class House(DbModel):
    price: float
    website_id: str
    description: str

    def __init__(self, id, price, website_id, description):
        self.id = id if id else str(uuid4())
        self.price = price
        self.website_id = website_id
        self.description = description

    def to_dict(self): 
        """Convert object to a dictionary so it can be inserted in MongoDB."""
        return {
            "_id": self.id,
            "price": self.price,
            "website": self.website_id,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data): 
        """Create the House object from MongoDB data/dictionary"""
        return cls(
            id=data.get("_id"),
            price=data["price"],
            website_id=data["website_id"],
            description=data["description"]
        )