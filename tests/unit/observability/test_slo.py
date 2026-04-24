from infrawatch.observability.domain.models.slo import SLO


class TestSLO:
    def test_slo_stores_name_and_threshold(self) -> None:
        slo = SLO(name="error_rate", metric_name="http_error_rate", threshold=0.05)

        assert slo.name == "error_rate"
        assert slo.threshold == 0.05

    def test_slo_is_breached_when_value_above_threshold(self) -> None:
        slo = SLO(name="error_rate", metric_name="http_error_rate", threshold=0.05)

        assert slo.is_breached(0.06) is True

    def test_slo_not_breached_when_value_below_threshold(self) -> None:
        slo = SLO(name="error_rate", metric_name="http_error_rate", threshold=0.05)

        assert slo.is_breached(0.03) is False

    def test_slo_not_breached_at_exact_threshold(self) -> None:
        slo = SLO(name="error_rate", metric_name="http_error_rate", threshold=0.05)

        assert slo.is_breached(0.05) is False
