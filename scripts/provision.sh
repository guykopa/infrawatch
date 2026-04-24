#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-infrawatch}"
REGION="${REGION:-eu-west-1}"

echo "==> Starting minikube"
minikube start --driver=docker

echo "==> Creating namespace"
kubectl apply -f k8s/namespace.yaml

echo "==> Running terraform init + apply"
cd terraform
terraform init -input=false
terraform plan -input=false -out=tfplan
terraform apply -input=false tfplan
cd ..

echo "==> Provisioning complete"
