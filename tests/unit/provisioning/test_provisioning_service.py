import pytest

from infrawatch.provisioning.domain.exceptions.provisioning_error import ProvisioningError
from infrawatch.provisioning.domain.models.infrastructure import Infrastructure, InfrastructureConfig, InfraStatus
from infrawatch.provisioning.domain.models.terraform_state import TerraformState
from infrawatch.provisioning.domain.services.provisioning_service import ProvisioningService
from infrawatch.provisioning.ports.i_infra_provider import IInfraProvider
from tests.conftest import FakeInfraProvider


class TestProvisioningService:
    def test_provision_delegates_to_provider(self, fake_infra_provider: FakeInfraProvider) -> None:
        service = ProvisioningService(provider=fake_infra_provider)
        config = InfrastructureConfig(name="prod", region="eu-west-1")

        result = service.provision(config)

        assert isinstance(result, Infrastructure)
        assert result.is_ready()
        assert config in fake_infra_provider.provisioned

    def test_destroy_delegates_to_provider(self, fake_infra_provider: FakeInfraProvider) -> None:
        service = ProvisioningService(provider=fake_infra_provider)
        infra = Infrastructure(id="infra-001", status=InfraStatus.READY)

        service.destroy(infra)

        assert infra in fake_infra_provider.destroyed

    def test_get_state_delegates_to_provider(self, fake_infra_provider: FakeInfraProvider) -> None:
        service = ProvisioningService(provider=fake_infra_provider)

        state = service.get_state()

        assert isinstance(state, TerraformState)

    def test_provision_raises_when_result_not_ready(self) -> None:
        class FailingProvider(IInfraProvider):
            def apply(self, config: InfrastructureConfig) -> Infrastructure:
                return Infrastructure(id="fail-001", status=InfraStatus.FAILED)

            def destroy(self, infrastructure: Infrastructure) -> None:
                pass

            def get_state(self) -> TerraformState:
                return TerraformState(resources=[], version="1.0")

        service = ProvisioningService(provider=FailingProvider())
        config = InfrastructureConfig(name="prod", region="eu-west-1")

        with pytest.raises(ProvisioningError):
            service.provision(config)
