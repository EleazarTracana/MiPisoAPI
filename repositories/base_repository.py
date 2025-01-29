
from repositories.database_manager import DatabaseManager, get_database
from fastapi import Depends


class BaseRepository():
    def __init__(self, collection_name: str,database_manager: DatabaseManager = Depends(get_database)):
        self.collection = database_manager.db[collection_name]
