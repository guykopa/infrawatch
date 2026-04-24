variable "kubeconfig_path" {
  description = "Path to the kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "infrawatch"
}

variable "image" {
  description = "Docker image to deploy"
  type        = string
}

variable "replicas" {
  description = "Number of pod replicas"
  type        = number
  default     = 2
}
