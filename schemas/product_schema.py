from pydantic import BaseModel
from typing import Optional
from schemas.category_schema import IDN
class Product(BaseModel):
    id:Optional[str]=None
    name:str
    description:Optional[str]=None
    price:float
    category:IDN