from fastapi import FastAPI
from fastapi import Depends
from repositories.house_repository import HouseRepository
from models.requests.house_request import  HouseRequest
from models.house import House
from repositories.database_manager import DatabaseManager, get_database
from dotenv import load_dotenv 

load_dotenv() 

app = FastAPI()

test_array = [1,2,3,4,5]

def get_house_repository(db_manager: DatabaseManager = Depends(get_database)):
    return HouseRepository(db_manager)

@app.get('/api/v1/health')
async def get_health_status():
    return {"Status": "Ok"}

@app.post("/api/v1/houses", response_model=str)
async def insert_house(data: HouseRequest, house_repository: HouseRepository = Depends(get_house_repository)):
    result = await house_repository.insert(House(price= data.price, website=data.website))
    return result 





