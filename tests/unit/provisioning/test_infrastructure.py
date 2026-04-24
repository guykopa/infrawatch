import pytest

from infrawatch.provisioning.domain.models.infrastructure import (
    Infrastructure,
    InfrastructureConfig,
    InfraStatus,
)


class TestInfrastructureConfig:
    def test_config_stores_name_and_region(self) -> None:
        config = InfrastructureConfig(name="prod", region="eu-west-1")

        assert config.name == "prod"
        assert config.region == "eu-west-1"

    def test_config_requires_name(self) -> None:
        with pytest.raises(TypeError):
            InfrastructureConfig(region="eu-west-1")  # type: ignore[call-arg]

    def test_config_requires_region(self) -> None:
        with pytest.raises(TypeError):
            InfrastructureConfig(name="prod")  # type: ignore[call-arg]


class TestInfraStatus:
    def test_has_ready_status(self) -> None:
        assert InfraStatus.READY

    def test_has_pending_status(self) -> None:
        assert InfraStatus.PENDING

    def test_has_failed_status(self) -> None:
        assert InfraStatus.FAILED

    def test_has_destroyed_status(self) -> None:
        assert InfraStatus.DESTROYED


class TestInfrastructure:
    def test_infrastructure_stores_id_and_status(self) -> None:
        infra = Infrastructure(id="infra-001", status=InfraStatus.READY)

        assert infra.id == "infra-001"
        assert infra.status == InfraStatus.READY

    def test_infrastructure_is_ready(self) -> None:
        infra = Infrastructure(id="infra-001", status=InfraStatus.READY)

        assert infra.is_ready() is True

    def test_infrastructure_not_ready_when_pending(self) -> None:
        infra = Infrastructure(id="infra-001", status=InfraStatus.PENDING)

        assert infra.is_ready() is False

    def test_infrastructure_not_ready_when_failed(self) -> None:
        infra = Infrastructure(id="infra-001", status=InfraStatus.FAILED)

        assert infra.is_ready() is False

    def test_two_infrastructures_with_same_id_are_equal(self) -> None:
        infra_a = Infrastructure(id="infra-001", status=InfraStatus.READY)
        infra_b = Infrastructure(id="infra-001", status=InfraStatus.READY)

        assert infra_a == infra_b

    def test_two_infrastructures_with_different_ids_are_not_equal(self) -> None:
        infra_a = Infrastructure(id="infra-001", status=InfraStatus.READY)
        infra_b = Infrastructure(id="infra-002", status=InfraStatus.READY)

        assert infra_a != infra_b
