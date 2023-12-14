import os
from loguru import logger as log

from .server import run_server
from .config import Config, DevConfig

from .db import DataBaseController

__version__ = (1,0,0,0)

log.add(
    os.path.join(os.getcwd(), 'logs', '{time:DD-MM-YYYY}.log'), 
    format='{time:HH:mm:ss.SSSZ} | [{level}]\t| {message}'
)
log.critical('='*15 + ' Инициализация Notes_FastAPI_Server v'+".".join(str(x) for x in __version__) + ' ' +'='*15)


async def start():
    try:
        await DataBaseController.create_database()
        await run_server(Config().server, DevConfig().debug_mode)
    except KeyboardInterrupt:
        pass