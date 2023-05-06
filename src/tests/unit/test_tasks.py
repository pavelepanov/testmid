import pytest
from src.tasks.tasks import make_operation, celery


class TestPostData:
    async def test_make_operation(self):
        task = make_operation.delay(1, 2, "+")
        task = task.id
        assert isinstance(task, str) == isinstance("fadsfsdf", str)

    async def test_calculate(self, create_task):
        print(type(create_task))
        task = celery.AsyncResult(create_task).info
        if task[2] == "+":
            assert task[0] + task[1] == 3
        if task[2] == "-":
            return task[0] - task[1]
        if task[2] == "/":
            return task[0] / task[1]
        if task[2] == "*":
            return task[0] * task[1]
