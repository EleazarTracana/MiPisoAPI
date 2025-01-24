from fastapi import FastAPI
from fastapi import Depends
from repositories import WebsitesRepository
from requests import  WebsiteRequest
from responses import  WebsiteResponse
from models import Website
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
        WebsiteResponse.from_orm(result)
    return None

@app.post("/api/v1/websites")
async def get_house_by_id(request: WebsiteRequest, websites_repository: WebsitesRepository = Depends()) -> WebsiteResponse:
    result = await websites_repository.insert_one(Website(
        name=request.name,
        url=request.url
    ))
    if result:
        WebsiteResponse.from_orm(result)
    return None


