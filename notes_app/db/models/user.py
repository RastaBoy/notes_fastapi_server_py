from sqlalchemy import Column, String, DateTime as SQLDateTime, ForeignKey, Integer, Enum as SQLEnum, Boolean, Date as SQLDate
from sqlalchemy.orm import relationship

from .. import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_token = Column(String(length=64), nullable=False)
    nickname = Column(String(length=256), default="")

    tasks = relationship('TaskModel', back_populates='user')
