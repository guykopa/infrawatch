import logging
import subprocess

from infrawatch.deployment.domain.models.deployment import Deployment, Pod, PodStatus
from infrawatch.deployment.domain.models.rollout_status import RolloutStatus
from infrawatch.deployment.ports.i_container_orchestrator import IContainerOrchestrator

logger = logging.getLogger(__name__)


class HelmAdapter(IContainerOrchestrator):
    """Calls helm to manage Kubernetes deployments via Helm charts."""

    def __init__(self, namespace: str = "default", release: str = "infrawatch") -> None:
        self._namespace = namespace
        self._release = release

    def apply(self, manifest: str) -> RolloutStatus:
        result = subprocess.run(
            ["helm", "upgrade", "--install", self._release, manifest,
             "--namespace", self._namespace, "--wait", "--timeout", "120s"],
            capture_output=True,
            text=True,
            timeout=130,
        )
        if result.returncode != 0:
            logger.error("helm upgrade failed: %s", result.stderr)
            return RolloutStatus(ready=False, replicas=0, available=0)
        return RolloutStatus(ready=True, replicas=1, available=1)

    def rollback(self, deployment: Deployment) -> RolloutStatus:
        result = subprocess.run(
            ["helm", "rollback", self._release, "--namespace", self._namespace, "--wait"],
            capture_output=True,
            text=True,
            timeout=130,
        )
        if result.returncode != 0:
            logger.error("helm rollback failed: %s", result.stderr)
            return RolloutStatus(ready=False, replicas=0, available=0)
        return RolloutStatus(ready=True, replicas=1, available=1)

    def get_pod_status(self, name: str) -> list[Pod]:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", self._namespace, "-l", f"app.kubernetes.io/instance={self._release}",
             "--no-headers", "-o", "custom-columns=NAME:.metadata.name,STATUS:.status.phase"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return []
        pods = []
        for line in result.stdout.strip().splitlines():
            parts = line.split()
            if len(parts) == 2:
                status = PodStatus.RUNNING if parts[1] == "Running" else PodStatus.PENDING
                pods.append(Pod(name=parts[0], status=status))
        return pods
