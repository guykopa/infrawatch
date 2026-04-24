from infrawatch.provisioning.domain.models.terraform_state import TerraformState


class TestTerraformState:
    def test_state_stores_version_and_resources(self) -> None:
        state = TerraformState(resources=[], version="1.0")

        assert state.version == "1.0"
        assert state.resources == []

    def test_state_is_empty_when_no_resources(self) -> None:
        state = TerraformState(resources=[], version="1.0")

        assert state.is_empty() is True

    def test_state_is_not_empty_when_has_resources(self) -> None:
        state = TerraformState(resources=["vpc-001"], version="1.0")

        assert state.is_empty() is False

    def test_state_resource_count(self) -> None:
        state = TerraformState(resources=["vpc-001", "subnet-001"], version="1.0")

        assert state.resource_count() == 2
