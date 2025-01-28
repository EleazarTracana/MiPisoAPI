import aiohttp
from repositories import WebsitesRepository, HousesRepository
from models import WebsiteSchema, Website, WebsiteSchemaField
from responses import WebsiteResponse
from web_requests import WebsiteRequest
from fastapi import Depends
import json
import os

CRAWL4AI_HOST = str(os.getenv('CRAWL4AI_HOST'))
CRAWL4AI_API_TOKEN=str(os.getenv('CRAWL4AI_API_TOKEN'))

class Crawl4AIClient:
    def __init__(self, client: aiohttp.ClientSession):
        self.client = client

    async def get_crawl(cls, task_id: str):
        return await cls.client.get(f"{CRAWL4AI_HOST}/task/{task_id}")

    async def run_crawl(cls, url: str, schema: WebsiteSchema):
        return await cls.client.post(f"{CRAWL4AI_HOST}/crawl",
            json={
                "urls": url,
                "cache_mode": "bypass",
                "extraction_config": {
                    "type": "json_css",
                    "params": {"schema": schema.to_dict()}
                }
            }
        )    

async def get_crawl4ai_client():
    try:
        client = aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {CRAWL4AI_API_TOKEN}"
        })

        return Crawl4AIClient(client)
    finally:
        pass

class WebsiteService():
    def __init__(self, websites_repository: WebsitesRepository = Depends(), houses_repository: HousesRepository = Depends(), craw4ai_client: Crawl4AIClient = Depends(get_crawl4ai_client)) -> None:
        self.websites_repository = websites_repository
        self.houses_repository = houses_repository,
        self.craw4ai_client = craw4ai_client

    async def create_by_request(cls, request: WebsiteRequest) -> WebsiteResponse:
        website = Website.from_request(request)
        result = await cls.websites_repository.insert_one(website)
        return WebsiteResponse.from_orm(result)

    async def find_one_by_id(cls, website_id: str) -> WebsiteResponse:
        result = await cls.websites_repository.find_one(website_id)
        return WebsiteResponse.from_orm(result)

    async def run_crawl_by_website_id(cls, website_id: str):
        website = await cls.websites_repository.find_one(website_id)
        response = await cls.craw4ai_client.run_crawl(website.url, website.website_schema)
        return await response.json()

    async def get_crawl_by_website_id_and_crawl_id(cls, website_id: str, crawl_id: str):
        result = await cls.craw4ai_client.get_crawl(crawl_id)
        result_as_json = await result.json()
        extracted_content = result_as_json["result"]["extracted_content"]
        extracted_json_result = json.loads(extracted_content),
        return json.loads(extracted_content)

    async def update_houses(cls, website_id: str, crawl_result):
        
        pass

