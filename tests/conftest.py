import pytest

from infrawatch.deployment.domain.models.deployment import Deployment, Pod, PodStatus
from infrawatch.deployment.domain.models.rollout_status import RolloutStatus
from infrawatch.deployment.ports.i_container_orchestrator import IContainerOrchestrator
from infrawatch.deployment.ports.i_image_registry import IImageRegistry
from infrawatch.observability.domain.models.alert import Alert
from infrawatch.observability.domain.models.metric import Metric
from infrawatch.observability.domain.models.slo import SLO
from infrawatch.observability.ports.i_alert_manager import IAlertManager
from infrawatch.observability.ports.i_metrics_collector import IMetricsCollector
from infrawatch.observability.ports.i_trace_exporter import ITraceExporter
from infrawatch.provisioning.domain.models.infrastructure import Infrastructure, InfrastructureConfig, InfraStatus
from infrawatch.provisioning.domain.models.terraform_state import TerraformState
from infrawatch.provisioning.ports.i_infra_provider import IInfraProvider
from infrawatch.quality.domain.models.quality_report import LintResult, QualityReport, ScanResult, RunResult
from infrawatch.quality.ports.i_linter import ILinter
from infrawatch.quality.ports.i_security_scanner import ISecurityScanner
from infrawatch.quality.ports.i_test_runner import ITestRunner


class FakeInfraProvider(IInfraProvider):
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


class FakeOrchestratorAdapter(IContainerOrchestrator):
    def __init__(self) -> None:
        self.applied: list[str] = []
        self.rolled_back: list[Deployment] = []

    def apply(self, manifest: str) -> RolloutStatus:
        self.applied.append(manifest)
        return RolloutStatus(ready=True, replicas=3, available=3)

    def rollback(self, deployment: Deployment) -> RolloutStatus:
        self.rolled_back.append(deployment)
        return RolloutStatus(ready=True, replicas=3, available=3)

    def get_pod_status(self, name: str) -> list[Pod]:
        return [Pod(name=f"{name}-abc", status=PodStatus.RUNNING)]


class FakeImageRegistry(IImageRegistry):
    def __init__(self) -> None:
        self.pushed: list[tuple[str, str]] = []

    def push(self, image: str, tag: str) -> str:
        self.pushed.append((image, tag))
        return f"{image}:{tag}"

    def image_exists(self, image: str, tag: str) -> bool:
        return (image, tag) in self.pushed


class FakeMetricsCollector(IMetricsCollector):
    def __init__(self, metrics: list[Metric] | None = None) -> None:
        self._metrics = metrics or []

    def collect(self, target: str) -> list[Metric]:
        return self._metrics


class FakeTraceExporter(ITraceExporter):
    def __init__(self) -> None:
        self.exported: list[object] = []

    def export(self, trace: object) -> None:
        self.exported.append(trace)


class FakeAlertManager(IAlertManager):
    def __init__(self) -> None:
        self.fired: list[Alert] = []
        self.resolved: list[Alert] = []

    def fire(self, alert: Alert) -> None:
        self.fired.append(alert)

    def resolve(self, alert: Alert) -> None:
        self.resolved.append(alert)


class FakeLinter(ILinter):
    def __init__(self, result: LintResult | None = None) -> None:
        self._result = result or LintResult(passed=True, errors=[])

    def lint(self, path: str) -> LintResult:
        return self._result


class FakeTestRunner(ITestRunner):
    def __init__(self, result: RunResult | None = None) -> None:
        self._result = result or RunResult(passed=True, total=1, failed=0, coverage=100.0)

    def run(self, path: str) -> RunResult:
        return self._result


class FakeSecurityScanner(ISecurityScanner):
    def __init__(self, result: ScanResult | None = None) -> None:
        self._result = result or ScanResult(passed=True, vulnerabilities=[])

    def scan(self, image: str) -> ScanResult:
        return self._result


@pytest.fixture
def fake_infra_provider() -> FakeInfraProvider:
    return FakeInfraProvider()


@pytest.fixture
def fake_orchestrator() -> FakeOrchestratorAdapter:
    return FakeOrchestratorAdapter()


@pytest.fixture
def fake_image_registry() -> FakeImageRegistry:
    return FakeImageRegistry()


@pytest.fixture
def fake_metrics_collector() -> FakeMetricsCollector:
    return FakeMetricsCollector()


@pytest.fixture
def fake_trace_exporter() -> FakeTraceExporter:
    return FakeTraceExporter()


@pytest.fixture
def fake_alert_manager() -> FakeAlertManager:
    return FakeAlertManager()


@pytest.fixture
def fake_linter() -> FakeLinter:
    return FakeLinter()


@pytest.fixture
def fake_test_runner() -> FakeTestRunner:
    return FakeTestRunner()


@pytest.fixture
def fake_security_scanner() -> FakeSecurityScanner:
    return FakeSecurityScanner()
