from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.deployment.domain.models.deployment import Deployment, Pod
    from infrawatch.deployment.domain.models.rollout_status import RolloutStatus


class IContainerOrchestrator(ABC):
    """Contract for container orchestration backends (kubectl, Helm, etc.)."""

    @abstractmethod
    def apply(self, manifest: str) -> RolloutStatus: ...

    @abstractmethod
    def rollback(self, deployment: Deployment) -> RolloutStatus: ...

    @abstractmethod
    def get_pod_status(self, name: str) -> list[Pod]: ...
