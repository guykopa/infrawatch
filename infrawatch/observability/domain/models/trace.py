from dataclasses import dataclass


@dataclass(frozen=True)
class Trace:
    """Represents a distributed trace span."""

    trace_id: str
    span_id: str
    operation: str
    duration_ms: float
