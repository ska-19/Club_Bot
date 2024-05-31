from pydantic import BaseModel


class AddProduct(BaseModel):
    name: str
    price: int
    user_id: int
    description: str
    quantity: int
    club_id: int


class UpdateProduct(BaseModel):
    id: int
    user_id: int
    name: str
    price: int
    description: str
    quantity: int


