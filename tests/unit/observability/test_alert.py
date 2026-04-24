from infrawatch.observability.domain.models.alert import Alert, AlertSeverity


class TestAlert:
    def test_alert_stores_name_message_severity(self) -> None:
        alert = Alert(name="high_error_rate", message="Error rate > 5%", severity=AlertSeverity.CRITICAL)

        assert alert.name == "high_error_rate"
        assert alert.message == "Error rate > 5%"
        assert alert.severity == AlertSeverity.CRITICAL

    def test_alert_is_critical(self) -> None:
        alert = Alert(name="down", message="Service down", severity=AlertSeverity.CRITICAL)

        assert alert.is_critical() is True

    def test_alert_is_not_critical_when_warning(self) -> None:
        alert = Alert(name="latency", message="Latency high", severity=AlertSeverity.WARNING)

        assert alert.is_critical() is False

    def test_alert_severity_has_info_warning_critical(self) -> None:
        assert AlertSeverity.INFO
        assert AlertSeverity.WARNING
        assert AlertSeverity.CRITICAL
