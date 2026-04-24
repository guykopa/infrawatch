import logging
import re
import subprocess

from infrawatch.quality.domain.models.quality_report import RunResult
from infrawatch.quality.ports.i_test_runner import ITestRunner

logger = logging.getLogger(__name__)

_SUMMARY_RE = re.compile(r"(\d+) passed")
_FAILED_RE = re.compile(r"(\d+) failed")
_COVERAGE_RE = re.compile(r"TOTAL\s+\d+\s+\d+\s+(\d+)%")


class PytestAdapter(ITestRunner):
    """Runs pytest with coverage reporting."""

    def run(self, path: str) -> RunResult:
        result = subprocess.run(
            ["pytest", path, "--cov", "--cov-report=term-missing", "-q"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = result.stdout + result.stderr
        passed_match = _SUMMARY_RE.search(output)
        failed_match = _FAILED_RE.search(output)
        passed = int(passed_match.group(1)) if passed_match else 0
        failed = int(failed_match.group(1)) if failed_match else 0
        coverage_match = _COVERAGE_RE.search(output)
        coverage = float(coverage_match.group(1)) if coverage_match else 0.0
        return RunResult(
            passed=result.returncode == 0,
            total=passed + failed,
            failed=failed,
            coverage=coverage,
        )
