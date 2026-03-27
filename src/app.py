from uuid import uuid4

from textual.app import App, ComposeResult, on
from textual.binding import Binding
from textual.widgets import (
    Header,
    Footer,
    Input,
    OptionList
)
from textual.widgets.selection_list import Selection
from textual.widgets.option_list import Option

from src.adapters.json import JsonAdapter
from src.dtos.task import TaskDTO
from src.widgets import Tasks, TaskDetails, TaskLists





class ToDoApp(App):
    CSS_PATH = "style/grid_layout.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
        Binding(key="j", action="down", description="Scroll down", show=True),
        Binding(key="k", action="up", description="Scroll up", show=True),
        Binding(key="enter", action="select", description="Select", show=True),
    ]

    def __init__(self, json_adapter: JsonAdapter, *args, **kwargs):
        self.json_adapter = json_adapter
        super().__init__(*args, **kwargs)
        self.current_requester = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TaskLists(classes="box", json_adapter=self.json_adapter)
        yield Tasks(classes="box", json_adapter=self.json_adapter)
        yield TaskDetails("", classes="box", id="task_details")
        yield Input(placeholder="todo ...", classes="input", id="input")

    def on_mount(self) -> None:
        self.title = "ToDo App"

    @on(Input.Submitted, "#input")
    def new_item(self, event: Input.Submitted) -> None:
        if isinstance(self.app.current_requester, Tasks):
            list_key = self.query_one(TaskLists).highlighted_option.id

            tasks: Tasks = self.query_one(Tasks)
            key = f"{list_key}-{str(uuid4())[:8]}"
            tasks.add_option(item=Selection(event.value, value=key))

            self.json_adapter.new_task(list_key, TaskDTO(
                key=key,
                title=event.value,
                description="",
                markdown="",
                due_date=None,
                completed=False
            ))
            self.query_one(Input).clear()
            tasks.focus()
        if isinstance(self.app.current_requester, TaskLists):
            task_lists: TaskLists = self.query_one(TaskLists)
            key = str(uuid4())[:8]
            task_lists.add_option(option=Option(event.value, id=key))

            self.json_adapter.new_list(key, event.value, description="")
            self.query_one(Input).clear()
            task_lists.focus()

    @on(TaskLists.OptionHighlighted)
    def update_tasks(self, event: TaskLists.OptionHighlighted) -> None:
        tasks_widget: Tasks = self.query_one(Tasks)
        tasks_widget.clear_options()
        task_lists: TaskLists = self.query_one(TaskLists)
        tasks = self.json_adapter.get_all_tasks(event.option.id)
        for task in tasks:
            tasks_widget.add_option(item=Selection(task.title, value=task.key, id=task.key))
        task_lists.focus()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.query_one(Tasks).focus()

# EOF