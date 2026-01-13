from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema import Post, PostCreate
from app.db import create_db, Post as PostModel, get_async_session
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/posts")
async def get_all_posts(
    userId: int | None = None,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = select(PostModel)
    if userId:
        stmt = stmt.where(PostModel.userId == userId)
    
    result = await session.execute(stmt)
    db_posts = result.scalars().all()
    
    if not db_posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return db_posts

@app.get("/post/{post_id}")
async def get_post_by_id(
    post_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.get(PostModel, post_id)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")
    return result

@app.post("/post", status_code=201)
async def create_new_post(
    new_post: PostCreate,
    session: AsyncSession = Depends(get_async_session)
):
    # Auto-generate ID via autoincrement, no conflict check needed
    db_post = PostModel(**new_post.model_dump())
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post
