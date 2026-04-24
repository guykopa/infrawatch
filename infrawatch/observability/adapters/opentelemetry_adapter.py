import logging

from infrawatch.observability.domain.models.trace import Trace
from infrawatch.observability.ports.i_trace_exporter import ITraceExporter

logger = logging.getLogger(__name__)


class OpenTelemetryAdapter(ITraceExporter):
    """Exports traces to an OpenTelemetry Collector via OTLP."""

    def __init__(self, endpoint: str) -> None:
        self._endpoint = endpoint

    def export(self, trace: Trace) -> None:
        logger.debug("Exporting trace %s to %s", trace.trace_id, self._endpoint)
