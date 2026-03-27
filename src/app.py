from datetime import datetime
from uuid import uuid4

from textual.app import App, ComposeResult, on
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from textual.widgets import (
    Header,
    Footer,
    Input,
    DataTable,
    SelectionList,
    OptionList
)
from textual.events import Key, Mount
from textual.widgets.data_table import DuplicateKey
from textual.widgets.selection_list import Selection
from textual.widgets.option_list import Option

from src.adapters.json import JsonAdapter
from src.dtos.task import TaskDTO
from src.widgets import Tasks, TaskDetails, TaskLists
from src.dtos.priority import Priority





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
        # Binding(key="n", action="new", description="New ToDo", show=True),
        # Binding(key="d", action="delete", description="Delete ToDo", show=True),
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
        yield TaskDetails([], classes="box")
        yield Input(placeholder="todo ...", classes="input", id="input")
        # yield Footer()
        # with Horizontal():
        #     with Vertical():
        #         yield TaskLists()
        #         yield Tasks()
        #         yield TaskDetails()
        # with Horizontal():
        #     yield Input(placeholder="todo ...", classes="input", id="input")

    def on_mount(self) -> None:
        self.title = "ToDo App"
        # task_lists = self.query_one(TaskLists)
        # for task_list in self.json_adapter.get_all_lists():
        #     option = Option(task_list.name, id=task_list.key)
        #     task_lists.add_option(option=option)
        # self.tasks: Tasks = self.query_one(Tasks)
        # self.sub_title = ""
        # self.task_list = self.query_one(TaskLists)
        # self.table.cursor_type = "row"
        # self.table.add_columns(*COLUMNS[0])

    # def action_new(self) -> None:
    #     self.query_one(Input).focus()
        # tasks: Tasks = self.query_one(Tasks)
        # key = len(tasks.rows.keys()) + 1
        # tasks.add_row(
        #     "1", "new todo", "X", datetime.now().strftime("%d/%m/%Y"),
        #     key=key
        # )
        # self.query_one(Input).focus()

    # @on(Key)
    # def keys(self, event):
    #     if event.key in ["n"]:
    #         self.query_one(Input).focus()

    # @on(Input.Submitted)
    # def new_todo(self, event: Input.Changed) -> None:
    #     a = self._last_focused_on_app_blur
    #     # self.screen.blur
    #     # tasks: Tasks = self.query_one(Tasks)
    #     # try:
    #     #     key = str(uuid4())[:8]
    #     #     tasks.add_row(
    #     #         key, event.value, "X", datetime.now().strftime("%d/%m/%Y"),
    #     #         key=key
    #     #     )
    #     # except DuplicateKey:
    #     #     key = str(uuid4())[:8]
    #     #     tasks.add_row(
    #     #         key, event.value, "X", datetime.now().strftime("%d/%m/%Y"),
    #     #         key=key
    #     #     )
    #     # self.query_one(Input).clear()
    #     # tasks.focus()
    #     self.screen.previous_focused
    #     list_key = self.query_one(TaskLists).highlighted_option.id

    #     tasks: Tasks = self.query_one(Tasks)
    #     key = f"{list_key}-{str(uuid4())[:8]}"
    #     tasks.add_option(item=Selection(event.value, value=key))

    #     self.json_adapter.new_task(list_key, TaskDTO(
    #         key=key,
    #         title=event.value,
    #         description="",
    #         markdown="",
    #         due_date=None,
    #         # priority=Priority.LOW,
    #         completed=False
    #     ))
    #     self.query_one(Input).clear()
    #     tasks.focus()

    # @on(Mount)
    # @on(SelectionList.SelectedChanged)
    # def update_selected_view(self) -> None:
    #     self.query_one().update(self.query_one(SelectionList).selected)

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

    # def delete_item(self) -> None:
    #     if isinstance(self.app.current_requester, Tasks):
    #         tasks: Tasks = self.query_one(Tasks)
    #         if tasks.cursor_row is not None:
    #             tasks.remove_row(list(tasks.rows.keys())[tasks.cursor_row])
    #     if isinstance(self.app.current_requester, TaskLists):
    #         task_lists: TaskLists = self.query_one(TaskLists)
    #         if task_lists.cursor_row is not None:
    #             task_lists.remove_option(list(task_lists.options.keys())[task_lists.cursor_row])


    # @on(Mount)
    @on(TaskLists.OptionHighlighted)
    def update_tasks(self, event: TaskLists.OptionHighlighted) -> None:
        tasks_widget: Tasks = self.query_one(Tasks)
        tasks_widget.clear_options()
        task_lists: TaskLists = self.query_one(TaskLists)
        tasks = self.json_adapter.get_all_tasks(event.option.id)
        for task in tasks:
            tasks_widget.add_option(item=Selection(task.title, value=task.key, id=task.key))
        task_lists.focus()

    # def action_delete(self) -> None:
    #     tasks: Tasks = self.query_one(Tasks)
    #     if tasks.cursor_row is not None:
    #         tasks.remove_row(list(tasks.rows.keys())[tasks.cursor_row])

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.query_one(Tasks).focus()

# EOF