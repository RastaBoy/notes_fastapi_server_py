from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True)
    first_name : Mapped[str] = mapped_column(default='')
    second_name : Mapped[str] = mapped_column(default='')
    email : Mapped[str] = mapped_column(nullable=False)
    hash : Mapped[str] = mapped_column(nullable=False)

    dt_create : Mapped[datetime] = mapped_column(default=datetime.now())

    user_notes : Mapped[List['Note']] = relationship(back_populates='creator')


class Note(Base):
    __tablename__ = 'notes'

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(nullable=False)
    content : Mapped[str] = mapped_column(nullable=False)

    dt_create : Mapped[datetime] = mapped_column(default=datetime.now())
    dt_update : Mapped[datetime] = mapped_column(default=datetime.now())

    creator_id : Mapped[int] = mapped_column(ForeignKey('users.id'))
    creator : Mapped[User] = relationship(back_populates='user_notes')
