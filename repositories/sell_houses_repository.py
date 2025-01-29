from repositories.base_repository import BaseRepository
from repositories.database_manager import DatabaseManager, get_database
from models.sell_house import SellHouse
from fastapi import Depends

class SellHousesRepository(BaseRepository):
    def __init__(self, database_manager: DatabaseManager = Depends(get_database)):
        super().__init__("houses",database_manager)

    async def insert(self, house: SellHouse) -> str:
        house_dict = house.to_dict()
        result = await self.collection.insert_one(house_dict)  
        return str(result.inserted_id)

    async def find_one(self, houseId: str) -> str:
        result = await self.collection.find_one({ "_id": houseId})  
        if result:
            return result
        return None

    async def find_by_website_id(self, website_id: str) -> str:
        result = await self.collection.find_one({ "website_id": website_id})  
        if result:
            return result
        return None