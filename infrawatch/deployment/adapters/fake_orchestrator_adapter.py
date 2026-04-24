from infrawatch.deployment.domain.models.deployment import Deployment, Pod, PodStatus
from infrawatch.deployment.domain.models.rollout_status import RolloutStatus
from infrawatch.deployment.ports.i_container_orchestrator import IContainerOrchestrator


class FakeOrchestratorAdapter(IContainerOrchestrator):
    """In-memory IContainerOrchestrator for use in unit tests."""

    def __init__(self) -> None:
        self.applied: list[str] = []
        self.rolled_back: list[Deployment] = []

    def apply(self, manifest: str) -> RolloutStatus:
        self.applied.append(manifest)
        return RolloutStatus(ready=True, replicas=3, available=3)

    def rollback(self, deployment: Deployment) -> RolloutStatus:
        self.rolled_back.append(deployment)
        return RolloutStatus(ready=True, replicas=3, available=3)

    def get_pod_status(self, name: str) -> list[Pod]:
        return [Pod(name=f"{name}-abc", status=PodStatus.RUNNING)]
