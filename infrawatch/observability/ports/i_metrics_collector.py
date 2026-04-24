from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.observability.domain.models.metric import Metric


class IMetricsCollector(ABC):
    """Contract for metrics collection backends (Prometheus, etc.)."""

    @abstractmethod
    def collect(self, target: str) -> list[Metric]: ...
