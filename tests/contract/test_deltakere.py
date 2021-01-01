"""Contract test cases for klasser."""
import json
from typing import Any

import pytest
import requests


@pytest.mark.contract
def test_create_deltakere(http_service: Any) -> None:
    """Should return status 201."""
    url = f"{http_service}/deltakere"
    with open("tests/files/Deltakere.json") as json_file:
        data = json.load(json_file)

    headers = {"content-type": "application/json; charset=utf-8"}
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 201


@pytest.mark.contract
def test_get_deltakere(http_service: Any) -> None:
    """Should return status 200 and json."""
    url = f"{http_service}/deltakere"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

    assert len(response.text) > 0
