variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
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
