from textual.widgets import TextArea
from textual.binding import Binding

# from src.widgets.task_details_static import TaskDetailsStatic
# from src.widgets.tasks import Tasks
# from src.widgets.task_lists import TaskLists
from src.adapters.json import JsonAdapter
# from src.widgets.tasks import Tasks


class TaskDetailsText(TextArea):

    BINDINGS = [
        Binding(key="left", action="move_to_tasks", description="<-", show=True),
        Binding(key="escape", action="close_details_text", description="Close Details", show=True),
        Binding(key="ctrl+s", action="save_details", description="Save Details", show=True),
    ]


    def __init__(
        self, 
        *content, 
        name = None, 
        id = None, 
        classes = None, 
        disabled = False, 
        compact = False, 
        language: str = "markdown", 
        theme: str = "css",
        json_adapter: JsonAdapter,
        **kwargs
    ):
        super().__init__(
            *content, 
            name=name, 
            id=id, 
            classes=classes, 
            disabled=disabled, 
            compact=compact, 
            language=language,
            theme=theme,
            **kwargs
        )
        self.json_adapter = json_adapter

    def action_move_to_tasks(self) -> None:
        self.screen.focus_previous()

    def action_close_details(self) -> None:
        self.remove()

    def action_save_details(self) -> None:
        task_key = self.screen.query_one("#tasks").highlighted_option.id
        list_key = self.screen.query_one("#task_lists").highlighted_option.id
        self.json_adapter.update_task_description(list_key, task_key, self.text)

    def close_details_text(self):
        self.screen.query_one("#task_details_text").remove()
        tasks = self.screen.query_one("#tasks")
        tasks.focus()
        tasks.update_preview()