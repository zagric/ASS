# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from typing import TYPE_CHECKING

from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient


if TYPE_CHECKING:
    from httpx import Response


def test_create_simulation_success(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for("create_simulation_handler")
    payload = {
        "producers_count": faker.random_int(min=0, max=1000),
        "consumers_count": faker.random_int(min=0, max=1000),
        "buffer_size": faker.random_int(min=0, max=10000),
    }
    response: Response = client.post(url, json=payload)

    assert response.is_success
    json_data = response.json()

    assert json_data["producers_count"] == payload["producers_count"]
    assert json_data["consumers_count"] == payload["consumers_count"]
    assert json_data["buffer_size"] == payload["buffer_size"]
