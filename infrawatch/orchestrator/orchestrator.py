from infrawatch.observability.domain.models.metric import Metric
from infrawatch.orchestrator.interfaces.i_deployment_module import IDeploymentModule
from infrawatch.orchestrator.interfaces.i_observability_module import IObservabilityModule
from infrawatch.orchestrator.interfaces.i_provisioning_module import IProvisioningModule
from infrawatch.orchestrator.interfaces.i_quality_module import IQualityModule
from infrawatch.provisioning.domain.models.infrastructure import Infrastructure, InfrastructureConfig
from infrawatch.deployment.domain.models.rollout_status import RolloutStatus
from infrawatch.quality.domain.models.quality_report import QualityReport


class Orchestrator:
    """Coordinates all domain modules. Depends only on module interfaces."""

    def __init__(
        self,
        provisioning: IProvisioningModule,
        deployment: IDeploymentModule,
        observability: IObservabilityModule,
        quality: IQualityModule,
    ) -> None:
        self._provisioning = provisioning
        self._deployment = deployment
        self._observability = observability
        self._quality = quality

    def provision(self, config: InfrastructureConfig) -> Infrastructure:
        return self._provisioning.provision(config)

    def deploy(self, image: str, version: str) -> RolloutStatus:
        return self._deployment.deploy(image, version)

    def collect_metrics(self, target: str) -> list[Metric]:
        return self._observability.collect_metrics(target)

    def check_quality(self, path: str, image: str) -> QualityReport:
        lint = self._quality.run_lint(path)
        tests = self._quality.run_tests(path)
        scan = self._quality.run_security_scan(image)
        return QualityReport(lint=lint, tests=tests, scan=scan)
