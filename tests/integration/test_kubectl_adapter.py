import pytest

from infrawatch.deployment.adapters.kubectl_adapter import KubectlAdapter
from infrawatch.deployment.domain.models.deployment import Deployment, DeploymentStatus
from infrawatch.deployment.domain.models.rollout_status import RolloutStatus


@pytest.mark.integration
class TestKubectlAdapter:
    """Requires a running minikube cluster."""

    def test_apply_returns_rollout_status(self, tmp_path: pytest.TempPathFactory) -> None:
        manifest = str(tmp_path / "deployment.yaml")
        adapter = KubectlAdapter(namespace="test")

        result = adapter.apply(manifest)

        assert isinstance(result, RolloutStatus)

    def test_get_pod_status_returns_pods(self) -> None:
        adapter = KubectlAdapter(namespace="test")

        pods = adapter.get_pod_status("infrawatch-app")

        assert isinstance(pods, list)

    def test_rollback_returns_rollout_status(self) -> None:
        adapter = KubectlAdapter(namespace="test")
        deployment = Deployment(name="infrawatch-app", image="app:1.0", version="1.0", status=DeploymentStatus.FAILED)

        result = adapter.rollback(deployment)

        assert isinstance(result, RolloutStatus)
