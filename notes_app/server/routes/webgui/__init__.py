from fastapi import APIRouter

api_router = APIRouter(
    prefix='/api/v1',
    tags=['api']
)

from .auth import *