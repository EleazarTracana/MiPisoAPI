from models import House, User, Website
from database_manager import DatabaseManager, get_database
from datetime import datetime
from fastapi import Depends

class BaseRepository():
    def __init__(self, collection_name: str,database_manager: DatabaseManager = Depends(get_database)):
        self.collection = database_manager.db[collection_name]

class HousesRepository(BaseRepository):
    def __init__(self, database_manager: DatabaseManager = Depends(get_database)):
        super().__init__("houses",database_manager)

    async def insert(self, house: House) -> str:
        house_dict = house.to_dict()
        result = await self.collection.insert_one(house_dict)  
        return str(result.inserted_id)

    async def find_one(self, houseId: House) -> str:
        result = await self.collection.find_one({ "_id": houseId})  
        if result:
            return result
        return None

    async def find_by_website_id(self, website_id: House) -> str:
        result = await self.collection.find_one({ "website_id": website_id})  
        if result:
            return result
        return None

class UsersRepository(BaseRepository):
    def __init__(self, database_manager: DatabaseManager = Depends(get_database)):
        super().__init__("users",database_manager)


class WebsitesRepository(BaseRepository):
    def __init__(self, database_manager: DatabaseManager = Depends(get_database)):
        super().__init__("websites",database_manager)
    
    async def find_one(self, website_id: str) -> Website:
        result = await self.collection.find_one({ "_id": website_id})  
        if result:
            return Website.from_dict(result)
        return None

    async def insert_one(self, website: Website) -> Website:
        website_dict = website.to_dict()
        result = await self.collection.insert_one(website_dict) 
        website.id = result.inserted_id 
        return website 
