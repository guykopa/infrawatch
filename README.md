# infrawatch

DevOps platform demonstrating the full infrastructure lifecycle of a cloud-ready Python application.

## Stack

Python 3.11 · FastAPI · Terraform · Kubernetes (minikube) · Prometheus · Grafana · OpenTelemetry · Trivy · GitHub Actions · GHCR · Docker

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -r app/requirements.txt
pytest tests/unit/ app/tests/ -q
```

## Local dev with Docker Compose

Start the full stack locally (app + Prometheus + Grafana + OTel Collector):

```bash
docker compose -f docker/docker-compose.yml up -d
```

| Service | URL |
|---------|-----|
| FastAPI app | http://localhost:8000 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 (admin/admin) |
| OTel Collector | grpc://localhost:4317 |

## Commands

| Command | Description |
|---------|-------------|
| `pytest tests/unit/ app/tests/ -q` | Run unit tests |
| `pytest tests/integration/ -v --timeout=120` | Run integration tests (requires minikube + Terraform) |
| `flake8 infrawatch/ app/` | Lint |
| `mypy infrawatch/ app/` | Type check |
| `./scripts/provision.sh` | Bootstrap cluster + terraform apply |
| `./scripts/deploy.sh` | Build + push + kubectl apply |
| `./scripts/rollback.sh` | Emergency rollback |
| `./scripts/health_check.sh` | Full cluster health check |
| `python3 scripts/check_slo.py` | Check SLO against Prometheus |
| `cd docs && make html` | Build Sphinx documentation |

## CI/CD

Workflows run on a self-hosted GitHub Actions runner. Images are pushed to GHCR.

| Workflow | Trigger | What it does |
|----------|---------|-------------|
| `ci.yml` | push to any branch | lint, test, build, security scan |
| `cd-staging.yml` | push to main | terraform + deploy to staging namespace |
| `cd-prod.yml` | git tag `vX.Y.Z` | deploy to prod + SLO check + auto-rollback |

### Runner setup

```bash
mkdir actions-runner && cd actions-runner
# Download and configure from GitHub → Settings → Actions → Runners
./config.sh --url https://github.com/<org>/<repo> --token <TOKEN>
sudo ./svc.sh install && sudo ./svc.sh start
```

### Required GitHub secrets and variables

| Name | Type | Scope |
|------|------|-------|
| `REGISTRY_USER` | Secret | Repository |
| `REGISTRY_PASSWORD` | Secret | Repository |
| `KUBECONFIG_STAGING` | Secret | Environment: staging |
| `KUBECONFIG_PROD` | Secret | Environment: production |
| `PROMETHEUS_URL` | Variable | Repository |

## Architecture

Modular Hexagonal Architecture — 4 independent domains coordinated by an Orchestrator.
See [ARCHITECTURE.md](ARCHITECTURE.md) for full details.
