from contextlib import asynccontextmanager
from asyncio import current_task
from loguru import logger

from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession  


DeclarativeBase = declarative_base()

__CONNSTRING__ = 'sqlite+aiosqlite:///database.db'

class Database:

    _engine = create_async_engine(__CONNSTRING__, echo=False)
    _session_factory = async_scoped_session(
        orm.sessionmaker(_engine, class_=AsyncSession),
        scopefunc=current_task
    )


    @staticmethod
    async def create_database():
        # DeclarativeBase.metadata.drop_all(Database._engine)
        # DeclarativeBase.metadata.create_all(Database._engine)
        async with Database._engine.begin() as conn:
            await conn.run_sync(DeclarativeBase.metadata.create_all)
    
    @staticmethod
    @asynccontextmanager
    async def session(old_session:AsyncSession = None) -> AsyncSession:
        if old_session is None:
            session: AsyncSession = Database._session_factory()
        else:
            session: AsyncSession = old_session
            
        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            await session.rollback()
            raise
        else:
            await session.commit()
        finally:
            await session.close()

    
from .models import *