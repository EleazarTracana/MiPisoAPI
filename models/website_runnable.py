from typing import List
from enum import Enum
from models.db_model import DbModel

class WebsiteRunnableStatus(Enum):
    CREATED: 1
    RUNNING: 2
    FINISHED: 3

class WebsiteRunnable(DbModel):
    id: str
    website_id: str
    urls: List[str]
    status: WebsiteRunnableStatus

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
        runnable = cls()
        runnable.id = str(data.get("_id"))
        runnable.website_id = data.get("website_id")
        runnable.urls = data.get("urls", [])
        runnable.status = WebsiteRunnableStatus(data.get("status"))
        runnable.set_audit_fields_from_dict(data)
        return runnable