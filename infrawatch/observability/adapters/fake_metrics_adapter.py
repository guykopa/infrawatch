from infrawatch.observability.domain.models.metric import Metric
from infrawatch.observability.ports.i_metrics_collector import IMetricsCollector


class FakeMetricsAdapter(IMetricsCollector):
    """In-memory IMetricsCollector for use in unit tests."""

    def __init__(self, metrics: list[Metric] | None = None) -> None:
        self._metrics = metrics or []

    def collect(self, target: str) -> list[Metric]:
        return self._metrics
