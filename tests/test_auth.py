from fastapi.testclient import TestClient
from faker import Faker

from app.core.config import API_PREFIX
from app.internal.auth.schemas import UserCreate

AUTH_API_PREFIX = f"{API_PREFIX}/auth"


fake = Faker()

user_payload = UserCreate(username=fake.name(), password=fake.password(length=8))


def test_success_case_for_signup(test_client: TestClient):
    response = test_client.post(
        f"{AUTH_API_PREFIX}/signup", json=user_payload.model_dump()
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "ok"
    assert isinstance(response_json["data"], dict)
    assert isinstance(response_json["data"]["access_token"], str)
    assert isinstance(response_json["data"]["user"], dict)
    assert response_json["data"]["user"]["username"] == user_payload.username


def test_duplicate_signup_failure(test_client: TestClient):
    response = test_client.post(
        f"{AUTH_API_PREFIX}/signup", json=user_payload.model_dump()
    )
    assert response.status_code == 400


def test_login_success(test_client: TestClient):
    response = test_client.post(
        f"{AUTH_API_PREFIX}/login", json=user_payload.model_dump()
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "ok"
    assert isinstance(response_json["data"], dict)
    assert isinstance(response_json["data"]["access_token"], str)
    assert isinstance(response_json["data"]["user"], dict)
    assert response_json["data"]["user"]["username"] == user_payload.username


def test_invalid_username_in_login_failure(test_client: TestClient):
    user_payload = user_payload = UserCreate(
        username=fake.name(), password=fake.password(length=8)
    )
    response = test_client.post(
        f"{AUTH_API_PREFIX}/login", json=user_payload.model_dump()
    )
    assert response.status_code == 400


def test_invalid_password_in_login_failure(test_client: TestClient):
    payload = UserCreate(username=user_payload.username, password=fake.password(8))
    response = test_client.post(f"{AUTH_API_PREFIX}/login", json=payload.model_dump())
    assert response.status_code == 400
