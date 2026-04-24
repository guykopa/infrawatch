import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


class TestHealthEndpoint:
    def test_health_returns_200(self, client: TestClient) -> None:
        response = client.get("/health")

        assert response.status_code == 200

    def test_health_returns_status_ok(self, client: TestClient) -> None:
        response = client.get("/health")

        assert response.json() == {"status": "ok"}


class TestReadyEndpoint:
    def test_ready_returns_200(self, client: TestClient) -> None:
        response = client.get("/ready")

        assert response.status_code == 200

    def test_ready_returns_status_ready(self, client: TestClient) -> None:
        response = client.get("/ready")

        assert response.json() == {"status": "ready"}


class TestMetricsEndpoint:
    def test_metrics_returns_200(self, client: TestClient) -> None:
        response = client.get("/metrics")

        assert response.status_code == 200

    def test_metrics_returns_prometheus_format(self, client: TestClient) -> None:
        response = client.get("/metrics")

        assert "text/plain" in response.headers["content-type"]

    def test_metrics_contains_request_counter(self, client: TestClient) -> None:
        client.get("/health")

        response = client.get("/metrics")

        assert "http_requests_total" in response.text

    def test_metrics_contains_latency_histogram(self, client: TestClient) -> None:
        client.get("/health")

        response = client.get("/metrics")

        assert "http_request_duration_seconds" in response.text

    def test_request_counter_increments(self, client: TestClient) -> None:
        client.get("/health")
        client.get("/health")

        response = client.get("/metrics")

        assert 'path="/health"' in response.text
