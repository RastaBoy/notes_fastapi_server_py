import os, aiosqlite

from loguru import logger as log
from contextlib import asynccontextmanager
from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .exc import MigrationException
from .models import Base, MetaData
from .services.meta import MetaService


CONNECTION_STRING = 'sqlite+aiosqlite:///database.db'
MIGRATIONS_PATH = os.path.join(os.getcwd(), 'migrations')


class DataBaseController:
    # TODO Не забыть отключить эхо
    _engine = create_async_engine(CONNECTION_STRING, echo=True)
    _session = async_sessionmaker(bind=_engine)

    @staticmethod
    async def __make_mirations__(session : AsyncSession, current_version : int = 0):
            log.info(f"Проверка на наличие обновлений для базы данных. Текущая версия б/д: {current_version}")
            if os.path.isdir(MIGRATIONS_PATH):
                content = os.listdir(MIGRATIONS_PATH)
                for file in content:
                    if os.path.isfile(os.path.join(MIGRATIONS_PATH, file)) and file.endswith('.sql'):
                        # Папка с sql файлами формата *версия*_*название*.sql

                        # TODO Организовать по человечески
                        # ----------------
                        migration_version, migration_name = int(file.split('_')[0]), file.split('_')[1]
                        # ----------------
                        if current_version < migration_version:
                            try:
                                log.info(f"Осуществление миграции \"{migration_name}\". Обновление на версию {migration_version}.")
                                with open(os.path.join(MIGRATIONS_PATH, file), 'r') as f:
                                    for query in f.readlines():
                                        await session.execute(query)
                                await session.commit()
                                log.info(f"Миграция прошла успешно.")
                            except Exception as e:
                                log.exception(f"В ходе выполнения миграций при выполнении команды {query} возникло исключение \"{e.__class__.__name__}\": {e}")
                                raise MigrationException(f"В ходе выполнения миграции \"{migration_name}\", при выполнении команды {query} возникло исключение \"{e.__class__.__name__}\": {e}")
                                

    @staticmethod
    async def __get_version__(session : AsyncSession) -> int:
        meta_service = MetaService(session)
        meta = await meta_service.get_by_id(0)
        if meta is None:
            await meta_service.create(MetaData(version=0))
            return 0

        return meta.version



    @staticmethod
    async def create_database():
        async with DataBaseController._engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            async with DataBaseController.get_session() as session:
                db_version = await DataBaseController.__get_version__(session)
                await DataBaseController.__make_mirations__(session, db_version)


    @staticmethod
    @asynccontextmanager
    async def get_session() -> AsyncSession:
            async with DataBaseController._session.begin() as session:
                yield session    
                


from .models import *