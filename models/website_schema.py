from models.website_schema_field import WebsiteSchemaField
from typing import List

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