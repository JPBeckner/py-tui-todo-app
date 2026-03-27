from uuid import uuid4

from textual.widgets import Input, OptionList
from textual.binding import Binding
from textual import on
from textual.widgets.option_list import Option

from src.adapters.json import JsonAdapter


class TaskLists(OptionList):
    """Task Lists Widget

    :param DataTable: _description_
    :type DataTable: _type_
    """
    BINDINGS = [
        Binding(key="n", action="new", description="New Task List", show=True),
        Binding(key="d", action="delete", description="Delete Task List", show=True),
        Binding(key="j", action="down", description="Scroll down", show=True),
        Binding(key="k", action="up", description="Scroll up", show=True),
        Binding(key="right", action="move_to_tasks", description="->", show=True),
    ]
    
    def __init__(self, *content, name = None, id = None, classes = None, disabled = False, markup = True, compact = False, json_adapter: JsonAdapter = None):
        super().__init__(*content, name=name, id=id, classes=classes, disabled=disabled, markup=markup, compact=compact)
        self.json_adapter = json_adapter

    def on_mount(self):
        self.border_title = "Task Lists"
        # task_lists = self.query_one(TaskLists)
        for task_list in self.json_adapter.get_all_lists():
            option = Option(task_list.name, id=task_list.key)
            self.add_option(option)
            # task_lists.add_option(option=option)

    def show_task_lists(self) -> None:
        for task_list in self.json_adapter.get_all_lists():
            option = Option(task_list.name, id=task_list.key)
            self.add_option(option)

        # tasks = self.screen.query_one("#tasks", Tasks)
        # if self.highlighted_option:
        #     list_key = self.highlighted_option.id
        #     tasks.options = [Option(task.name, id=task.key) for task in self.json_adapter.get_all_tasks(list_key)]

    def action_move_to_tasks(self) -> None:
        self.screen.focus_next()

    def action_new(self) -> None:
        self.app.current_requester = self
        self.screen.query_one("#input").focus()

    def action_delete(self) -> None:
        if self.highlighted_option:
            list_id = self.highlighted_option.id
            self.remove_option(list_id)
            self.json_adapter.remove_list(list_id)

    @on(Input.Submitted, "#input")
    def new_todo(self, event: Input.Submitted) -> None:
        if self.app.current_requester is self:
            task_lists: TaskLists = self.query_one(TaskLists)
            key = str(uuid4())[:8]
            task_lists.add_option(item=Option(event.value, value=key))
            
            self.json_adapter.new_list(key, event.value, description="")
            self.query_one(Input).clear()
            task_lists.focus()

