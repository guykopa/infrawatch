#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-infrawatch}"

echo "==> Pods"
kubectl get pods -n "${NAMESPACE}"

echo "==> Deployment status"
kubectl rollout status deployment/infrawatch-app -n "${NAMESPACE}"

echo "==> Service"
kubectl get svc -n "${NAMESPACE}"

echo "==> App /health"
APP_URL=$(kubectl get svc infrawatch-app -n "${NAMESPACE}" \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl --fail --silent "${APP_URL}/health"

echo "==> Health check passed"
