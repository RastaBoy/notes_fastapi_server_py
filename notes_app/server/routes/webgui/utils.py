from fastapi import Request
from typing import Awaitable

from ....controllers.authentication import AuthenticationController
from ....controllers.authentication.exc import AuthenticationException


def auth_required(func : Awaitable):
    async def wrapper(request : Request, *args, **kwargs):
        if request.headers.get('user_token') is None:
            raise AuthenticationException(f"Для выполнения данной операции пользователь должен быть авторизован.")
        # Здесь можно играться, но на текущий момент достаточно просто передачи JWT-токена
        AuthenticationController.get_email_from_jwt(request.headers.get('user_token'))
        return await func(request, *args, **kwargs)
        
    return wrapper