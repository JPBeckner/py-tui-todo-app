from textual.binding import Binding
from textual.widgets import Pretty

class TaskDetails(Pretty):

    BINDINGS = [
        Binding(key="left", action="move_to_tasks", description="<-", show=True),
    ]

    def on_mount(self, event):
        self.border_title = "Task Details"
        self.update("Select a task to see details")

    def action_move_to_tasks(self) -> None:
        self.screen.focus_previous()