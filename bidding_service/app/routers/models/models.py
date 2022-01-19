from pydantic import BaseModel
from typing import List, Optional


class ProductModel(BaseModel):
    name: str
    description: str
    img_path: str
    price: float
    seller_id: Optional[int]

    class Config:
        orm_mode: True


class QuestionModel(BaseModel):
    product_id: int
    question: str
# class Product(BaseModel):
#     id: int
#     is_active: bool
#     is_deleted: bool
#     first_name: str
#     last_name: str
#     email: str
