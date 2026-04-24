from dataclasses import dataclass
from enum import Enum


class InfraStatus(Enum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"
    DESTROYED = "destroyed"


@dataclass(frozen=True)
class InfrastructureConfig:
    """Desired state for an infrastructure environment."""

    name: str
    region: str


@dataclass(frozen=True)
class Infrastructure:
    """Represents a provisioned infrastructure environment."""

    id: str
    status: InfraStatus

    def is_ready(self) -> bool:
        return self.status == InfraStatus.READY
