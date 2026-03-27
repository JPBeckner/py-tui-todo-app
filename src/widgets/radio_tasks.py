from textual.widgets import DataTable


COLUMNS = [
    ("#", "ToDo", "Completed", "Created"),
]


class Tasks(DataTable):
    
    def on_mount(self):
        self.cursor_type = "row"
        self.add_columns(*COLUMNS[0])
    