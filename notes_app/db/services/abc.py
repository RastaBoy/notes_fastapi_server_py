from abc import ABC
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from typing import Iterable, Generic, TypeVar, Type
from functools import lru_cache


T = TypeVar('T')


class IService(Generic[T]):

    def __init__(self, session : AsyncSession) -> None:
        self.session = session


    @property
    @lru_cache(maxsize=None)
    def model(self) -> Type[T]:
        for base in type(self).__orig_bases__:
            if hasattr(base, '__args__'):
                return base.__args__[0]
    

    async def commit(self):
        await self.session.commit()


    async def create(self, instance: T, flush : bool = True) -> T:
        self.session.add(instance)
        if flush:
            await self.session.flush()

        return instance


    async def delete(self, instance: T, flush : bool = False):
        await self.session.delete(instance)
        if flush:
            await self.session.flush()
    

    async def update(self, instance: T, flush : bool = True) -> T:
        instance = await self.session.merge(instance)
        if flush:
            await self.session.flush()
        return instance
    

    async def get_by_id(self, id: int) -> Optional[T]:
        try:
            return (await self.session.scalars(select(self.model).where(self.model.id == id))).one()
        except NoResultFound:
            return None
    
    async def get_last(self) -> Optional[T]:
        return (await self.session.scalars(select(self.model).order_by(self.model.id.desc()))).first()


    async def get_all(self, order_by : bool = False) -> Iterable[T]:
        if order_by:
            return (await self.session.scalars(select(self.model).order_by(self.model.id))).all()

        return (await self.session.scalars(select(self.model))).all()