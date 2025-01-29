from repositories.website_repository import WebsitesRepository
from repositories.website_runnable_repository import WebsiteRunnablesRepository
from clients.crawl4ai_client import Crawl4AIClient, get_crawl4ai_client
from fastapi import Depends
import json

class WebsiteRunnableService:
    def __init__(self, websites_repository: WebsitesRepository = Depends(), websites_runnables_repository: WebsiteRunnablesRepository = Depends(), craw4ai_client: Crawl4AIClient = Depends(get_crawl4ai_client)) -> None:
        self.websites_repository = websites_repository
        self.websites_runnables_repository = websites_runnables_repository
        self.craw4ai_client = craw4ai_client

    async def create_one(cls, website_id):
        website = await cls.websites_repository.find_one(website_id)
        result = await cls.craw4ai_client.run_crawl(website.url, website.pagination_schema)
        result_as_json = await result.json()

        response_as_json = None
        while True:
            response = await cls.craw4ai_client.get_crawl(result_as_json["task_id"])
            response_as_json = await response.json()
    
            if response_as_json["status"] != "processing":
                break


        extracted_content = response_as_json["result"]["extracted_content"]
        return json.loads(extracted_content)
         
