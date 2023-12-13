from .abc import IDBService
from ..models import MetaData


class MetaService(IDBService[MetaData]):
    ...