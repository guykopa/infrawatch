class MetricsUnavailableError(Exception):
    """Raised when the metrics backend cannot be reached."""


class AlertError(Exception):
    """Raised when firing or resolving an alert fails."""
