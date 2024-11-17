from pydantic import BaseModel
from uuid import UUID 

class BooksRequestBody(BaseModel):
    name: str
    description: str
    number_of_copies: int
    author_id: UUID
