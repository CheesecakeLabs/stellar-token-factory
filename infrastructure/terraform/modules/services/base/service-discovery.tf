resource "aws_service_discovery_service" "sd" {
  count = local.features.service_discovery ? 1 : 0

  name = var.alias_name

  dns_config {
    namespace_id = var.service_config.service_discovery_dns_namespace
    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }

  tags = local.default_tags
}
