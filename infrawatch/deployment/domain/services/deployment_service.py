from infrawatch.deployment.domain.exceptions.deployment_error import DeploymentError
from infrawatch.deployment.domain.models.deployment import Pod
from infrawatch.deployment.domain.models.rollout_status import RolloutStatus
from infrawatch.deployment.ports.i_container_orchestrator import IContainerOrchestrator


class DeploymentService:
    """Orchestrates application deployment via an IContainerOrchestrator."""

    def __init__(self, orchestrator: IContainerOrchestrator) -> None:
        self._orchestrator = orchestrator

    def deploy(self, image: str, version: str) -> RolloutStatus:
        manifest = f"{image}:{version}"
        status = self._orchestrator.apply(manifest)
        if not status.is_ready():
            raise DeploymentError(f"Deployment failed for {image}:{version}")
        return status

    def get_pods(self, name: str) -> list[Pod]:
        return self._orchestrator.get_pod_status(name)
