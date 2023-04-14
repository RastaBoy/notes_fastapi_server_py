from fastapi import Response
from fastapi.responses import HTMLResponse

from . import webgui_router
from .models import AuthorizationRequest


@webgui_router.post('/login')
async def login(request : AuthorizationRequest):
    print(request)
    return


