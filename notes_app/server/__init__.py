import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from starlette.responses import FileResponse

from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperConfig

from .routes.webgui import api_router

from ..config import ServerSettings
from ..controllers.authentication.exc import AuthenticationException

STATIC_FOLDER_PATH = os.path.join(os.getcwd(), 'static')

def build_app(debug : bool = False) -> FastAPI:
    app = FastAPI(debug=debug)
    app.include_router(
        router=api_router
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:8080"
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )


    @app.exception_handler(Exception)
    async def base_exceptions(request : Request, exc : Exception):
        # TODO Похоже на кашу с самоповторами, нужно переделать
        if type(exc) in (RequestValidationError, ):
            return JSONResponse(
                status_code=400,
                content={
                    'error_class' : exc.__class__.__name__,
                    'message' : str(exc)
                }
            )
        
        if isinstance(exc, AuthenticationException):
            return JSONResponse(
                status_code=401,
                content={
                    'error_class' : exc.__class__.__name__,
                    'message' : str(exc)
                }
            )

        return JSONResponse(
            status_code=500,
            content={
                'error_class' : exc.__class__.__name__,
                'message' : str(exc)
            }
        )



    @app.get('/{path:path}')
    async def index(path : str):
        # Похоже на костыль, наверняка это должно как-то по-другому делаться
        if not '.' in path:
            return FileResponse(os.path.join(STATIC_FOLDER_PATH, 'index.html'))
        else:
            return FileResponse(os.path.join(STATIC_FOLDER_PATH, *path.split('/')))


    return app


async def run_server(settings : ServerSettings, debug_mode : bool = False):
    cfg = HyperConfig()
    cfg.bind = f'0.0.0.0:{settings.port}'
    cfg.debug = debug_mode

    return await serve(build_app(debug_mode), cfg)