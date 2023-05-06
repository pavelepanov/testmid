from celery import Celery
from celery.result import AsyncResult
from config import REDIS_HOST, REDIS_PORT

import time
from database.db import redis_client

celery = Celery("tasks", broker=f"redis://{REDIS_HOST}:{REDIS_PORT}", backend="redis://")


@celery.task(bind=True)
def create_task(self):
    print(f"{self.AsyncResult(self.request.id).ready()}")


@celery.task(bind=True)
def make_operation(self, x: int, y: int, operation: str):
    redis_client.set(self.AsyncResult(self.request.id).id, "Task running")
    time.sleep(10)
    redis_client.set(self.AsyncResult(self.request.id).id, "Task complete")
    print(self.request.args)
    return self.request.args


@celery.task(bind=True)
def calculate(self, task_id: str):
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



