import pytest
import dotenv
import os
import requests
import json
from http import HTTPStatus
from models.User import User


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")
