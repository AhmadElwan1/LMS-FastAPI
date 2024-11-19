from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from sqlalchemy import update
from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import insert
from replace_domain.exceptions import BookAlreadyBorrowedError, BookNotBorrowedError, ModelNotFoundError
from replace_domain.infra.db.schema import books
from replace_domain.repositories.authors import get as get_author


@dataclass
class Books:
    id: UUID
    name: str
    description: str
    number_of_pages: int
    is_borrowed: bool
    author_id: UUID
    created_at: datetime
    updated_at: datetime


def get(id: UUID, conn: Connection) -> Books:
    if result := conn.execute(books.select().where(books.c.id == id)).first():
        return Books(**result._asdict())
    else:
        raise ModelNotFoundError(Books, id)


def get_all(conn: Connection) -> list[Books]:
    return [Books(**book) for book in conn.execute(books.select()).mappings().fetchall()]


def delete(id: UUID, conn: Connection) -> None:
    conn.execute(books.delete().where(books.c.id == get(id, conn).id))


def new(name: str, description: str, number_of_pages: int, author_id: UUID, conn: Connection) -> Books:
    author = get_author(author_id, conn)
    default_retry_map = conn.execute(insert(books).values(
        name=name,
        description=description,
        number_of_pages=number_of_pages,
        is_borrowed=False,
        author_id=author_id,
    ).returning(books)).mappings().one()
    return Books(**default_retry_map)

def get_by_author_id(author_id: UUID, conn: Connection) -> list[Books]:
    results = conn.execute(
        books.select().where(books.c.author_id == author_id)
    ).mappings().fetchall()
    return [Books(**book) for book in results] if results else (_ for _ in ()).throw(ModelNotFoundError(author_id))


def update_book(book_id: UUID, data: dict, conn: Connection) -> dict:
    result = conn.execute(books.select().where(books.c.id == book_id)).first()
    if not result:
        raise ModelNotFoundError(Books, book_id)
    conn.execute(update(books).where(books.c.id == book_id).values(**data))
    updated_result = conn.execute(books.select().where(books.c.id == book_id)).first()
    return dict(updated_result._mapping)

def borrow_book(book_id: UUID, conn: Connection) -> Books:
    book = get(book_id, conn)
    if book.is_borrowed:
        raise BookAlreadyBorrowedError(book_id)
    updated_book = update_book(book_id, {"is_borrowed": True}, conn)
    return Books(**updated_book)

def return_book(book_id: UUID, conn: Connection) -> Books:
    book = get(book_id, conn)
    if not book.is_borrowed:
        raise BookNotBorrowedError(book_id)
    
    updated_book = update_book(book_id, {"is_borrowed": False}, conn)
    return Books(**updated_book)


