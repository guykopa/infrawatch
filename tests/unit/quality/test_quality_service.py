from infrawatch.quality.domain.exceptions.quality_error import QualityGateError
from infrawatch.quality.domain.models.quality_report import LintResult, QualityReport, RunResult, ScanResult
from infrawatch.quality.domain.services.quality_service import QualityService
from tests.conftest import FakeLinter, FakeSecurityScanner, FakeTestRunner
import pytest


class TestQualityService:
    def test_run_lint_delegates_to_linter(self, fake_linter: FakeLinter) -> None:
        service = QualityService(linter=fake_linter, runner=FakeTestRunner(), scanner=FakeSecurityScanner())

        result = service.run_lint(".")

        assert isinstance(result, LintResult)
        assert result.passed is True

    def test_run_tests_delegates_to_runner(self, fake_test_runner: FakeTestRunner) -> None:
        service = QualityService(linter=FakeLinter(), runner=fake_test_runner, scanner=FakeSecurityScanner())

        result = service.run_tests(".")

        assert isinstance(result, RunResult)
        assert result.passed is True

    def test_run_security_scan_delegates_to_scanner(self, fake_security_scanner: FakeSecurityScanner) -> None:
        service = QualityService(linter=FakeLinter(), runner=FakeTestRunner(), scanner=fake_security_scanner)

        result = service.run_security_scan("app:1.0")

        assert isinstance(result, ScanResult)
        assert result.passed is True

    def test_quality_gate_passed_when_all_pass(self) -> None:
        service = QualityService(linter=FakeLinter(), runner=FakeTestRunner(), scanner=FakeSecurityScanner())
        report = QualityReport(
            lint=LintResult(passed=True, errors=[]),
            tests=RunResult(passed=True, total=10, failed=0, coverage=90.0),
            scan=ScanResult(passed=True, vulnerabilities=[]),
        )

        assert service.quality_gate_passed(report) is True

    def test_quality_gate_raises_when_fails(self) -> None:
        service = QualityService(linter=FakeLinter(), runner=FakeTestRunner(), scanner=FakeSecurityScanner())
        report = QualityReport(
            lint=LintResult(passed=False, errors=["E501"]),
            tests=RunResult(passed=True, total=10, failed=0, coverage=90.0),
            scan=ScanResult(passed=True, vulnerabilities=[]),
        )

        with pytest.raises(QualityGateError):
            service.quality_gate_passed(report)
