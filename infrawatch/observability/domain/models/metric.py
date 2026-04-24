from dataclasses import dataclass, field


@dataclass(frozen=True)
class Metric:
    """A single time-series metric data point."""

    name: str
    value: float
    labels: dict[str, str] = field(default_factory=dict)

    def is_above(self, threshold: float) -> bool:
        return self.value > threshold
