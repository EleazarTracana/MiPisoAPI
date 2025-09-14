from repositories.website_repository import WebsitesRepository
from repositories.website_runnable_repository import WebsiteRunnablesRepository
from clients.crawl4ai_client import Crawl4AIClient, get_crawl4ai_client
from models.website_runnable import WebsiteRunnable, WebsiteRunnableStatus
from models.website_schema import WebsiteSchema
from models.sell_house import SellHouse
from fastapi import Depends
from responses import WebsiteRunnableResponse
from repositories.sell_houses_repository import SellHousesRepository
from typing import List
import time
import json
import asyncio

class WebsiteRunnableService:
    global max_chunk_runnable
    max_chunk_runnable = 1
    runnable_wait_interval = 1
    max_concurrent_tasks = 12

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

    def __clean_square_meters(self, raw_square_meters: str) -> float:
        my_list = raw_square_meters.split(" ")
        if len(my_list) == 4 and my_list[2] == "m²":
            return float(my_list[0].replace(",", "."))
        return None

    async def __process_runnable(self, runnable: WebsiteRunnable, website_schema: WebsiteSchema):
        """
        Process a runnable by running a crawl, waiting to be finished,
        parses the result to our house model and is inserted in the repository
        """
        task_id = await self.__run_crawl(runnable, website_schema)
        results = await self.__get_crawl(task_id)
        for raw_result in results:
            try:
                await self.__process_runnable_result(raw_result, runnable.website_id)
                print(f"Processed result for runnable {runnable.id}", flush=True)
            except Exception as e:
                print(f"Error processing result for runnable {runnable.id}: {e}")

    async def __process_runnable_result(self, raw_result, website_id):
        """
        Parses the extracted content from the crawl api result and maps each
        item individually to our house model.
        """
        extracted_content = raw_result["extracted_content"]
        extracted_content_json: List = json.loads(extracted_content)
        for result in extracted_content_json:
            for item in result["houses"]:
                await self.sell_houses_repository.insert(SellHouse(
                    id=None,
                    website_id=website_id,
                    external_id=item["external_id"],
                    currency=item["currency"],
                    price=int(item["price"]),
                    address=item["address"],
                    description=item["description"],
                    title=item["title"],
                    images=item["photos"],
                    square_meters=self.__clean_square_meters(item["square_meters"])
                ))

    async def __run_crawl(self, website_runnable: WebsiteRunnable, website_schema: WebsiteSchema) -> str:
        raw_result = await self.craw4ai_client.run_crawl(website_runnable.urls, website_schema)
        json_result = await raw_result.json()
        return json_result["task_id"]

    async def __get_crawl(self, task_id: str):
        await asyncio.sleep(self.runnable_wait_interval)
        raw_response = await self.craw4ai_client.get_crawl(task_id)
        json_response = await raw_response.json()
        if self.__is_crawl_finished(json_response):
            return json_response["results"]
        else:
            return await self.__get_crawl(task_id)

    def __is_crawl_finished(self, response) -> bool:
        return response["status"] != "processing" and response["status"] != "pending"

    async def run_by_website_id(cls, website_id) -> bool:
        website = await cls.websites_repository.find_one(website_id)
        runnables = await cls.websites_runnables_repository.find_by_website_id(website_id)
        semaphore = asyncio.Semaphore(cls.max_concurrent_tasks)

        async def sem_task(runnable):
            async with semaphore:
                await cls.__process_runnable(runnable, website.website_schema)

        tasks = [sem_task(runnable) for runnable in runnables]
        await asyncio.gather(*tasks)
        return True

    async def run_single_by_website(cls, website_id, runnable_id) -> bool: 
        website = await cls.websites_repository.find_one(website_id)
        runnable = await cls.websites_runnables_repository.find_one(runnable_id)
        await cls.__process_runnable(runnable, website.website_schema)
        return True

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
            created_runnables_response.append(
                WebsiteRunnableResponse.from_orm(runnable))

        return created_runnables_response
