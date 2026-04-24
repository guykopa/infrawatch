from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.observability.domain.models.trace import Trace


class ITraceExporter(ABC):
    """Contract for trace export backends (Jaeger, OTel Collector, etc.)."""

    @abstractmethod
    def export(self, trace: Trace) -> None: ...
