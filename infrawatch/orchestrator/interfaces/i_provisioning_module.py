from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.provisioning.domain.models.infrastructure import Infrastructure, InfrastructureConfig
    from infrawatch.provisioning.domain.models.terraform_state import TerraformState


class IProvisioningModule(ABC):
    """Contract for the provisioning module."""

    @abstractmethod
    def provision(self, config: InfrastructureConfig) -> Infrastructure: ...

    @abstractmethod
    def destroy(self, infrastructure: Infrastructure) -> None: ...

    @abstractmethod
    def get_state(self) -> TerraformState: ...
