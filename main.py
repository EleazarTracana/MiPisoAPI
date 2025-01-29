from fastapi import FastAPI, HTTPException
from fastapi import Depends
from web_requests import  WebsiteRequest
from responses import  WebsiteResponse
from dotenv import load_dotenv
from services.website_runnable_service import WebsiteRunnableService
from services.website_service import WebsiteService 

load_dotenv() 

app = FastAPI()

@app.get('/api/v1/health')
async def get_health_status():
    return {"Status": "Ok"}

@app.get("/api/v1/websites/{website_id}")
async def get_website_by_id(website_id: str, website_service: WebsiteService = Depends()) -> WebsiteResponse:
    result = await website_service.find_one_by_id(website_id)
    if not result:
        raise HTTPException(404, "Website not found")
    return result

@app.post("/api/v1/websites/{website_id}/runnables")
async def run_crawl_by_website_id(website_id: str, website_runnables_service: WebsiteRunnableService = Depends()):
    result = await website_runnables_service.create_one(website_id)
    return result
    
@app.post("/api/v1/websites/{website_id}/crawl")
async def run_crawl_by_website_id(website_id: str, website_service: WebsiteService = Depends()):
    result = await website_service.run_crawl_by_website_id(website_id)
    return result

@app.get("/api/v1/websites/{website_id}/crawl/{crawl_id}")
async def get_crawl_by_website_id_and_crawl_id(website_id: str, crawl_id: str, website_service: WebsiteService = Depends()):
    result = await website_service.get_crawl_by_website_id_and_crawl_id(website_id, crawl_id)
    return result

@app.post("/api/v1/websites")
async def create_by_request(request: WebsiteRequest, website_service: WebsiteService = Depends()) -> WebsiteResponse:
    result = await website_service.create_by_request(request)
    return result


