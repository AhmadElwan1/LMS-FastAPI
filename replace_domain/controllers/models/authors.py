from pydantic import BaseModel

class AuthorsRequestBody(BaseModel):
    name: str
