from pydantic import BaseModel


# 2. Define your Data Model
class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str