from http import HTTPStatus
import pytest
import requests
from models.User import User


@pytest.fixture
def users(app_url: str) -> list[dict]:
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()['items']

class TestUsers:
    def test_users_no_duplicates(self, users: list[dict]):
        users_ids = [user["id"] for user in users]
        assert len(users_ids) == len(set(users_ids))

    def test_users(self, app_url: str, users: list[dict]):
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK

        for user in users:
            User.model_validate(user)

    @pytest.mark.parametrize("user_id", [1, 6, 12])
    def test_user(self, app_url: str, user_id: int):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK

        user = response.json()
        User.model_validate(user)

    @pytest.mark.parametrize("user_id", [13, 100])
    def test_user_nonexistent_values(self, app_url: str, user_id: int):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", [-1, 0, "fafaf", None, ["user"]])
    def test_user_invalid_values(self, app_url: str, user_id: int):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

