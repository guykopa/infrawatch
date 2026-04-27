terraform {
  required_version = ">= 1.5"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
  backend "local" {}
}

provider "kubernetes" {
  config_path = var.kubeconfig_path
}

module "kubernetes" {
  source    = "./modules/kubernetes"
  namespace = var.namespace
  image     = var.image
  replicas  = var.replicas
}

module "monitoring" {
  source    = "./modules/monitoring"
  namespace = var.namespace
}
