from infrawatch.observability.domain.models.metric import Metric
from infrawatch.observability.domain.models.slo import SLO
from infrawatch.observability.domain.services.metrics_service import MetricsService
from tests.conftest import FakeMetricsCollector


class TestMetricsService:
    def test_collect_metrics_delegates_to_collector(self) -> None:
        metrics = [Metric(name="up", value=1.0, labels={})]
        service = MetricsService(collector=FakeMetricsCollector(metrics=metrics))

        result = service.collect_metrics("localhost:9090")

        assert result == metrics

    def test_check_slo_passes_when_not_breached(self) -> None:
        metrics = [Metric(name="http_error_rate", value=0.03, labels={})]
        service = MetricsService(collector=FakeMetricsCollector(metrics=metrics))
        slo = SLO(name="error_rate", metric_name="http_error_rate", threshold=0.05)

        assert service.check_slo(slo, target="localhost:9090") is True

    def test_check_slo_fails_when_breached(self) -> None:
        metrics = [Metric(name="http_error_rate", value=0.08, labels={})]
        service = MetricsService(collector=FakeMetricsCollector(metrics=metrics))
        slo = SLO(name="error_rate", metric_name="http_error_rate", threshold=0.05)

        assert service.check_slo(slo, target="localhost:9090") is False

    def test_check_slo_passes_when_metric_not_found(self) -> None:
        service = MetricsService(collector=FakeMetricsCollector(metrics=[]))
        slo = SLO(name="error_rate", metric_name="http_error_rate", threshold=0.05)

        assert service.check_slo(slo, target="localhost:9090") is True
