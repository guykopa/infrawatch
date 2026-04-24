#!/usr/bin/env bash
set -euo pipefail

IMAGE="${IMAGE:?IMAGE is required}"
VERSION="${VERSION:?VERSION is required}"
NAMESPACE="${NAMESPACE:-infrawatch}"

echo "==> Rolling update to ${IMAGE}:${VERSION}"
kubectl set image deployment/infrawatch-app \
  infrawatch-app="${IMAGE}:${VERSION}" \
  -n "${NAMESPACE}"

echo "==> Waiting for rollout (zero-downtime)"
kubectl rollout status deployment/infrawatch-app \
  -n "${NAMESPACE}" --timeout=120s

echo "==> Update complete"
