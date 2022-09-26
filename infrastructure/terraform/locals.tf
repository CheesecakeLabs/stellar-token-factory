locals {
  # This project is designed to work with Terraform Workspace
  environment = terraform.workspace

  # A name prefix to use in all created resources
  name_prefix = "${var.project_name}-${local.environment}"

  # Default TAGs to apply in all created resources
  default_tags = merge({
    "ckl:environment" = "${local.environment}"
    "ckl:project"     = "${var.project_name}"
    "ckl:name_prefix" = "${local.name_prefix}"
    "ckl:managed_by"  = "Terraform"
  }, var.additional_tags)

  # Create Service Discovery Private DNS Namespace if some service require
  create_service_discovery_dns_namespace = contains([for sd in var.services_config : sd.features.service_discovery], true)

  account_id = data.aws_caller_identity.current.account_id

}

data "aws_caller_identity" "current" {}