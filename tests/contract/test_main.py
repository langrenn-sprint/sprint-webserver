"""Contract test cases for ping."""
from typing import Any

import pytest
import requests


@pytest.mark.contract
def test_main(http_service: Any) -> None:
    """Should return OK."""
    url = f"{http_service}"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

    assert len(response.text) > 0
