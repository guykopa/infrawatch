from dataclasses import dataclass


@dataclass(frozen=True)
class RolloutStatus:
    """Snapshot of a Kubernetes rollout state."""

    ready: bool
    replicas: int
    available: int

    def is_ready(self) -> bool:
        return self.ready

    def all_available(self) -> bool:
        return self.available == self.replicas
