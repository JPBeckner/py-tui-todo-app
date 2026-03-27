from typing import Optional

from src.dtos.base import BaseDTO
from src.dtos.priority import Priority
from src.dtos.task import TaskDTO


class TaskListsDTO(BaseDTO):
    key: str
    name: str
    description: Optional[str]
    tasks: list[TaskDTO]