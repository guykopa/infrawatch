from dataclasses import dataclass, field


@dataclass(frozen=True)
class TerraformState:
    """Snapshot of the current Terraform-managed infrastructure state."""

    version: str
    resources: list[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        return len(self.resources) == 0

    def resource_count(self) -> int:
        return len(self.resources)
