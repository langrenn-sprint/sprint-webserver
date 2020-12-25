"""Contract test cases for resultat."""
from typing import Any

import pytest
import requests


@pytest.mark.contract
def test_resultat(http_service: Any) -> None:
    """Should return status 200 and html."""
    url = f"{http_service}/resultat"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

    assert len(response.text) > 0
