from infrawatch.quality.domain.exceptions.quality_error import QualityGateError
from infrawatch.quality.domain.models.quality_report import LintResult, QualityReport, RunResult, ScanResult
from infrawatch.quality.ports.i_linter import ILinter
from infrawatch.quality.ports.i_security_scanner import ISecurityScanner
from infrawatch.quality.ports.i_test_runner import ITestRunner


class QualityService:
    """Runs lint, tests, and security scans via injected port implementations."""

    def __init__(self, linter: ILinter, runner: ITestRunner, scanner: ISecurityScanner) -> None:
        self._linter = linter
        self._runner = runner
        self._scanner = scanner

    def run_lint(self, path: str) -> LintResult:
        return self._linter.lint(path)

    def run_tests(self, path: str) -> RunResult:
        return self._runner.run(path)

    def run_security_scan(self, image: str) -> ScanResult:
        return self._scanner.scan(image)

    def quality_gate_passed(self, report: QualityReport) -> bool:
        if not report.gate_passed():
            raise QualityGateError("Quality gate failed")
        return True
