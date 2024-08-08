from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from ..core.config import settings

engine = create_async_engine(settings.db.ASYNC_DATABASE_URL)
session = async_sessionmaker(bind=engine)


async def get_db():
    async with session() as db:
        yield db


class Base(DeclarativeBase):
    pass


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
