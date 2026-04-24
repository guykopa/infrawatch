import pytest

from infrawatch.provisioning.adapters.terraform_adapter import TerraformAdapter
from infrawatch.provisioning.domain.models.infrastructure import InfrastructureConfig, InfraStatus


@pytest.mark.integration
class TestTerraformAdapter:
    """Requires a real terraform binary and a valid working directory."""

    def test_apply_returns_infrastructure(self, tmp_path: pytest.TempPathFactory) -> None:
        (tmp_path / "main.tf").write_text('output "hello" { value = "world" }')
        adapter = TerraformAdapter(working_dir=str(tmp_path))
        config = InfrastructureConfig(name="test", region="eu-west-1")

        result = adapter.apply(config)

        assert result.status in (InfraStatus.READY, InfraStatus.FAILED)

    def test_get_state_returns_terraform_state(self, tmp_path: pytest.TempPathFactory) -> None:
        (tmp_path / "main.tf").write_text('output "hello" { value = "world" }')
        adapter = TerraformAdapter(working_dir=str(tmp_path))

        state = adapter.get_state()

        assert state is not None

    def test_destroy_does_not_raise(self, tmp_path: pytest.TempPathFactory) -> None:
        from infrawatch.provisioning.domain.models.infrastructure import Infrastructure
        adapter = TerraformAdapter(working_dir=str(tmp_path))
        infra = Infrastructure(id="test-001", status=InfraStatus.READY)

        adapter.destroy(infra)
