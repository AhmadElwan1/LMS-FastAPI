from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import insert
from LMS.infra.db.schema import books
from LMS.exceptions import ModelNotFoundError


@dataclass
class Books:
    id: UUID
    name: str
    description: str
    number_of_copies: int
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


def new(name: str, description: str, number_of_copies: int, author_id: UUID, conn: Connection) -> Books:
    default_retry_map = conn.execute(insert(books).values(
        name=name,
        description=description,
        number_of_copies=number_of_copies,
        author_id=author_id,
    ).returning(books)).mappings().one()
    return Books(**default_retry_map)

def get_by_author_id(author_id: UUID, conn: Connection) -> list[Books]:
    return [Books(**book) for book in conn.execute(
        books.select().where(books.c.author_id == author_id)).mappings().fetchall()]
