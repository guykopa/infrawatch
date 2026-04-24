from infrawatch.observability.domain.models.metric import Metric


class TestMetric:
    def test_metric_stores_name_value_labels(self) -> None:
        metric = Metric(name="http_requests_total", value=42.0, labels={"method": "GET"})

        assert metric.name == "http_requests_total"
        assert metric.value == 42.0
        assert metric.labels == {"method": "GET"}

    def test_metric_with_no_labels(self) -> None:
        metric = Metric(name="up", value=1.0, labels={})

        assert metric.labels == {}

    def test_metric_is_above_threshold(self) -> None:
        metric = Metric(name="error_rate", value=0.06, labels={})

        assert metric.is_above(0.05) is True

    def test_metric_is_not_above_threshold(self) -> None:
        metric = Metric(name="error_rate", value=0.03, labels={})

        assert metric.is_above(0.05) is False
