from pydantic import BaseModel

class HouseRequest(BaseModel):
    price: float
    website: str