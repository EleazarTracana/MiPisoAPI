from typing import List
from repositories.base_repository import BaseRepository
from repositories.database_manager import DatabaseManager, get_database
from models.website_runnable import WebsiteRunnable, WebsiteRunnableStatus
from fastapi import Depends

class WebsiteRunnablesRepository(BaseRepository):
    def __init__(self, database_manager: DatabaseManager = Depends(get_database)):
        super().__init__("website_runnables", database_manager)
    
    async def find_one(self, runnable_id: str) -> WebsiteRunnable:
        result = await self.collection.find_one({"_id": runnable_id})
        if result:
            return WebsiteRunnable.from_dict(result)
        return None
    
    async def find_by_website_id(self, website_id: str) -> List[WebsiteRunnable]:
        cursor = self.collection.find({"website_id": website_id})
        results = await cursor.to_list(length=None)
        return [WebsiteRunnable.from_dict(result) for result in results]
    
    async def insert_one(self, runnable: WebsiteRunnable) -> WebsiteRunnable:
        runnable.set_audit_fields()
        runnable_dict = runnable.to_dict()
        result = await self.collection.insert_one(runnable_dict)
        
        runnable.id = result.inserted_id
        return runnable
    
    async def update_status(self, runnable_id: str, status: WebsiteRunnableStatus) -> bool:
        result = await self.collection.update_one(
            {"_id": runnable_id},
            {"$set": {"status": status.value}}
        )
        return result.modified_count > 0