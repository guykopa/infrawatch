from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.quality.domain.models.quality_report import LintResult


class ILinter(ABC):
    """Contract for linting backends (flake8, mypy, etc.)."""

    @abstractmethod
    def lint(self, path: str) -> LintResult: ...
