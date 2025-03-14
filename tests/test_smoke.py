import pytest
import requests
from http import HTTPStatus
from models.User import *
from models.AppStatus import AppStatus



class TestSmoke:
    def test_status_healthcheck(self, app_url: str):
        response = requests.get(f"{app_url}/status/", timeout=5)
        assert response.status_code == HTTPStatus.OK
        result = response.json()
        AppStatus.model_validate(result)
        assert result["users"] == True
    @pytest.mark.parametrize("endpoint, expected_status", [("/api/users", HTTPStatus.OK), ("/status", HTTPStatus.OK)])
    def test_api_endpoints(self, app_url: str, endpoint: str, expected_status: HTTPStatus):
        response = requests.get(f"{app_url}{endpoint}")
        assert response.status_code == expected_status

        if endpoint == "/api/users":
            Users.model_validate(response.json())

