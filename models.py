from typing import Optional
from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    year: int
    pages: Optional[int] = None
    isbn: Optional[str] = None
