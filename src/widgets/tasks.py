# from textual.widgets import DataTable


# COLUMNS = [
#     ("#", "ToDo", "Completed", "Created"),
# ]


# class Tasks(DataTable):
    
#     def on_mount(self):
#         self.cursor_type = "row"
#         self.add_columns(*COLUMNS[0])

from uuid import uuid4

from textual import on
from textual.selection import Selection
from textual.widgets import Input, SelectionList
from textual.binding import Binding

from src.adapters.json import JsonAdapter
from src.dtos.task import TaskDTO
from src.widgets.task_lists import TaskLists


class Tasks(SelectionList):
    
    def __init__(self, *selections, name = None, id = None, classes = None, disabled = False, compact = False, json_adapter: JsonAdapter = None):
        super().__init__(*selections, name=name, id=id, classes=classes, disabled=disabled, compact=compact)
        self.json_adapter = json_adapter
    
    BINDINGS = [
        Binding(key="left", action="move_to_task_lists", description="<-", show=True),
        Binding(key="right", action="move_to_task_details", description="->", show=True),
        Binding(key="n", action="new", description="New Task", show=True),
        Binding(key="d", action="delete", description="Delete Task", show=True),
    ]
    
    def on_mount(self):
        self.border_title = "Tasks"

    def action_move_to_task_lists(self) -> None:
        self.screen.focus_previous()

    def action_move_to_task_details(self) -> None:
        self.screen.focus_next()

    def action_new(self) -> None:
        self.app.current_requester = self
        self.screen.query_one("#input").focus()

    def action_delete(self) -> None:
        # tasks: Tasks = self.query_one(Tasks)
        # if tasks.cursor_row is not None:
        #     tasks.remove_row(list(tasks.rows.keys())[tasks.cursor_row])

        if self.highlighted_option:
            list_key = self.screen.query_one(TaskLists).highlighted_option.id
            self.remove_option(self.highlighted_option.value)
            self.json_adapter.remove_task(list_key, self.highlighted_option.id)

    # @on(Input.Submitted, "#input")
    # def new_todo(self, event: Input.Submitted) -> None:
    #     if self.app.current_requester is self:
    #         list_key = self.query_one(TaskLists).highlighted_option.id
            
    #         tasks: Tasks = self.query_one(Tasks)
    #         key = f"{list_key}-{str(uuid4())[:8]}"
    #         tasks.add_option(item=Selection(event.value, value=key))
            
    #         self.json_adapter.new_task(list_key, TaskDTO(
    #             key=key,
    #             title=event.value,
    #             description="",
    #             markdown="",
    #             due_date=None,
    #             completed=False
    #         ))
    #         self.query_one(Input).clear()
    #         tasks.focus()

