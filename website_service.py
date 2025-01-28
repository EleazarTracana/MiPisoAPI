import aiohttp
from repositories import WebsitesRepository
from models import WebsiteSchema, Website, WebsiteSchemaField
from responses import WebsiteResponse
from web_requests import WebsiteRequest
from fastapi import Depends
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
    def __init__(self, website_repository: WebsitesRepository = Depends(), craw4ai_client: Crawl4AIClient = Depends(get_crawl4ai_client)) -> None:
        self.website_repository = website_repository
        self.craw4ai_client = craw4ai_client

    async def create_by_request(cls, request: WebsiteRequest) -> WebsiteResponse:
        website = Website.from_request(request)
        result = await cls.website_repository.insert_one(website)
        return WebsiteResponse.from_orm(result)

    async def find_one_by_id(cls, website_id: str) -> WebsiteResponse:
        result = await cls.website_repository.find_one(website_id)
        return WebsiteResponse.from_orm(result)

    async def run_crawl_by_website_id(cls, website_id: str):
        website = await cls.website_repository.find_one(website_id)
        response = await cls.craw4ai_client.run_crawl(website.url, website.website_schema)
        return await response.json()

    async def get_crawl_by_website_id_and_crawl_id(cls, website_id: str, crawl_id: str):
        result = await cls.craw4ai_client.get_crawl(crawl_id)
        return (await result.json())


