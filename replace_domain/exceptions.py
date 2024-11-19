from typing import Any
from uuid import UUID

from pydantic import BaseModel


class ResponseError(BaseModel):
    title: str | None
    detail: str | None


class ModelNotFoundError(Exception):
    def __init__(self, model: type[Any], id: UUID | str) -> None:
        self.model = model.__name__
        self.id = id

class BookNotFoundError(Exception):
    def __init__(self, book_id:UUID):
        self.message = f"Book with ID {book_id} not found."
        super().__init__(self.message)