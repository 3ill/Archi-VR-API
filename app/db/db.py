from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config.db_config import DBConfig


class Base(DeclarativeBase):
    pass


config = DBConfig()
engine = create_async_engine(config.get_db_url())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@lru_cache(maxsize=1)
def get_worker_engine():
    worker_config = DBConfig()
    return create_async_engine(worker_config.get_db_url(), pool_pre_ping=True)


@lru_cache(maxsize=1)
def get_worker_session_maker():
    return async_sessionmaker(get_worker_engine(), expire_on_commit=False)


async def init_db_and_tables():
    async with engine.begin() as _conn:
        await _conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as _session:
        yield _session
