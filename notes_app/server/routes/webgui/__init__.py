from fastapi import APIRouter

webgui_router = APIRouter(
    prefix='/gui',
    tags=['webgui']
)

from .auth import *