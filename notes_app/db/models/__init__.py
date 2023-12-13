
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    ...


# Для хранения версии Б/Д
class MetaData(Base):
    __tablename__ = '__meta__'

    id : Mapped[int] = mapped_column(primary_key=True)
    version : Mapped[int] = mapped_column(default=0)



from .models import *