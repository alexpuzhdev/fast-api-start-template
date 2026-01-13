"""
Тесты для health endpoint.
"""

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint() -> None:
    test_client = TestClient(create_app())
    response = test_client.get("/api/v1/health")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "ok"
