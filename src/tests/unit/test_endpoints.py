import pytest
from conftest import client
from fastapi import status


class TestEndpoint:
    data_positive = [
        (10,
         20,
         "+"),
        (10,
         20,
         "-"),
        (10,
         20,
         "/"),
        (10,
         20,
         "*")
    ]

    data_negative = [
        (10,
         20,
         4),
        (10,
         20,
         "a"),
        (10,
         20,
         [123, 432]),
        (10,
         20,
         "")
    ]

    @pytest.mark.parametrize("x, y, operation", data_positive)
    async def test_post_data_positive(self, x, y, operation):
        response = client.post("/root/one", data={
            "x": x,
            "y": y,
            "operation": operation
        })

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("x, y, operation", data_negative)
    async def test_post_data_negative(self, x, y, operation):
        response = client.post("/root/one", data={
            "x": x,
            "y": y,
            "operation": operation
        })

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    async def test_get_answer(self, create_task):
        response = client.post("/root/two", data={
            "task_id": create_task
        })

        assert response.status_code == status.HTTP_200_OK

    async def test_get_list_of_tasks(self, create_task):
        response = client.post("/root/three")
        assert response.status_code == status.HTTP_200_OK