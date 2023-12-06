
from sqlalchemy.orm import Mapped, mapped_column

from .. import Base

# Для хранения версии Б/Д
class MetaData(Base):
    id : Mapped[int] = mapped_column(primary_key=True)
    version : Mapped[int] = mapped_column(default=0)

