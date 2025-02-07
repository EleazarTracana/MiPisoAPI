from repositories.website_repository import WebsitesRepository
from repositories.website_runnable_repository import WebsiteRunnablesRepository
from clients.crawl4ai_client import Crawl4AIClient, get_crawl4ai_client
from models.website_runnable import WebsiteRunnable, WebsiteRunnableStatus
from models.sell_house import SellHouse
from fastapi import Depends
from responses import WebsiteRunnableResponse
from repositories.sell_houses_repository import SellHousesRepository
from typing import List
import json

class WebsiteRunnableService:
    global max_chunk_runnable
    max_chunk_runnable = 100

    def __init__(self, websites_repository: WebsitesRepository = Depends(), 
    websites_runnables_repository: WebsiteRunnablesRepository = Depends(), 
    sell_houses_repository: SellHousesRepository = Depends(),
    craw4ai_client: Crawl4AIClient = Depends(get_crawl4ai_client)) -> None:

        self.websites_repository = websites_repository
        self.websites_runnables_repository = websites_runnables_repository
        self.craw4ai_client = craw4ai_client
        self.sell_houses_repository = sell_houses_repository

    def __create_set_of_urls(self, base_url: str, max_page: int) -> List[str]:
        all_urls = []
        for i in range(max_page):
            all_urls.append(f"{base_url}?pagina-{i+1}")
        return all_urls

    def __clean_square_meters(raw_square_meters: str) -> int:
        my_list = raw_square_meters.split(" ")
        if list.count == 2 and list[1] == "m² cubie.":
            return int(my_list[0])
        return None

    async def run_by_website_id(cls, website_id):
        website = await cls.websites_repository.find_one(website_id)
        runnables = await cls.websites_runnables_repository.find_by_website_id(website_id)
        for runnable in runnables:
            result = await cls.craw4ai_client.run_crawl(runnable.urls, website.website_schema)
            result_as_json = await result.json()
            while True:
                response = await cls.craw4ai_client.get_crawl(result_as_json["task_id"])
                response_as_json = await response.json()
                if response_as_json["status"] != "processing" and response_as_json["status"] != "pending":
                    extracted_content = response_as_json["result"]["extracted_content"]
                    all_houses: List = json.loads(extracted_content)
                    for house in all_houses:
                        await cls.sell_houses_repository.insert(SellHouse(
                            id=None,
                            currency=house["currency"],
                            price=int(house["price"]),
                            address=house["address"],
                            description=house["description"],
                            square_meters=cls.__clean_square_meters(house["square_meters"])
                        ))
        return

    async def create_by_website_id(cls, website_id):
        website = await cls.websites_repository.find_one(website_id)
        result = await cls.craw4ai_client.run_crawl(website.url, website.pagination_schema)
        result_as_json = await result.json()

        response_as_json = None
        while True:
            response = await cls.craw4ai_client.get_crawl(result_as_json["task_id"])
            response_as_json = await response.json()
    
            if response_as_json["status"] != "processing" and response_as_json["status"] != "pending":
                break

        extracted_content = response_as_json["result"]["extracted_content"]
        final_result = json.loads(extracted_content)
        max_page = int(final_result[0]["max_page"])

        all_urls: List[str] = cls.__create_set_of_urls(website.url, max_page)
        chunk_urls = []
        created_runnables: List[WebsiteRunnable] = []
        for i in range(len(all_urls)):
            if len(chunk_urls) == max_chunk_runnable:
                created_runnable = await cls.websites_runnables_repository.insert_one(WebsiteRunnable(
                    id=None,
                    website_id=website_id,
                    urls=chunk_urls.copy(),
                    status=WebsiteRunnableStatus.CREATED
                ))
                created_runnables.append(created_runnable)
                chunk_urls.clear()
            else:
                chunk_urls.append(all_urls[i])

        created_runnables_response: List[WebsiteRunnableResponse] = []
        for runnable in created_runnables:
            created_runnables_response.append(WebsiteRunnableResponse.from_orm(runnable))

        return created_runnables_response
            
    

         
