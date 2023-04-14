import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.responses import FileResponse

from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperConfig

from .routes.webgui import webgui_router

from ..config import ServerSettings


def build_app(debug : bool = False) -> FastAPI:
    app = FastAPI(debug=debug)
    app.include_router(
        router=webgui_router
    )

    @app.get('/{path:path}')
    async def index(path : str):
        # Похоже на костыль, наверняка это должно как-то по-другому делаться
        if not '.' in path:
            return FileResponse(os.path.join(os.getcwd(), 'ui', 'index.html'))
        else:
            return FileResponse(os.path.join(os.getcwd(), 'ui', *path.split('/')))


    return app


async def run_server(settings : ServerSettings, debug_mode : bool = False):
    cfg = HyperConfig()
    cfg.bind = f'0.0.0.0:{settings.port}'
    cfg.debug = debug_mode

    return await serve(build_app(debug_mode), cfg)