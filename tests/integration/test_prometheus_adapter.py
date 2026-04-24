import pytest

from infrawatch.observability.adapters.prometheus_adapter import PrometheusAdapter
from infrawatch.observability.domain.models.metric import Metric


@pytest.mark.integration
class TestPrometheusAdapter:
    """Requires a running Prometheus instance at localhost:9090."""

    def test_collect_returns_metrics(self) -> None:
        adapter = PrometheusAdapter(base_url="http://localhost:9090")

        metrics = adapter.collect("up")

        assert isinstance(metrics, list)

    def test_collect_returns_metric_objects(self) -> None:
        adapter = PrometheusAdapter(base_url="http://localhost:9090")

        metrics = adapter.collect("up")

        for metric in metrics:
            assert isinstance(metric, Metric)
            assert metric.name
