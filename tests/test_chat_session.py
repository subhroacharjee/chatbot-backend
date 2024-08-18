from fastapi.testclient import TestClient
from faker import Faker

from app.core.config import API_PREFIX
from app.internal.auth.schemas import UserCreate
from app.internal.chats.schemas import Chat

fake = Faker()

CHAT_SESSION_API_PREFIX = f"{API_PREFIX}/session"


def _get_token(test_client: TestClient):
    user_payload = UserCreate(username=fake.name(), password=fake.password(length=8))
    response = test_client.post(
        f"{API_PREFIX}/auth/signup", json=user_payload.model_dump()
    )
    assert response.status_code == 200
    token = response.json()["data"]["access_token"]
    assert token is not None
    return token


def test_create_chat_session(test_client: TestClient):
    token = _get_token(test_client)

    response = test_client.post(
        CHAT_SESSION_API_PREFIX, headers={"authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    response_body = response.json()
    assert isinstance(response_body, dict)
    assert response_body["status"] == "ok"
    assert isinstance(response_body["data"], dict)
    assert isinstance(response_body["data"]["id"], int)


def test_create_chat_session_without_bearer(test_client: TestClient):
    response = test_client.post(
        CHAT_SESSION_API_PREFIX,
    )

    assert response.status_code == 401


def test_create_chat_update_and_delete_chat(test_client: TestClient):
    """
    Generally i would create tests for the three cases, but due to the time
    crunch and my limited knowledge on pytest, I will make the three test into
    one.
    """
    token = _get_token(test_client)
    headers = {"authorization": f"Bearer {token}"}

    response = test_client.post(CHAT_SESSION_API_PREFIX, headers=headers)

    assert response.status_code == 200
    response_body = response.json()
    assert isinstance(response_body, dict)
    assert response_body["status"] == "ok"
    session_id: int = response_body["data"]["id"]

    # create test
    response = test_client.post(
        f"{CHAT_SESSION_API_PREFIX}/{session_id}/chat",
        headers=headers,
        json={"prompt": "deeez"},
    )
    assert response.status_code == 200
    response_body = response.json()
    assert isinstance(response_body, dict)
    print(response_body)
    assert response_body["status"] == "ok"
    assert isinstance(response_body["data"], dict)
    chat = Chat.model_validate(response_body["data"])
    assert chat.response == "response from ai"

    # update test
    response = test_client.put(
        f"{CHAT_SESSION_API_PREFIX}/{session_id}/chat/{chat.id}",
        headers=headers,
        json={"prompt": "deeez"},
    )
    assert response.status_code == 200
    response_body = response.json()
    assert isinstance(response_body, dict)
    print(response_body)
    assert response_body["status"] == "ok"
    assert isinstance(response_body["data"], dict)
    chat = Chat.model_validate(response_body["data"])
    assert chat.response == "response from ai"

    # delete test
    response = test_client.delete(
        f"{CHAT_SESSION_API_PREFIX}/{session_id}/chat/{chat.id}",
        headers=headers,
    )
    assert response.status_code == 200

    # checking if after delete we still retrieve the previous chat or not.
    response = test_client.put(
        f"{CHAT_SESSION_API_PREFIX}/{session_id}/chat/{chat.id}",
        headers=headers,
        json={"prompt": "deeez"},
    )
    assert response.status_code == 404
