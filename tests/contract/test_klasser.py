"""Contract test cases for klasser."""
from typing import Any

import pytest
import requests


@pytest.mark.contract
def test_get_klasser(http_service: Any) -> None:
    """Should return status 200 and json."""
    url = f"{http_service}/klasser"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    assert len(response.text) > 0
