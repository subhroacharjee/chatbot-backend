from fastapi.testclient import TestClient

from app.core.config import API_PREFIX

API_ENDPOINT = f"{API_PREFIX}/health-check/"


def test_health_check(test_client: TestClient):
    response = test_client.get(API_ENDPOINT)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "data": None}
