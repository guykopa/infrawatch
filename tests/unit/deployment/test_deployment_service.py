import pytest

from infrawatch.deployment.domain.exceptions.deployment_error import DeploymentError
from infrawatch.deployment.domain.models.deployment import Deployment, DeploymentStatus
from infrawatch.deployment.domain.models.rollout_status import RolloutStatus
from infrawatch.deployment.domain.services.deployment_service import DeploymentService
from infrawatch.deployment.ports.i_container_orchestrator import IContainerOrchestrator
from tests.conftest import FakeOrchestratorAdapter


class TestDeploymentService:
    def test_deploy_delegates_to_orchestrator(self, fake_orchestrator: FakeOrchestratorAdapter) -> None:
        service = DeploymentService(orchestrator=fake_orchestrator)

        result = service.deploy(image="app", version="1.0")

        assert isinstance(result, RolloutStatus)
        assert result.is_ready()
        assert len(fake_orchestrator.applied) == 1

    def test_deploy_raises_when_rollout_not_ready(self) -> None:
        class FailingOrchestrator(IContainerOrchestrator):
            def apply(self, manifest: str) -> RolloutStatus:
                return RolloutStatus(ready=False, replicas=3, available=0)

            def rollback(self, deployment: Deployment) -> RolloutStatus:
                return RolloutStatus(ready=True, replicas=3, available=3)

            def get_pod_status(self, name: str) -> list:
                return []

        service = DeploymentService(orchestrator=FailingOrchestrator())

        with pytest.raises(DeploymentError):
            service.deploy(image="app", version="1.0")

    def test_get_status_delegates_to_orchestrator(self, fake_orchestrator: FakeOrchestratorAdapter) -> None:
        service = DeploymentService(orchestrator=fake_orchestrator)

        pods = service.get_pods("app")

        assert len(pods) == 1
        assert pods[0].is_running()
