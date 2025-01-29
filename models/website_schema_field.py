from typing import Optional, List

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