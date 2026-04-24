from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrawatch.quality.domain.models.quality_report import ScanResult


class ISecurityScanner(ABC):
    """Contract for security scanning backends (Trivy, etc.)."""

    @abstractmethod
    def scan(self, image: str) -> ScanResult: ...
