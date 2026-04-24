import pytest

from infrawatch.deployment.domain.models.rollout_status import RolloutStatus
from infrawatch.observability.domain.models.alert import Alert, AlertSeverity
from infrawatch.observability.domain.models.metric import Metric
from infrawatch.observability.domain.models.slo import SLO
from infrawatch.orchestrator.interfaces.i_deployment_module import IDeploymentModule
from infrawatch.orchestrator.interfaces.i_observability_module import IObservabilityModule
from infrawatch.orchestrator.interfaces.i_provisioning_module import IProvisioningModule
from infrawatch.orchestrator.interfaces.i_quality_module import IQualityModule
from infrawatch.orchestrator.orchestrator import Orchestrator
from infrawatch.provisioning.domain.models.infrastructure import Infrastructure, InfrastructureConfig, InfraStatus
from infrawatch.provisioning.domain.models.terraform_state import TerraformState
from infrawatch.quality.domain.models.quality_report import LintResult, QualityReport, RunResult, ScanResult


class FakeProvisioningModule(IProvisioningModule):
    def __init__(self) -> None:
        self.provisioned: list[InfrastructureConfig] = []

    def provision(self, config: InfrastructureConfig) -> Infrastructure:
        self.provisioned.append(config)
        return Infrastructure(id="infra-001", status=InfraStatus.READY)

    def destroy(self, infrastructure: Infrastructure) -> None:
        pass

    def get_state(self) -> TerraformState:
        return TerraformState(resources=[], version="1.0")


class FakeDeploymentModule(IDeploymentModule):
    def __init__(self) -> None:
        self.deployed: list[tuple[str, str]] = []

    def deploy(self, image: str, version: str) -> RolloutStatus:
        self.deployed.append((image, version))
        return RolloutStatus(ready=True, replicas=3, available=3)

    def rollback(self, deployment: object) -> RolloutStatus:
        return RolloutStatus(ready=True, replicas=3, available=3)

    def get_status(self, name: str) -> RolloutStatus:
        return RolloutStatus(ready=True, replicas=3, available=3)


class FakeObservabilityModule(IObservabilityModule):
    def collect_metrics(self, target: str) -> list[Metric]:
        return [Metric(name="up", value=1.0, labels={})]

    def check_slo(self, slo: SLO) -> bool:
        return True

    def fire_alert(self, alert: Alert) -> None:
        pass


class FakeQualityModule(IQualityModule):
    def run_lint(self, path: str) -> LintResult:
        return LintResult(passed=True, errors=[])

    def run_tests(self, path: str) -> RunResult:
        return RunResult(passed=True, total=10, failed=0, coverage=90.0)

    def run_security_scan(self, image: str) -> ScanResult:
        return ScanResult(passed=True, vulnerabilities=[])

    def quality_gate_passed(self, report: QualityReport) -> bool:
        return True


@pytest.fixture
def orchestrator() -> Orchestrator:
    return Orchestrator(
        provisioning=FakeProvisioningModule(),
        deployment=FakeDeploymentModule(),
        observability=FakeObservabilityModule(),
        quality=FakeQualityModule(),
    )


class TestOrchestrator:
    def test_provision_delegates_to_provisioning_module(self, orchestrator: Orchestrator) -> None:
        config = InfrastructureConfig(name="prod", region="eu-west-1")

        result = orchestrator.provision(config)

        assert isinstance(result, Infrastructure)
        assert result.is_ready()

    def test_deploy_delegates_to_deployment_module(self, orchestrator: Orchestrator) -> None:
        result = orchestrator.deploy(image="app", version="1.0")

        assert isinstance(result, RolloutStatus)
        assert result.is_ready()

    def test_check_quality_delegates_to_quality_module(self, orchestrator: Orchestrator) -> None:
        report = orchestrator.check_quality(path=".", image="app:1.0")

        assert isinstance(report, QualityReport)
        assert report.gate_passed()

    def test_collect_metrics_delegates_to_observability_module(self, orchestrator: Orchestrator) -> None:
        metrics = orchestrator.collect_metrics(target="localhost:9090")

        assert len(metrics) == 1
        assert metrics[0].name == "up"

    def test_orchestrator_never_imports_concrete_classes(self) -> None:
        import inspect
        import infrawatch.orchestrator.orchestrator as mod

        source = inspect.getsource(mod)

        assert "TerraformAdapter" not in source
        assert "KubectlAdapter" not in source
        assert "PrometheusAdapter" not in source
