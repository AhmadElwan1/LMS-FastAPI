from fastapi import APIRouter, status, Request
from uuid import UUID
from LMS.controllers.models.books import BooksRequestBody
from LMS.repositories.books import get, get_all, get_by_author_id, delete, new, Books
from typing import List
from LMS.infra.db.engine import engine

books_router = APIRouter(
    prefix='/books',
    tags=['Books'],
)


@books_router.get("/", response_model=List[Books])
async def get_all_books(r: Request):
    print(">>>>>>>>>>>>", r.headers)
    with engine.connect() as conn:
        books = get_all(conn)
    return books


@books_router.get("/{book_id}", response_model=Books)
async def get_book(book_id: UUID):
    with engine.connect() as conn:
        book = get(book_id, conn)
    return book

@books_router.get("/author/{author_id}", response_model=List[Books])
async def get_books_by_author(author_id: UUID):
    with engine.connect() as conn:
        books = get_by_author_id(author_id, conn)
    return books

@books_router.post("/", response_model=Books)
async def create_book(book: BooksRequestBody):
    with engine.begin() as conn:
        return new(name=book.name, description=book.description, conn=conn)


@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    with engine.begin() as conn:
        delete(book_id, conn)
