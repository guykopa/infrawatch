from infrawatch.observability.domain.models.alert import Alert
from infrawatch.observability.ports.i_alert_manager import IAlertManager


class AlertService:
    """Fires and resolves alerts via an IAlertManager."""

    def __init__(self, manager: IAlertManager) -> None:
        self._manager = manager

    def fire_alert(self, alert: Alert) -> None:
        self._manager.fire(alert)

    def resolve_alert(self, alert: Alert) -> None:
        self._manager.resolve(alert)
