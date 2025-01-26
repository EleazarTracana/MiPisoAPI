from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, JsonCssExtractionStrategy, CrawlResult
from repositories import WebsitesRepository
from models import WebsiteSchema, Website
from web_requests import WebsiteRequest
from responses import WebsiteResponse
from fastapi import Depends
import json

class WebScrapperManager():
    client:  AsyncWebCrawler

    def __init__(self, client):
        self.client = client

    async def run_with_schema_configuration(cls, schema: WebsiteSchema, url: str) -> CrawlResult:
        extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
        config = CrawlerRunConfig(
            cache_mode = CacheMode.BYPASS,
            extraction_strategy=extraction_strategy,
        )
        return await cls.client.arun(
            config=config,
            url=url
        )


async def get_scraper_client():
    try:
        client = await AsyncWebCrawler().start()
        return WebScrapperManager(client)
    finally:
         await client.close()

class WebsiteService():
    def __init__(self, website_repository: WebsitesRepository = Depends(), web_scrapper: WebScrapperManager = Depends(get_scraper_client)) -> None:
        self.website_repository = website_repository
        self.web_scrapper = web_scrapper

    async def create_by_request(cls, request: WebsiteRequest) -> WebsiteResponse:
        result = await cls.website_repository.insert_one(Website(
            name=request.name,
            url=request.url,
            website_schema=request.website_schema,
            page_query_parameter=request.page_query_parameter
        ))
        return WebsiteResponse.from_orm(result)

    async def find_one_by_id(cls, website_id: str) -> WebsiteResponse:
        result = await cls.website_repository.find_one(website_id)
        return result

    async def run_scrapper_by_website_id(cls, website_id: str):
        website = await cls.website_repository.find_one(website_id)
        scrapper_result = await cls.web_scrapper.run_with_schema_configuration(website.schema, website.url)
        extracted_content = json.loads(scrapper_result)

        print(extracted_content)




