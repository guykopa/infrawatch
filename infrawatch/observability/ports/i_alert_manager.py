from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.observability.domain.models.alert import Alert


class IAlertManager(ABC):
    """Contract for alert management backends (Grafana, Alertmanager, etc.)."""

    @abstractmethod
    def fire(self, alert: Alert) -> None: ...

    @abstractmethod
    def resolve(self, alert: Alert) -> None: ...
