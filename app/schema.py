from pydantic import BaseModel

class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str

class PostCreate(BaseModel):  # For POST endpoint (no ID needed)
    userId: int
    title: str
    body: str
