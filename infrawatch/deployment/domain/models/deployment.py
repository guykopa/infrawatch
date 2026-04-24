from dataclasses import dataclass
from enum import Enum


class PodStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    TERMINATED = "terminated"


class DeploymentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass(frozen=True)
class Pod:
    """Represents a single Kubernetes pod."""

    name: str
    status: PodStatus

    def is_running(self) -> bool:
        return self.status == PodStatus.RUNNING


@dataclass(frozen=True)
class Deployment:
    """Represents a Kubernetes deployment."""

    name: str
    image: str
    version: str
    status: DeploymentStatus

    def is_running(self) -> bool:
        return self.status == DeploymentStatus.RUNNING
