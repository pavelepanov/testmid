from fastapi import APIRouter, HTTPException

from tasks.tasks import make_operation, calculate
from database.db import redis_client

from .shemas import PostData, GetAnswer, GetListOfTasks

from typing import List

router = APIRouter(
    prefix="/root",
    tags=["root"]
)


@router.get("/one", response_model=PostData)
def post_data(x: int, y: int, operation: str) -> str:
    task = make_operation.delay(x, y, operation)
    return {"task_id": task.id, }


@router.get("/two", response_model=GetAnswer)
def get_answer(task_id: str) -> int:
    try:
        result = calculate.delay(task_id)
        result = result.get()
        return {"result": result, }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Task with this id no completed"
        })


@router.get("/three", response_model=List[GetListOfTasks])
def get_list_of_tasks() -> list:
    tasks_info = []
    for task_key in redis_client.keys():
        task_key = task_key.decode("utf-8")
        if not task_key.startswith("_kombu") and not task_key.startswith("celery"):
            #tasks_info.append({task_key: redis_client.get(task_key).decode("utf-8"), })
            tasks_info.append({"task_key": task_key, "status": redis_client.get(task_key).decode("utf-8")})
    return tasks_info
