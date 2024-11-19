from typing import Optional
from pydantic import BaseModel
from uuid import UUID 

class BooksRequestBody(BaseModel):
    name: str
    description: str
    number_of_pages: int
    author_id: UUID

class BookUpdateRequestBody(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    number_of_pages: Optional[int] = None
    is_borrowed: Optional[bool] = None
    author_id: Optional[UUID] = None