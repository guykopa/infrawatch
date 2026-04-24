import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)


def setup_tracing(otlp_endpoint: str) -> None:
    """Configure OpenTelemetry with OTLP exporter."""
    provider = TracerProvider()
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)


def setup_instrumentation(app: FastAPI, otlp_endpoint: str | None = None) -> None:
    """Attach Prometheus metrics and OpenTelemetry tracing middleware."""
    if otlp_endpoint:
        setup_tracing(otlp_endpoint)

    tracer = trace.get_tracer(__name__)

    @app.middleware("http")
    async def track_request(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start = time.monotonic()
        with tracer.start_as_current_span(f"{request.method} {request.url.path}"):
            response = await call_next(request)
        duration = time.monotonic() - start

        REQUEST_COUNT.labels(
            method=request.method,
            path=request.url.path,
            status=response.status_code,
        ).inc()
        REQUEST_LATENCY.labels(
            method=request.method,
            path=request.url.path,
        ).observe(duration)

        response.headers["X-Response-Time"] = f"{duration:.4f}s"
        return response
