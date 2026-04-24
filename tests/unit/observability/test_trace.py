from infrawatch.observability.domain.models.trace import Trace


class TestTrace:
    def test_trace_stores_ids_operation_duration(self) -> None:
        trace = Trace(trace_id="abc123", span_id="span001", operation="GET /health", duration_ms=12.5)

        assert trace.trace_id == "abc123"
        assert trace.span_id == "span001"
        assert trace.operation == "GET /health"
        assert trace.duration_ms == 12.5

    def test_two_traces_with_same_fields_are_equal(self) -> None:
        a = Trace(trace_id="abc", span_id="s1", operation="GET /", duration_ms=5.0)
        b = Trace(trace_id="abc", span_id="s1", operation="GET /", duration_ms=5.0)

        assert a == b
