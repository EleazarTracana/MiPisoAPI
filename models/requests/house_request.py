from pydantic import BaseModel

class HouseRequest(BaseModel):
    price: float
    website: str
    def __init__(self, price, website):
        self.price = price,
        self.website = website