from dataclasses import dataclass


@dataclass(frozen=True)
class SLO:
    """Service Level Objective definition."""

    name: str
    metric_name: str
    threshold: float

    def is_breached(self, value: float) -> bool:
        return value > self.threshold
