from datetime import datetime

from pydantic import BaseModel

class AddProduct(BaseModel):
    name: str
    price: int
    description: str
    photo: str
    quantity: int
    rating: int
    club_id: int

class UpdateProduct(BaseModel):
    name: str
    price: int
    description: str
    photo: str
    quantity: int
    rating: int
    club_id: int

