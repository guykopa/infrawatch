infrawatch
==========

DevOps platform demonstrating the full infrastructure lifecycle of a cloud-ready
Python application. Covers provisioning (Terraform), deployment (Kubernetes),
observability (Prometheus, Grafana, OpenTelemetry), and quality (flake8, pytest, Trivy).

.. toctree::
   :maxdepth: 2
   :caption: Contents

Orchestrator
------------

.. automodule:: infrawatch.orchestrator.orchestrator
   :members:

Provisioning
------------

.. automodule:: infrawatch.provisioning.domain.services.provisioning_service
   :members:

.. automodule:: infrawatch.provisioning.domain.models.infrastructure
   :members:

Deployment
----------

.. automodule:: infrawatch.deployment.domain.services.deployment_service
   :members:

.. automodule:: infrawatch.deployment.domain.services.rollback_service
   :members:

Observability
-------------

.. automodule:: infrawatch.observability.domain.services.metrics_service
   :members:

.. automodule:: infrawatch.observability.domain.services.alert_service
   :members:

Quality
-------

.. automodule:: infrawatch.quality.domain.services.quality_service
   :members:
