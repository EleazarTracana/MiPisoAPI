from typing import List
from enum import Enum
from models.db_model import DbModel
from uuid import uuid4

class WebsiteRunnableStatus(Enum):
    CREATED = 1
    RUNNING = 2
    FINISHED = 3

class WebsiteRunnable(DbModel):
    def __init__(self,id: str, website_id: str, urls: List[str], status: WebsiteRunnableStatus):
        self.id = id if id else str(uuid4())
        self.website_id = website_id
        self.urls = urls
        self.status = status

    def to_dict(self) -> dict:
        return {
            "_id": self.id,
            "website_id": self.website_id,
            "urls": self.urls,
            "status": self.status.value,
            **self.get_audit_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WebsiteRunnable':
        runnable = cls(
            id=str(data.get("_id")),
            website_id=data.get("website_id"),
            urls=data.get("urls", []),
            status=WebsiteRunnableStatus(data.get("status"))
        )
        runnable.set_audit_fields_from_dict(data)
        return runnable