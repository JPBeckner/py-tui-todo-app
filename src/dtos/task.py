from typing import Optional

from pydantic import Field

from src.dtos.base import BaseDTO
from src.dtos.priority import Priority


class TaskDTO(BaseDTO):
    key: str
    title: str
    description: str
    markdown: str
    due_date: Optional[str]
    # priority: Priority
    completed: bool = Field(default=False)