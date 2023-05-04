from fastapi import FastAPI

from tasks.router import router as tasks_router

app = FastAPI(
    title="Middle test"
)

app.include_router(tasks_router)
