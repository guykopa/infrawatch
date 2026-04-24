#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-infrawatch}"

echo "==> Emergency rollback on deployment/infrawatch-app"
kubectl rollout undo deployment/infrawatch-app -n "${NAMESPACE}"

echo "==> Waiting for rollback to complete"
kubectl rollout status deployment/infrawatch-app \
  -n "${NAMESPACE}" --timeout=120s

echo "==> Rollback complete"
