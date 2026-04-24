resource "kubernetes_config_map" "prometheus" {
  metadata {
    name      = "prometheus-config"
    namespace = var.namespace
  }

  data = {
    "prometheus.yml" = file("${path.module}/../../../monitoring/prometheus.yml")
  }
}
