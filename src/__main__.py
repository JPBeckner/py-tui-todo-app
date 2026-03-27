import json

from src.adapters.json import JsonAdapter
from src.app import ToDoApp
from src.dtos.task_lists import TaskListsDTO
from src.dtos.task import TaskDTO


app = ToDoApp(
    json_adapter=JsonAdapter("tasks.json")
)


def load_data():
    with open("tasks.json", "r") as f:
        data = json.load(f)
        task_lists: list[TaskListsDTO] = [TaskListsDTO.model_validate(task_list) for task_list in data]
        return task_lists


if __name__ == "__main__":
    app.run()

# EOF