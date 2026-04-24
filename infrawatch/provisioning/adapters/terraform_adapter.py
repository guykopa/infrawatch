import json
import logging
import subprocess

from infrawatch.provisioning.domain.models.infrastructure import Infrastructure, InfrastructureConfig, InfraStatus
from infrawatch.provisioning.domain.models.terraform_state import TerraformState
from infrawatch.provisioning.ports.i_infra_provider import IInfraProvider

logger = logging.getLogger(__name__)


class TerraformAdapter(IInfraProvider):
    """Calls the terraform CLI to provision and destroy infrastructure."""

    def __init__(self, working_dir: str) -> None:
        self._working_dir = working_dir

    def apply(self, config: InfrastructureConfig) -> Infrastructure:
        self._run(["terraform", "init", "-input=false"])
        self._run(["terraform", "plan", "-input=false", "-out=tfplan"])
        result = subprocess.run(
            ["terraform", "apply", "-input=false", "-auto-approve", "tfplan"],
            cwd=self._working_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            logger.error("terraform apply failed: %s", result.stderr)
            return Infrastructure(id=config.name, status=InfraStatus.FAILED)
        return Infrastructure(id=config.name, status=InfraStatus.READY)

    def destroy(self, infrastructure: Infrastructure) -> None:
        result = subprocess.run(
            ["terraform", "destroy", "-input=false", "-auto-approve"],
            cwd=self._working_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            logger.error("terraform destroy failed: %s", result.stderr)

    def get_state(self) -> TerraformState:
        result = subprocess.run(
            ["terraform", "show", "-json"],
            cwd=self._working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return TerraformState(resources=[], version="unknown")
        try:
            data = json.loads(result.stdout)
            resources = [r["address"] for r in data.get("values", {}).get("root_module", {}).get("resources", [])]
            version = data.get("terraform_version", "unknown")
        except (json.JSONDecodeError, KeyError):
            resources = []
            version = "unknown"
        return TerraformState(resources=resources, version=version)

    def _run(self, cmd: list[str]) -> None:
        result = subprocess.run(
            cmd,
            cwd=self._working_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(f"{cmd[0]} {cmd[1]} failed: {result.stderr}")
