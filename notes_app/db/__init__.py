import os

from loguru import logger as log

from contextlib import asynccontextmanager
from typing import Optional

from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession, async_sessionmaker


__CONNECTION_STRING__ = 'sqlite+aiosqlite://database.db'
__MIGRATIONS_PATH = os.path.join(os.getcwd(), 'migrations')

class Base(DeclarativeBase):
    ...


class DataBaseController:
    # TODO Не забыть отключить эхо
    _engine = create_async_engine(__CONNECTION_STRING__, echo=True)
    _session = async_sessionmaker(bind=_engine)

    @staticmethod
    async def __make_mirations__(session : AsyncSession):
        if os.path.isdir(__MIGRATIONS_PATH):
            content = os.listdir(__MIGRATIONS_PATH)
            for file in content:
                if os.path.isfile(os.path.join(__MIGRATIONS_PATH, file)) and file.endswith('.sql'):
                    # TODO нужно будет придумать механизм миграции
                    # Папка с sql файлами формата *версия*_*название*.sql 
                    ...

    @staticmethod
    async def create_database():
        async with DataBaseController._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all())
            async with DataBaseController.get_session() as session:
                await DataBaseController.__make_mirations__(session)


    @staticmethod
    @asynccontextmanager
    async def get_session(old_session : AsyncSession = None) -> AsyncSession:
        current_session : Optional[AsyncSession] = None
        if old_session is None:
            current_session : AsyncSession = DataBaseController._session.begin()
        else:
            current_session = old_session
        
        try:
            yield current_session
        except Exception as e:
            log.exception(f"Откат сессии в связи с исключением \"{e.__class__.__name__}\": {str(e)}")
            await current_session.rollback()
        finally:
            await current_session.commit()

from .models import *