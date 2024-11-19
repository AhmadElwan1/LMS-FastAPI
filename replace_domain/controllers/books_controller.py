from fastapi import APIRouter, HTTPException, status, Request
from uuid import UUID
from replace_domain.controllers.models.books import BookUpdateRequestBody, BooksRequestBody
from replace_domain.exceptions import BookNotFoundError
from replace_domain.repositories.books import get, get_all, get_by_author_id, update_book, borrow_book, return_book, delete, new, Books
from typing import List
from replace_domain.infra.db.engine import engine

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
    try:
        with engine.connect() as conn:
            book = get(book_id, conn)
            return book
    except BookNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= e.message)

@books_router.get("/author/{author_id}", response_model=List[Books])
async def get_books_by_author(author_id: UUID):
    with engine.connect() as conn:
        books = get_by_author_id(author_id, conn)
    return books

@books_router.post("/", response_model=Books)
async def create_book(book: BooksRequestBody):
    with engine.begin() as conn:
        return new(name=book.name, description=book.description, number_of_pages=book.number_of_pages, author_id=book.author_id, conn=conn)


@books_router.patch("/{book_id}", response_model=Books)
async def patch_book(book_id: UUID, update_data: BookUpdateRequestBody):
    with engine.begin() as conn:
        return update_book(book_id, update_data.dict(exclude_unset=True), conn)
    

@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    try:
        with engine.begin() as conn:
            delete(book_id, conn)
    except ModuleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e.msg))

@books_router.post("/{book_id}/borrow", response_model=Books)
async def borrow_book_route(book_id: UUID):
    with engine.begin() as conn:
        return borrow_book(book_id, conn)


@books_router.post("/{book_id}/return", response_model=Books)
async def return_book_route(book_id: UUID):
    with engine.begin() as conn:
        return return_book(book_id, conn)

