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
        self.message = f"{self.model} with ID {self.id} not found."
        super().__init__(self.message)

class BookAlreadyBorrowedError(Exception):
    def __init__(self, book_id: UUID):
        self.book_id = book_id
        self.message = f"Book with ID {book_id} is already borrowed."
        super().__init__(self.message)

class BookNotBorrowedError(Exception):
    def __init__(self, book_id: UUID):
        self.book_id = book_id
        self.message = f"Book with ID {book_id} is not borrowed."
        super().__init__(self.message)
