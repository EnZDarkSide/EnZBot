from datetime import datetime
from typing import List


class SubjTask(object):
    def __init__(self, name=None, status=None, openDate=None, dueDate=None):
        self.name = name
        self.status = status
        self.dueDate = dueDate
        self.openDate = openDate

    def to_str(self):
        text = f'Название: {self.name}\n' \
               f'Статус: {self.status}\n' \
               f'Выдано: {self.openDate}\n' \
               f'Срок сдачи: {self.dueDate}'
        return text


class Subject:
    def __init__(self, name=None, url=None, tasks=[]):
        self.name = name
        self.url = url
        self.tasks = tasks

    def add(self, task: SubjTask):
        self.tasks.append(task)

    def get_by_date_arr(self, dates: list):
        result = []
        for task in self.tasks:
            due_date = datetime.strptime(task.dueDate, "%d.%m.%Y %H:%M").date()
            if due_date in dates:
                result.append(task)

        return result

