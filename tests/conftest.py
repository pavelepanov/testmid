import pytest
import asyncio
from fastapi.testclient import TestClient
from config import REDIS_HOST, REDIS_PORT
from main import app
from src.tasks.tasks import make_operation
from celery import Celery


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
def celery_config():
    return {
        'broker_url': f"redis://{REDIS_HOST}:{REDIS_PORT}",
        'result_backend': "redis://"
    }


@pytest.fixture(scope="function")
async def create_task():
    task = make_operation.delay(1, 2, "+")
    return task.id


@pytest.fixture(scope="function")
async def create_celery():
    celery = Celery("tasks", broker=f"redis://{REDIS_HOST}:{REDIS_PORT}", backend="redis://")
    return celery
