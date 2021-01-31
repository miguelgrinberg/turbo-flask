import uuid


class Todo:
    def __init__(self, task):
        self.id = uuid.uuid4().hex
        self.task = task
        self.completed = False
