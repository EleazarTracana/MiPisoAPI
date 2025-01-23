
from uuid import uuid4

class House:
    def __init__(self, price, website):
        self.id = str(uuid4())
        self.price = price
        self.website = website

    def to_dict(self): 
        """Convert object to a dictionary so it can be inserted in MongoDB."""
        return {
            "_id": self.id,
            "price": self.price,
            "website": self.website
        }

    @classmethod
    def from_dict(cls, data): 
        """Create the House object from MongoDB data/dictionary"""
        return cls(
            id=data.get("_id"),
            price=data["price"],
            website=data["website"]
        )