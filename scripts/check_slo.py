#!/usr/bin/env python3
"""Check SLO: error rate must stay below 5%."""
import json
import logging
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

PROMETHEUS_URL = os.environ["PROMETHEUS_URL"]
THRESHOLD = 0.05


def query_prometheus(url: str, promql: str) -> list:
    """Query Prometheus instant query API and return result list."""
    full_url = f"{url}/api/v1/query?query={urllib.parse.quote(promql)}"
    with urllib.request.urlopen(full_url, timeout=10) as resp:
        return json.load(resp).get("data", {}).get("result", [])


def main() -> None:
    """Check error rate SLO against Prometheus and exit 1 if breached."""
    try:
        data = query_prometheus(
            PROMETHEUS_URL,
            "rate(http_requests_total{status=~'5..'}[5m])",
        )
    except urllib.error.URLError as exc:
        logging.error("Cannot reach Prometheus at %s: %s", PROMETHEUS_URL, exc)
        sys.exit(1)

    rate = float(data[0]["value"][1]) if data else 0.0

    if rate > THRESHOLD:
        logging.error("SLO breached: error_rate=%.4f > %.2f", rate, THRESHOLD)
        sys.exit(1)

    logging.info("SLO ok: error_rate=%.4f", rate)


if __name__ == "__main__":
    main()
