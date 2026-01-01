# schemas.py
from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    year: int
    country: str
    language: str

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    pass