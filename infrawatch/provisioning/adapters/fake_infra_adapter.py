from infrawatch.provisioning.domain.models.infrastructure import Infrastructure, InfrastructureConfig, InfraStatus
from infrawatch.provisioning.domain.models.terraform_state import TerraformState
from infrawatch.provisioning.ports.i_infra_provider import IInfraProvider


class FakeInfraAdapter(IInfraProvider):
    """In-memory IInfraProvider for use in unit tests."""

    def __init__(self) -> None:
        self.provisioned: list[InfrastructureConfig] = []
        self.destroyed: list[Infrastructure] = []

    def apply(self, config: InfrastructureConfig) -> Infrastructure:
        self.provisioned.append(config)
        return Infrastructure(id="fake-001", status=InfraStatus.READY)

    def destroy(self, infrastructure: Infrastructure) -> None:
        self.destroyed.append(infrastructure)

    def get_state(self) -> TerraformState:
        return TerraformState(resources=[], version="1.0")
