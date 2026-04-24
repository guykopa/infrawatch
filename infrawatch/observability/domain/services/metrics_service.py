from infrawatch.observability.domain.models.metric import Metric
from infrawatch.observability.domain.models.slo import SLO
from infrawatch.observability.ports.i_metrics_collector import IMetricsCollector


class MetricsService:
    """Collects metrics and evaluates SLOs via an IMetricsCollector."""

    def __init__(self, collector: IMetricsCollector) -> None:
        self._collector = collector

    def collect_metrics(self, target: str) -> list[Metric]:
        return self._collector.collect(target)

    def check_slo(self, slo: SLO, target: str) -> bool:
        metrics = self._collector.collect(target)
        for metric in metrics:
            if metric.name == slo.metric_name:
                return not slo.is_breached(metric.value)
        return True
