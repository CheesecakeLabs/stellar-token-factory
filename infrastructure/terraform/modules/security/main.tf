locals {
  name_prefix  = var.name_prefix
  default_tags = merge(var.default_tags, { "ckl:alias" = "security" })

  # Objects that should be accessed by Load Balancer
  obj_frontend_security_group = distinct([
    for k, v in var.services_config : v.container_port if v.features.http && k != "kong"
  ])
}