from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.quality.domain.models.quality_report import RunResult


class ITestRunner(ABC):
    """Contract for test runner backends (pytest, etc.)."""

    @abstractmethod
    def run(self, path: str) -> RunResult: ...
