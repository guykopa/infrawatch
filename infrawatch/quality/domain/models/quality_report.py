from dataclasses import dataclass, field


@dataclass(frozen=True)
class LintResult:
    """Result of a linting run."""

    passed: bool
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RunResult:
    """Result of a test suite run."""

    passed: bool
    total: int
    failed: int
    coverage: float

    def coverage_meets(self, threshold: float) -> bool:
        return self.coverage >= threshold


@dataclass(frozen=True)
class ScanResult:
    """Result of a security scan."""

    passed: bool
    vulnerabilities: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class QualityReport:
    """Aggregated quality gate report."""

    lint: LintResult
    tests: RunResult
    scan: ScanResult

    def gate_passed(self) -> bool:
        return self.lint.passed and self.tests.passed and self.scan.passed
