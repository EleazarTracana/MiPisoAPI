from repositories.website_repository import WebsitesRepository
from repositories.sell_houses_repository import SellHousesRepository
from models.website_schema import WebsiteSchema
from models.website import Website 
from models.website_schema_field import WebsiteSchemaField
from responses import WebsiteResponse
from web_requests import WebsiteRequest
from fastapi import Depends
from clients.crawl4ai_client import Crawl4AIClient, get_crawl4ai_client
import json

class WebsiteService():
    def __init__(self, websites_repository: WebsitesRepository = Depends(), houses_repository: SellHousesRepository = Depends(), craw4ai_client: Crawl4AIClient = Depends(get_crawl4ai_client)) -> None:
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
        return json.loads(extracted_content)

    async def update_houses(cls, website_id: str, crawl_result):
        
        pass

