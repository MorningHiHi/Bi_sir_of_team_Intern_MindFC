from pydantic import BaseModel
from typing import Optional
from schemas.category_schema import IDN
#from uuid import UUID
class Product(BaseModel):
    id:Optional[str]=None
    name:str
    description:Optional[str]=None
    price:float
    category:IDN