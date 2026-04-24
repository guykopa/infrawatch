import json
import logging
import urllib.error
import urllib.request

from infrawatch.observability.domain.models.alert import Alert
from infrawatch.observability.ports.i_alert_manager import IAlertManager

logger = logging.getLogger(__name__)


class GrafanaAdapter(IAlertManager):
    """Fires and resolves alerts via the Grafana Alertmanager API."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    def fire(self, alert: Alert) -> None:
        self._post("/api/alerts", {"name": alert.name, "message": alert.message, "severity": alert.severity.value})

    def resolve(self, alert: Alert) -> None:
        self._post("/api/alerts/resolve", {"name": alert.name})

    def _post(self, path: str, payload: dict) -> None:
        data = json.dumps(payload).encode()
        request = urllib.request.Request(
            f"{self._base_url}{path}",
            data=data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self._api_key}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.status not in (200, 201):
                    logger.error("Grafana API returned %s for %s", response.status, path)
        except urllib.error.URLError as exc:
            logger.error("Grafana unreachable: %s", exc)
