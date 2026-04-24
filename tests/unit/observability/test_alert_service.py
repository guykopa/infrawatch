from infrawatch.observability.domain.models.alert import Alert, AlertSeverity
from infrawatch.observability.domain.services.alert_service import AlertService
from tests.conftest import FakeAlertManager


class TestAlertService:
    def test_fire_alert_delegates_to_manager(self, fake_alert_manager: FakeAlertManager) -> None:
        service = AlertService(manager=fake_alert_manager)
        alert = Alert(name="high_error_rate", message="Error rate > 5%", severity=AlertSeverity.CRITICAL)

        service.fire_alert(alert)

        assert alert in fake_alert_manager.fired

    def test_resolve_alert_delegates_to_manager(self, fake_alert_manager: FakeAlertManager) -> None:
        service = AlertService(manager=fake_alert_manager)
        alert = Alert(name="high_error_rate", message="Error rate > 5%", severity=AlertSeverity.CRITICAL)

        service.resolve_alert(alert)

        assert alert in fake_alert_manager.resolved
