import json, jwt
from hashlib import sha256

from .dto import AuthRequest, RegisterRequest
from .exc import UserNotFound, AuthenticationException

from ...db.services.user import UserService, User


class AuthenticationController():
    '''

    Тащемта концепт должен быть простой:
    1. -- Авторизация --
    2. -- Регистрация --

    '''

    SOLD = '4jzTUlVrvVWl9s2qTMmDt2HaOlv4qkPR'

    @staticmethod
    def get_email_from_jwt(user_token : str) -> str:
        payload : dict = jwt.decode(
            user_token,
            "secret",
            "HS256"
        )
        if payload.get('email') is None:
            raise AuthenticationException('Некорректный токен пользователя.')
        
        return payload['email']

    def __init__(self, user_service : UserService):
        self.user_service = user_service
        

    def __get_user_hash__(self, email : str, password : str) -> str:
        # Итог 64 символа
        return sha256((email + self.SOLD + password).encode('utf-8')).hexdigest()


    def get_user_jwt_token(self, email : str, hash : str) -> str:
        return jwt.encode(
            payload={
                'email' : email,
                'password' : hash
            },
            key='secret',
            algorithm='HS256'
        )




    async def login(self, request : AuthRequest) -> str:
        user_hash = self.__get_user_hash__(
            request.email,
            request.password
        )
        user_model = await self.user_service.get_by_email(request.email)
        if user_model is None:
            raise UserNotFound(f"Пользователь с email \"{request.email}\" не зарегистрирован в системе.")
        
        if user_model.hash != user_hash:
            raise AuthenticationException(f"Неверно указаны email/пароль.")
        
        return self.get_user_jwt_token(
            user_model.email,
            user_model.hash
        )
    

    async def register(self, request : RegisterRequest) -> str:
        user = await self.user_service.get_by_email(request.email)
        if user is not None:
            raise AuthenticationException(f"Пользователь с email \"{request.email}\" уже существует в системе.")
        
        # Пока будем добавлять всех подряд просто так
        user_model = await self.user_service.create(
            User(
                email=request.email,
                first_name=request.first_name,
                second_name=request.second_name,
                hash=self.__get_user_hash__(
                    request.email,
                    request.password
                )
            )
        )

        return self.get_user_jwt_token(
            user_model.email,
            user_model.hash
        )
            