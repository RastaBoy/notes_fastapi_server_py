
from .server import run_server
from .config import Config, DevConfig

__version__ = (1,0,0,0)

async def start():
    try:
        await run_server(Config().server, DevConfig().debug_mode)
    except KeyboardInterrupt:
        pass