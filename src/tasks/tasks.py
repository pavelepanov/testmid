from celery import Celery
from celery.result import AsyncResult
from celery.backends.redis import RedisBackend
from config import REDIS_HOST, REDIS_PORT

import time
from database.db import redis_client

# celery = Celery("tasks", broker="redis://localhost:6379", backend="redis://")
celery = Celery("tasks")
celery.conf.update(
    broker_url="redis://localhost:6379/0",
    result_backend="redis://localhost:6379/0"
)

backend = RedisBackend(app=celery, url=f"redis://{REDIS_HOST}:{REDIS_PORT}/0")


@celery.task(bind=True)
def create_task(self):
    print(f"{self.AsyncResult(self.request.id).ready()}")


@celery.task(bind=True)
def make_operation(self, x: int, y: int, operation):
    print("-" * 8)
    redis_client.set(self.AsyncResult(self.request.id).id, "Task running")
    time.sleep(10)
    redis_client.set(self.AsyncResult(self.request.id).id, "Task complete")
    return self.request.args


@celery.task
def run_tasks():
    for task_id in celery.control.inspect().registered():
        result = AsyncResult(task_id)
        print("-" * 10)
        print(f'Task {task_id} is in state {result.state} with result {result.result}')
    i = celery.control.inspect().registered()
    print(i['celery@fedora'][0].id)


@celery.task
def mane():
    print(66666)
    time.sleep(10)
    return "hi"


@celery.task(bind=True)
def calculate(self, id):
    redis_client.set(self.AsyncResult(self.request.id).id, "Task running")
    task = celery.AsyncResult(id).info
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
