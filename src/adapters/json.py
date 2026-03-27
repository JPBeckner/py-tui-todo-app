import json

from src.dtos.task import TaskDTO
from src.dtos.task_lists import TaskListsDTO


def _load(file_path) -> list[TaskListsDTO]:
    with open(file_path, "r") as f:
            data = json.load(f)
            return [TaskListsDTO.model_validate(task_list) for task_list in data]


class JsonAdapter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.task_lists: list[TaskListsDTO] = []
        self.load()

    def load(self) -> list[TaskListsDTO]:
        with open(self.file_path, "r") as f:
            data = json.load(f)
            self.task_lists = [TaskListsDTO.model_validate(task_list) for task_list in data]


    def save(self, task_lists: list[TaskListsDTO]):
        with open(self.file_path, "w") as f:
            json.dump([task_list.model_dump() for task_list in task_lists], f, indent=4)

    def init(self):
        # Initialize the JSON file with an empty list if it doesn't exist
        try:
            with open(self.file_path, "x") as f:
                json.dump([], f)
        except FileExistsError:
            pass

    def new_list(self, key: str, name: str, description: str = ""):
        self.load()
        new_task_list = TaskListsDTO(key=key, name=name, description=description, tasks=[])
        self.task_lists.append(new_task_list)
        self.save(self.task_lists)

    def get_all_lists(self) -> list[TaskListsDTO]:
        self.load()
        return self.task_lists

    def get_list(self, key: str) -> TaskListsDTO | None:
        self.load()
        for task_list in self.task_lists:
            if task_list.key == key:
                return task_list
        return None

    def update_list(self, updated_list: TaskListsDTO):
        self.load()
        for i, task_list in enumerate(self.task_lists):
            if task_list.key == updated_list.key:
                self.task_lists[i] = updated_list
                self.save(self.task_lists)
                return

    def remove_list(self, key: str):
        self.load()
        self.task_lists = [task_list for task_list in self.task_lists if task_list.key != key]
        self.save(self.task_lists)

    def new_task(self, list_key: str, task: TaskDTO):
        self.load()
        for task_list in self.task_lists:
            if task_list.key == list_key:
                task_list.tasks.append(task)
                self.save(self.task_lists)
                return

    def remove_task(self, list_key: str, task_key: str):
        self.load()
        for task_list in self.task_lists:
            if task_list.key == list_key:
                task_list.tasks = [task for task in task_list.tasks if task.key != task_key]
                self.save(self.task_lists)
                return

    def update_task(self, list_key: str, updated_task: TaskDTO):
        self.load()
        for task_list in self.task_lists:
            if task_list.key == list_key:
                for i, task in enumerate(task_list.tasks):
                    if task.key == updated_task.key:
                        task_list.tasks[i] = updated_task
                        self.save(self.task_lists)
                        return

    def get_all_tasks(self, list_key: str) -> list[TaskDTO] | list:
        self.load()
        for task_list in self.task_lists:
            if task_list.key == list_key:
                return task_list.tasks
        return []