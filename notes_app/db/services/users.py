from .abc import IService
from ..models.user import UserModel


class UserService(IService[UserModel]):
    ...