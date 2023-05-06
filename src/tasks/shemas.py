from pydantic import BaseModel


class PostData(BaseModel):
    task_id: str


class GetAnswer(BaseModel):
    result: int


class GetListOfTasks(BaseModel):
    task_key: str
    status: str
