import json

from hashlib import sha256


class AuthorizationController():
    SOLD = 'a12hu240h923123hdf'

    def __init__(self):
        ...

    def __get_user_token__(self, email : str, password : str) -> str:
        # Итог 64 символа
        return sha256((email + self.SOLD + password).encode('utf-8')).hexdigest()

    def check_auth(self, email : str, password : str) -> bool:
        user_token = self.__get_user_token__(email, password)
        ...
    
    ...