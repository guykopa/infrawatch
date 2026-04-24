from infrawatch.quality.domain.models.quality_report import LintResult, QualityReport, ScanResult, RunResult


class TestLintResult:
    def test_lint_passed(self) -> None:
        result = LintResult(passed=True, errors=[])

        assert result.passed is True
        assert result.errors == []

    def test_lint_failed_with_errors(self) -> None:
        result = LintResult(passed=False, errors=["E501 line too long"])

        assert result.passed is False
        assert len(result.errors) == 1


class TestRunResult:
    def test_result_stores_counts_and_coverage(self) -> None:
        result = RunResult(passed=True, total=10, failed=0, coverage=95.0)

        assert result.total == 10
        assert result.failed == 0
        assert result.coverage == 95.0

    def test_result_failed_when_any_test_fails(self) -> None:
        result = RunResult(passed=False, total=10, failed=2, coverage=80.0)

        assert result.passed is False

    def test_coverage_meets_threshold(self) -> None:
        result = RunResult(passed=True, total=10, failed=0, coverage=85.0)

        assert result.coverage_meets(80.0) is True

    def test_coverage_does_not_meet_threshold(self) -> None:
        result = RunResult(passed=True, total=10, failed=0, coverage=75.0)

        assert result.coverage_meets(80.0) is False


class TestScanResult:
    def test_scan_passed_no_vulnerabilities(self) -> None:
        result = ScanResult(passed=True, vulnerabilities=[])

        assert result.passed is True
        assert result.vulnerabilities == []

    def test_scan_failed_with_vulnerabilities(self) -> None:
        result = ScanResult(passed=False, vulnerabilities=["CVE-2024-1234"])

        assert result.passed is False
        assert len(result.vulnerabilities) == 1


class TestQualityReport:
    def test_report_passes_when_all_pass(self) -> None:
        report = QualityReport(
            lint=LintResult(passed=True, errors=[]),
            tests=RunResult(passed=True, total=10, failed=0, coverage=90.0),
            scan=ScanResult(passed=True, vulnerabilities=[]),
        )

        assert report.gate_passed() is True

    def test_report_fails_when_lint_fails(self) -> None:
        report = QualityReport(
            lint=LintResult(passed=False, errors=["E501"]),
            tests=RunResult(passed=True, total=10, failed=0, coverage=90.0),
            scan=ScanResult(passed=True, vulnerabilities=[]),
        )

        assert report.gate_passed() is False

    def test_report_fails_when_tests_fail(self) -> None:
        report = QualityReport(
            lint=LintResult(passed=True, errors=[]),
            tests=RunResult(passed=False, total=10, failed=1, coverage=90.0),
            scan=ScanResult(passed=True, vulnerabilities=[]),
        )

        assert report.gate_passed() is False
