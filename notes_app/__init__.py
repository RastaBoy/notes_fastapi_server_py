
from .server import run_server
from .config import Config, DevConfig

from .db import Database

__version__ = (1,0,0,0)


async def start():
    try:
        await Database.create_database()
        await run_server(Config().server, DevConfig().debug_mode)
    except KeyboardInterrupt:
        pass