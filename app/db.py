# from collections.abc import AsyncGenerator
# import uuid

# from sqlalchemy import Column,String,Text,DateTime,ForeignKey
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker
# from sqlalchemy.orm import DeclarativeBase,relationship
# from datetime import datetime, timezone # Import the class and timezone
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# # 1. Define a Base class first
# class Base(DeclarativeBase):
#     pass

# class Post(Base):
#     __tablename__="post"

#     id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
#     caption = Column(Text)
#     url = Column(String,nullable=False)
#     file_type = Column(String,nullable=False)
#     file_name = Column(String,nullable=False)
#     created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# # creating the engine which create the database and tables

# engine = create_async_engine(DATABASE_URL)
# async_session_maker = async_sessionmaker(engine,expire_on_commit=False)

# # this funcation creates the database + tables
# async def create_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# #  this helps to connect with the database and intract with it to
# async def get_async_sesssion() -> AsyncGenerator[AsyncSession,None]:
#     async with async_session_maker() as session :
#         yield session


from collections.abc import AsyncGenerator
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "posts_db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ADMIN_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/"
class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Engines
admin_engine = create_async_engine(ADMIN_URL, isolation_level="AUTOCOMMIT")
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db():
    # 1. Create DB if not exists
    async with admin_engine.begin() as conn:
        try:
            await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"✅ Created DB: {DB_NAME}")
        except ProgrammingError:
            print(f"ℹ️ DB {DB_NAME} already exists")
    
    # 2. Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Created tables")

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
