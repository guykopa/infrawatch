from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.observability.domain.models.alert import Alert
    from infrawatch.observability.domain.models.metric import Metric
    from infrawatch.observability.domain.models.slo import SLO


class IObservabilityModule(ABC):
    """Contract for the observability module."""

    @abstractmethod
    def collect_metrics(self, target: str) -> list[Metric]: ...

    @abstractmethod
    def check_slo(self, slo: SLO) -> bool: ...

    @abstractmethod
    def fire_alert(self, alert: Alert) -> None: ...
