import logging
import subprocess

from infrawatch.quality.domain.models.quality_report import LintResult
from infrawatch.quality.ports.i_linter import ILinter

logger = logging.getLogger(__name__)


class Flake8Adapter(ILinter):
    """Runs flake8 to lint Python source code."""

    def lint(self, path: str) -> LintResult:
        result = subprocess.run(
            ["flake8", path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            errors = [line for line in result.stdout.splitlines() if line]
            logger.warning("flake8 found %d issue(s)", len(errors))
            return LintResult(passed=False, errors=errors)
        return LintResult(passed=True, errors=[])
