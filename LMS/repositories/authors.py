from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import insert
from LMS.infra.db.schema import authors
from LMS.exceptions import ModelNotFoundError

@dataclass
class Authors:
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

def get(id: UUID, conn: Connection) -> Authors:
    if result := conn.execute(authors.select().where(authors.c.id == id)).first():
        return Authors(**result._asdict())
    else:
        raise ModelNotFoundError(Authors, id)

def get_all(conn: Connection) -> list[Authors]:
    return [Authors(**author) for author in conn.execute(authors.select()).mappings().fetchall()]

def delete(id: UUID, conn: Connection) -> None:
    conn.execute(authors.delete().where(authors.c.id == get(id, conn).id))

def new(name: str, conn: Connection) -> Authors:
    default_retry_map = conn.execute(insert(authors).values(
        name=name,
    ).returning(authors)).mappings().one()
    return Authors(**default_retry_map)