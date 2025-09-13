import os
from typing import  List

CRAWL4AI_HOST = str(os.getenv('CRAWL4AI_HOST'))
CRAWL4AI_API_TOKEN=str(os.getenv('CRAWL4AI_API_TOKEN'))

import aiohttp
from models.website_schema import WebsiteSchema

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

    async def run_many_crawl(cls, urls: List[str], schema: WebsiteSchema):
        return await cls.client.post(f"{CRAWL4AI_HOST}/crawl",
            json={
                "urls": urls,
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