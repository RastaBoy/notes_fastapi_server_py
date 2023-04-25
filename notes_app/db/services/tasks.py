from .abc import IService
from ..models.task import TaskModel


class TaskService(IService[TaskModel]):
    ...