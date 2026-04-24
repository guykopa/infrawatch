class DeploymentError(Exception):
    """Raised when a deployment fails to reach ready state."""


class RollbackError(Exception):
    """Raised when a rollback fails."""
