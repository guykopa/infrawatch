import json
import logging
import subprocess

from infrawatch.quality.domain.models.quality_report import ScanResult
from infrawatch.quality.ports.i_security_scanner import ISecurityScanner

logger = logging.getLogger(__name__)


class TrivyAdapter(ISecurityScanner):
    """Runs Trivy to scan container images for vulnerabilities."""

    def scan(self, image: str) -> ScanResult:
        result = subprocess.run(
            ["trivy", "image", "--format", "json", "--exit-code", "0", image],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            logger.error("trivy scan failed: %s", result.stderr)
            return ScanResult(passed=False, vulnerabilities=["trivy execution failed"])
        try:
            data = json.loads(result.stdout)
            vulns = [
                f"{v['VulnerabilityID']} ({v['Severity']})"
                for r in data.get("Results", [])
                for v in r.get("Vulnerabilities", [])
                if v.get("Severity") in ("CRITICAL", "HIGH")
            ]
        except (json.JSONDecodeError, KeyError):
            vulns = []
        return ScanResult(passed=len(vulns) == 0, vulnerabilities=vulns)
