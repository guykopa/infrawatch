from infrawatch.quality.domain.models.quality_report import LintResult, RunResult, ScanResult
from infrawatch.quality.ports.i_linter import ILinter
from infrawatch.quality.ports.i_security_scanner import ISecurityScanner
from infrawatch.quality.ports.i_test_runner import ITestRunner


class FakeLinterAdapter(ILinter):
    """In-memory ILinter for use in unit tests."""

    def __init__(self, result: LintResult | None = None) -> None:
        self._result = result or LintResult(passed=True, errors=[])

    def lint(self, path: str) -> LintResult:
        return self._result


class FakeTestRunnerAdapter(ITestRunner):
    """In-memory ITestRunner for use in unit tests."""

    def __init__(self, result: RunResult | None = None) -> None:
        self._result = result or RunResult(passed=True, total=1, failed=0, coverage=100.0)

    def run(self, path: str) -> RunResult:
        return self._result


class FakeSecurityScannerAdapter(ISecurityScanner):
    """In-memory ISecurityScanner for use in unit tests."""

    def __init__(self, result: ScanResult | None = None) -> None:
        self._result = result or ScanResult(passed=True, vulnerabilities=[])

    def scan(self, image: str) -> ScanResult:
        return self._result
