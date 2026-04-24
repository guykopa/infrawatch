resource "kubernetes_namespace" "infrawatch" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_deployment" "app" {
  metadata {
    name      = "infrawatch-app"
    namespace = kubernetes_namespace.infrawatch.metadata[0].name
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = { app = "infrawatch-app" }
    }

    template {
      metadata {
        labels = { app = "infrawatch-app" }
      }

      spec {
        container {
          name              = "infrawatch-app"
          image             = var.image
          image_pull_policy = "Never"

          port { container_port = 8000 }

          resources {
            requests = { cpu = "100m", memory = "128Mi" }
            limits   = { cpu = "500m", memory = "256Mi" }
          }
        }
      }
    }
  }
}
