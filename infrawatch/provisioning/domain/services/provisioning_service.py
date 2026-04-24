from infrawatch.provisioning.domain.exceptions.provisioning_error import ProvisioningError
from infrawatch.provisioning.domain.models.infrastructure import Infrastructure, InfrastructureConfig
from infrawatch.provisioning.domain.models.terraform_state import TerraformState
from infrawatch.provisioning.ports.i_infra_provider import IInfraProvider


class ProvisioningService:
    """Orchestrates infrastructure lifecycle via an IInfraProvider."""

    def __init__(self, provider: IInfraProvider) -> None:
        self._provider = provider

    def provision(self, config: InfrastructureConfig) -> Infrastructure:
        infrastructure = self._provider.apply(config)
        if not infrastructure.is_ready():
            raise ProvisioningError(f"Provisioning failed for {config.name}: status={infrastructure.status}")
        return infrastructure

    def destroy(self, infrastructure: Infrastructure) -> None:
        self._provider.destroy(infrastructure)

    def get_state(self) -> TerraformState:
        return self._provider.get_state()
