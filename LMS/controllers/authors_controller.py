from fastapi import APIRouter, status, Request
from uuid import UUID
from LMS.controllers.models.authors import AuthorsRequestBody
from LMS.repositories.authors import get, get_all, delete, new, Authors
from typing import List
from LMS.infra.db.engine import engine

authors_router = APIRouter(
    prefix='/authors',
    tags=['Authors'],
)


@authors_router.get("/", response_model=List[Authors])
async def get_all_authors(r: Request):
    print(">>>>>>>>>>>>", r.headers)
    with engine.connect() as conn:
        authors = get_all(conn)
    return authors


@authors_router.get("/{author_id}", response_model=Authors)
async def get_author(author_id: UUID):
    with engine.connect() as conn:
        author = get(author_id, conn)
    return author

@authors_router.post("/", response_model=Authors)
async def create_author(author: AuthorsRequestBody):
    with engine.begin() as conn:
        return new(name=author.name, conn=conn)


@authors_router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: UUID):
    with engine.begin() as conn:
        delete(author_id, conn)
