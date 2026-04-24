from infrawatch.deployment.domain.models.deployment import Deployment, DeploymentStatus
from infrawatch.deployment.domain.models.rollout_status import RolloutStatus
from infrawatch.deployment.domain.services.rollback_service import RollbackService
from tests.conftest import FakeOrchestratorAdapter


class TestRollbackService:
    def test_rollback_delegates_to_orchestrator(self, fake_orchestrator: FakeOrchestratorAdapter) -> None:
        service = RollbackService(orchestrator=fake_orchestrator)
        deployment = Deployment(name="app", image="app:1.0", version="1.0", status=DeploymentStatus.FAILED)

        result = service.rollback(deployment)

        assert isinstance(result, RolloutStatus)
        assert result.is_ready()
        assert deployment in fake_orchestrator.rolled_back

    def test_rollback_records_the_deployment(self, fake_orchestrator: FakeOrchestratorAdapter) -> None:
        service = RollbackService(orchestrator=fake_orchestrator)
        deployment = Deployment(name="app", image="app:0.9", version="0.9", status=DeploymentStatus.FAILED)

        service.rollback(deployment)

        assert len(fake_orchestrator.rolled_back) == 1
        assert fake_orchestrator.rolled_back[0].version == "0.9"
