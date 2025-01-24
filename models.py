
from uuid import uuid4

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
        
class WebsiteSchemaField():
    name: str
    selector: str
    type: str
    def __init__(self, name, selector, type):
        self.name = name,
        self.selector = selector,
        self.type = type

class WebsiteSchema(): 
    name: str
    base_selector: str
    fields: list[WebsiteSchemaField]

class Website(DbModel):
    url: str
    name: str
    description: str
    page_query_parameter: str
    schema: WebsiteSchema
    def __init__(self, id, url, name, page_query_parameter, schema):
        self.id = id if id else str(uuid4())
        self.url = url
        self.name = name
        self.page_query_parameter = page_query_parameter
        self.schema= schema

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