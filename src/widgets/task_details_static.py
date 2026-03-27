from textual.binding import Binding
from textual.widgets import Static, TextArea


class TaskDetailsStatic(Static):
    BINDINGS = [
        Binding(key="left", action="move_to_tasks", description="<-", show=True),
    ]
    def on_mount(self, event):
        self.border_title = "Task Details"
        self.update("")
