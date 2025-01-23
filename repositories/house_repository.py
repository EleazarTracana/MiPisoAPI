from models.house import House
from repositories.database_manager import DatabaseManager, get_database
from fastapi import Depends

class HouseRepository:
    def __init__(self, database_manager: DatabaseManager = Depends(get_database)):
        self.collection = database_manager.db["houses"]

    async def insert(self, house: House) -> str:
        house_dict = house.to_dict()
        result = await self.collection.insert_one(house_dict)
        return str(result.inserted_id)