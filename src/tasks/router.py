from fastapi import APIRouter

from tasks.tasks import make_operation, calculate
from database.db import redis_client

router = APIRouter(
    prefix="/root",
    tags=["root"]
)


@router.post("/one")
def post_data(x: int, y: int, operation: str) -> str:
    task = make_operation.delay(x, y, operation)
    redis_client.set(task.id, "Task in queue")
    return task.id


@router.get("/two")
def get_answer(id: str) -> int:
    res = calculate.delay(id).get()
    redis_client.set(res.id, "Task in queue")
    return res


@router.get("/three")
def get_list_of_tasks():
    tasks_info = []
    for i in redis_client.keys():
        i = i.decode("utf-8")
        if not i.startswith("_kombu") and not i.startswith("celery"):
            tasks_info.append({i: redis_client.get(i), })

    return tasks_info
