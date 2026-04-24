from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.deployment.domain.models.deployment import Deployment
    from infrawatch.deployment.domain.models.rollout_status import RolloutStatus


class IDeploymentModule(ABC):
    """Contract for the deployment module."""

    @abstractmethod
    def deploy(self, image: str, version: str) -> RolloutStatus: ...

    @abstractmethod
    def rollback(self, deployment: Deployment) -> RolloutStatus: ...

    @abstractmethod
    def get_status(self, name: str) -> RolloutStatus: ...
