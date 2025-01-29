

from repositories.base_repository import BaseRepository
from repositories.database_manager import DatabaseManager, get_database
from models.website import Website
from fastapi import Depends

class WebsitesRepository(BaseRepository):
    def __init__(self, database_manager: DatabaseManager = Depends(get_database)):
        super().__init__("websites",database_manager)
    
    async def find_one(self, website_id: str) -> Website:
        result = await self.collection.find_one({ "_id": website_id})  
        if result:
            return Website.from_dict(result)
        return None

    async def insert_one(self, website: Website) -> Website:
        website.set_audit_fields()
        website_dict = website.to_dict()
        result = await self.collection.insert_one(website_dict) 
        website.id = result.inserted_id 
        return website 