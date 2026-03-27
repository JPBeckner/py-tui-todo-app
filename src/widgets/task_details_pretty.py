from textual.widgets import Pretty


class TaskDetailsPretty(Pretty):
    def __init__(self, *content, object=None, name = None, id = None, classes = None):
        super().__init__(*content, name=name, id=id, classes=classes)