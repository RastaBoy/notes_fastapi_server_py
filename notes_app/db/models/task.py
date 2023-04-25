
from sqlalchemy import Column, String, DateTime as SQLDateTime, ForeignKey, Integer, Enum as SQLEnum, Boolean, Date as SQLDate
from sqlalchemy.orm import relationship

from .. import Base

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    title = Column(String(length=256))
    text = Column(String, default="")

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('UserModel', uselist=False)
