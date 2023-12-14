
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse

from . import api_router

from ....db import DataBaseController
from ....db.services.user import UserService

from ....controllers.authentication import AuthenticationController
from ....controllers.authentication.dto import AuthRequest, RegisterRequest


@api_router.post('/login')
async def login(request : AuthRequest):
    async with DataBaseController.get_session() as session:
        user_token = await AuthenticationController(UserService(session)).login(request)
        return JSONResponse(
            status_code=200, 
            content={
                "user_token" : user_token
            }
        )


@api_router.post('/register')
async def register(request : RegisterRequest):
    async with DataBaseController.get_session() as session:
        user_token = await AuthenticationController(UserService(session)).register(request)
        return JSONResponse(
            status_code=200,
            content={
                'user_token' : user_token
            }
        )