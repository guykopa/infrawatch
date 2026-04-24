import logging
import urllib.error
import urllib.parse
import urllib.request
import json

from infrawatch.observability.domain.models.metric import Metric
from infrawatch.observability.ports.i_metrics_collector import IMetricsCollector

logger = logging.getLogger(__name__)


class PrometheusAdapter(IMetricsCollector):
    """Scrapes metrics from a Prometheus HTTP API."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    def collect(self, target: str) -> list[Metric]:
        url = f"{self._base_url}/api/v1/query?{urllib.parse.urlencode({'query': target})}"
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = json.loads(response.read().decode())
        except urllib.error.URLError as exc:
            logger.error("Prometheus unreachable: %s", exc)
            return []
        results = data.get("data", {}).get("result", [])
        metrics = []
        for item in results:
            name = item.get("metric", {}).get("__name__", target)
            labels = {k: v for k, v in item.get("metric", {}).items() if k != "__name__"}
            value = float(item.get("value", [0, 0])[1])
            metrics.append(Metric(name=name, value=value, labels=labels))
        return metrics
