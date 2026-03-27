from textual import on
from textual.widgets import Pretty, SelectionList, TextArea
from textual.binding import Binding

from src.adapters.json import JsonAdapter
from src.dtos.task import TaskDTO
from src.widgets.task_details_viewer import TaskDetailsViewer
from src.widgets.task_details_static import TaskDetailsStatic
from src.widgets.task_details_text import TaskDetailsText
from src.widgets.task_lists import TaskLists


class Tasks(SelectionList):
    
    def __init__(self, 
        *selections, 
        name = None, 
        id = None, 
        classes = None, 
        disabled = False, 
        compact = False, 
        json_adapter: JsonAdapter = None
    ):
        super().__init__(
            *selections, 
            name=name, 
            id=id, 
            classes=classes, 
            disabled=disabled, 
            compact=compact
        )
        self.json_adapter = json_adapter
    
    BINDINGS = [
        Binding(
            key="left", 
            action="move_to_task_lists", 
            description="<-", 
            show=True
        ),
        Binding(
            key="right", 
            action="move_to_task_details", 
            description="->", 
            show=True
        ),
        Binding(
            key="n", 
            action="new", 
            description="New Task", 
            show=True
        ),
        Binding(
            key="d", 
            action="delete", 
            description="Delete Task", 
            show=True
        ),
        Binding(
            key="e", 
            action="expand_task_details", 
            description="Expand Task Details", 
            show=True
        ),
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

        if self.highlighted_option:
            task_id=self.highlighted_option.id
            self.remove_option(task_id)
            list_key = self.screen.query_one(TaskLists).highlighted_option.id
            self.json_adapter.remove_task(list_key, task_id)

    @on(SelectionList.OptionHighlighted)
    async def update_preview(self) -> None:
        task_preview = self.screen.query_one_optional("#task_details_viewer")
        if task_preview:
            await task_preview.remove()
        task_details = self.screen.query_one(
            "#task_details_static", 
            TaskDetailsStatic
        )
        task = self.json_adapter.get_task(
            self.screen.query_one(TaskLists).highlighted_option.id, 
            self.highlighted_option.id
        )
        details = task.description if task else "No description"
        preview = TaskDetailsViewer(details, id="task_details_viewer")
        task_details.mount(preview)

    @on(SelectionList.OptionSelected)
    def update_completed_on_selection(self) -> None:
        list_key = self.screen.query_one(TaskLists).highlighted_option.id
        task_key = self.highlighted_option.id
        task = self.json_adapter.get_task(list_key, task_key)
        if task:
            task.completed = not task.completed
            self.json_adapter.update_task(list_key, task)
            self.refresh()

    def action_expand_task_details(self) -> None:
        if self.highlighted_option:
            list_key = self.screen.query_one(TaskLists).highlighted_option.id
            task_key = self.highlighted_option.id
            task = self.json_adapter.get_task(list_key, task_key)
                
            task_preview = self.screen.query_one_optional(TaskDetailsViewer)
            if task_preview:
                task_preview.remove()
            text = task.description or ""
            detail_text = TaskDetailsText(
                text=text,
                language="markdown",
                id="task_details_text", 
                json_adapter=self.json_adapter
            )

            task_details = self.screen.query_one("#task_details_static")
            task_details.mount(detail_text)
            detail_text.focus()