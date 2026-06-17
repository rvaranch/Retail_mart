from pydantic import BaseModel


class Product(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

class QuantityUpdate(BaseModel):
    quantity: int
