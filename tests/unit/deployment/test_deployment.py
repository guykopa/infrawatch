import pytest

from infrawatch.deployment.domain.models.deployment import Deployment, DeploymentStatus, Pod, PodStatus


class TestPod:
    def test_pod_stores_name_and_status(self) -> None:
        pod = Pod(name="app-abc", status=PodStatus.RUNNING)

        assert pod.name == "app-abc"
        assert pod.status == PodStatus.RUNNING

    def test_pod_is_running(self) -> None:
        pod = Pod(name="app-abc", status=PodStatus.RUNNING)

        assert pod.is_running() is True

    def test_pod_not_running_when_pending(self) -> None:
        pod = Pod(name="app-abc", status=PodStatus.PENDING)

        assert pod.is_running() is False


class TestDeployment:
    def test_deployment_stores_name_image_version(self) -> None:
        deployment = Deployment(name="app", image="app:1.0", version="1.0", status=DeploymentStatus.RUNNING)

        assert deployment.name == "app"
        assert deployment.image == "app:1.0"
        assert deployment.version == "1.0"

    def test_deployment_is_running(self) -> None:
        deployment = Deployment(name="app", image="app:1.0", version="1.0", status=DeploymentStatus.RUNNING)

        assert deployment.is_running() is True

    def test_deployment_not_running_when_failed(self) -> None:
        deployment = Deployment(name="app", image="app:1.0", version="1.0", status=DeploymentStatus.FAILED)

        assert deployment.is_running() is False

    def test_two_deployments_with_same_name_and_version_are_equal(self) -> None:
        a = Deployment(name="app", image="app:1.0", version="1.0", status=DeploymentStatus.RUNNING)
        b = Deployment(name="app", image="app:1.0", version="1.0", status=DeploymentStatus.RUNNING)

        assert a == b
