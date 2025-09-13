from models.db_model import DbModel
from uuid import uuid4

class SellHouse(DbModel):
    def __init__(self, id: str, price: float, address: str, currency: str, square_meters: int, website_id: str, external_id: str, description: str, images: list[str], title: str):
        self.id = id if id else str(uuid4())
        self.price = price
        self.currency = currency
        self.square_meters = square_meters
        self.external_id = external_id
        self.website_id = website_id
        self.description = description
        self.title = title
        self.images = images
        self.address = address

    def to_dict(self): 
        """Convert object to a dictionary so it can be inserted in MongoDB."""
        return {
            "_id": self.id,
            "external_id": self.external_id,
            "address": self.address,
            "title": self.title,
            "price": self.price,
            "currency" :self.currency,
            "square_meters": self.square_meters,
            "website_id": self.website_id,
            "description": self.description,
            "images": self.images,
             **self.get_audit_dict()
        }

    @classmethod
    def from_dict(cls, data): 
        """Create the House object from MongoDB data/dictionary"""
        house = cls()
        house.id = str(data.get("_id"))
        house.external_id = data.get("external_id")
        house.title = data.get("title")
        house.currency = data.get("currency")
        house.price = data.get("price")
        house.square_meters = data.get("square_meters")
        house.website_id = data.get("website_id")
        house.description = data.get("description")
        house.images = data.get("images")
        house.set_audit_fields_from_dict(data)
        return house