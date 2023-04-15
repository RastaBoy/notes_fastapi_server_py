from fastapi import Response
from fastapi.responses import HTMLResponse, JSONResponse

from . import api_router
from .models import AuthorizationRequest


@api_router.post('/login')
async def login(request : AuthorizationRequest):
    print(request)
    return JSONResponse("{}")


