from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .abc import IDBService
from ..models.models import User


class UserService(IDBService[User]):
    async def get_by_email(self, email : str) -> Optional[User]:
        try:
            return (await self.session.scalars(select(self.model).where(self.model.email==email))).one()
        except NoResultFound:
            return None