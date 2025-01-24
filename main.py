from fastapi import FastAPI
from fastapi import Depends
from repositories import WebsitesRepository
from models.requests.house_request import  HouseRequest
from models.responses.house_response import  HouseResponse

from models import House
from dotenv import load_dotenv 

load_dotenv() 

app = FastAPI()

@app.get('/api/v1/health')
async def get_health_status():
    return {"Status": "Ok"}

@app.get("/api/v1/websites/{websiteId}")
async def get_house_by_id(websiteId: str, websites_repository: WebsitesRepository = Depends()):
    result = await websites_repository.find_one(websiteId)
    if result:
        HouseResponse.from_orm(result)
    return None

@app.get("/api/v1/websites/{websiteId}")
async def get_house_by_id(websiteId: str, websites_repository: WebsitesRepository = Depends()):
    result = await websites_repository.find_one(websiteId)
    if result:
        HouseResponse.from_orm(result)
    return None


