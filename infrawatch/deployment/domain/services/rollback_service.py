from infrawatch.deployment.domain.models.deployment import Deployment
from infrawatch.deployment.domain.models.rollout_status import RolloutStatus
from infrawatch.deployment.ports.i_container_orchestrator import IContainerOrchestrator


class RollbackService:
    """Handles deployment rollback via an IContainerOrchestrator."""

    def __init__(self, orchestrator: IContainerOrchestrator) -> None:
        self._orchestrator = orchestrator

    def rollback(self, deployment: Deployment) -> RolloutStatus:
        return self._orchestrator.rollback(deployment)
