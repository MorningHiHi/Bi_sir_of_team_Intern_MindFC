from pydantic import BaseModel
from typing import Optional
class IDN(BaseModel):
    id:Optional[str]=None
    name:Optional[str]=None
class CreateIDN(BaseModel):
    name:Optional[str]=None
class IdIDN(BaseModel):
    id:Optional[str]=None