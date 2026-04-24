from dataclasses import dataclass
from enum import Enum


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Alert:
    """Represents a monitoring alert."""

    name: str
    message: str
    severity: AlertSeverity

    def is_critical(self) -> bool:
        return self.severity == AlertSeverity.CRITICAL
