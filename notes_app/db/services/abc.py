from abc import ABC
from typing import TypeVar, Type, Optional, Generic, List

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar('T')


class IDBService(Generic[T]):
    
    def __init__(self, session : AsyncSession) -> None:
        self.session = session
    
    
    @property
    def model(self) -> Type[T]:
        for base in type(self).__orig_bases__:
            if hasattr(base, '__args__'):
                return base.__args__[0]


    async def commit(self):
        await self.session.commit()


    async def create(self, instance : T, flush : bool = True) -> T:
        self.session.add(instance)
        if flush:
            await self.session.flush()
        
        return instance
    

    async def delete(self, instance : T, flush : bool = False):
        await self.session.delete(instance)
        if flush:
            await self.session.flush()

    
    async def update(self, instance : T, flush : bool = False) -> T:
        await self.session.merge(instance)
        if flush:
            await self.session.flush()
        
        return instance


    async def get_by_id(self, id : int) -> Optional[T]:
        try:
            return (await self.session.scalars(select(self.model).where(self.model.id==id))).one()
        except NoResultFound:
            return None
        # Возможно исключение MultipleResultsFound, но оно явно должно наверх подниматься

    
    async def get_all(self, order_by : bool = False) -> List[T]:
        if order_by:
            return (await self.session.scalars(select(self.model).order_by(self.model.id))).all() 
        
        return (await self.session.scalars(select(self.model))).all()
    