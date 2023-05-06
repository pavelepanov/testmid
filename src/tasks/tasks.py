from celery import Celery
from config import REDIS_HOST, REDIS_PORT

import time
from database import redis_client

celery = Celery("tasks", broker=f"redis://{REDIS_HOST}:{REDIS_PORT}", backend="redis://")


@celery.task(bind=True)
def make_operation(self, x: int, y: int, operation: str):
    """
    Return task's args: x: int. y: int, operation: str.
    """
    redis_client.set(self.AsyncResult(self.request.id).id, "Task running")
    time.sleep(10)
    redis_client.set(self.AsyncResult(self.request.id).id, "Task complete")
    return self.request.args


@celery.task(bind=True)
def calculate(self, task_id: str):
    """
    Return calculate x OPERATION y from task make_operation.
    """
    redis_client.set(self.AsyncResult(self.request.id).id, "Task running")
    task = celery.AsyncResult(task_id).info
    if task[2] == "+":
        redis_client.set(self.AsyncResult(self.request.id).id, "Task complete")
        return task[0] + task[1]
    if task[2] == "-":
        redis_client.set(self.AsyncResult(self.request.id).id, "Task complete")
        return task[0] - task[1]
    if task[2] == "/":
        redis_client.set(self.AsyncResult(self.request.id).id, "Task complete")
        return task[0] / task[1]
    if task[2] == "*":
        redis_client.set(self.AsyncResult(self.request.id).id, "Task complete")
        return task[0] * task[1]
