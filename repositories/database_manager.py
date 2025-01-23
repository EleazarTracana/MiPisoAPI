
from contextlib import asynccontextmanager
import os
from motor.motor_asyncio import AsyncIOMotorClient

CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
DATABASE_NAME = os.getenv('DATABASE_NAME')

class DatabaseManager:
    def __init__(self):
        self.client = AsyncIOMotorClient(CONNECTION_STRING)
        self.db = self.client[DATABASE_NAME]

@asynccontextmanager
async def get_database():
    db_manager = DatabaseManager()
    try:
        yield db_manager
    finally:
        await db_manager.client.close()
        