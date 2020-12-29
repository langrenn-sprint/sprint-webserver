"""Contract test cases for klasser."""
import json
from typing import Any

import pytest
import requests


@pytest.mark.contract
def test_create_klasser(http_service: Any) -> None:
    """Should return status 201."""
    url = f"{http_service}/klasser"
    with open("tests/files/Klasser.json") as json_file:
        data = json.load(json_file)

    headers = {"content-type": "application/json; charset=utf-8"}
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 201


@pytest.mark.contract
def test_get_klasser(http_service: Any) -> None:
    """Should return status 200 and json."""
    url = f"{http_service}/klasser"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    assert len(response.text) > 0
