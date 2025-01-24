
from contextlib import asynccontextmanager, contextmanager
import os
from motor.motor_asyncio import AsyncIOMotorClient

CONNECTION_STRING = str(os.getenv('MONGODB_CONNECTION_STRING'))
DATABASE_NAME = str(os.getenv('DATABASE_NAME'))

class DatabaseManager:
    def __init__(self):
        self.client = AsyncIOMotorClient(CONNECTION_STRING)
        self.db = self.client[DATABASE_NAME]

def get_database():
    db_manager = DatabaseManager()
    try:
        yield db_manager
    finally:
        db_manager.client.close()
        