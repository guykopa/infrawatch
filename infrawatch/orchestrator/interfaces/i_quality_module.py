from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.quality.domain.models.quality_report import LintResult, QualityReport, ScanResult, RunResult


class IQualityModule(ABC):
    """Contract for the quality module."""

    @abstractmethod
    def run_lint(self, path: str) -> LintResult: ...

    @abstractmethod
    def run_tests(self, path: str) -> RunResult: ...

    @abstractmethod
    def run_security_scan(self, image: str) -> ScanResult: ...

    @abstractmethod
    def quality_gate_passed(self, report: QualityReport) -> bool: ...
