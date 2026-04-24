#!/usr/bin/env bash
set -euo pipefail

IMAGE="${IMAGE:-infrawatch-app}"
VERSION="${VERSION:-latest}"
NAMESPACE="${NAMESPACE:-infrawatch}"

echo "==> Building Docker image ${IMAGE}:${VERSION}"
docker build -t "${IMAGE}:${VERSION}" -f docker/Dockerfile .

echo "==> Pushing image"
docker push "${IMAGE}:${VERSION}"

echo "==> Applying k8s manifests"
kubectl apply -f k8s/ -n "${NAMESPACE}"

echo "==> Waiting for rollout"
kubectl rollout status deployment/infrawatch-app -n "${NAMESPACE}" --timeout=120s

echo "==> Deploy complete: ${IMAGE}:${VERSION}"
