terraform {
  required_version = ">= 0.13"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.10"
    }
  }
}


locals {
  name_prefix  = var.name_prefix
  default_tags = merge(var.default_tags, { "ckl:alias" = "cluster" })
}

resource "aws_ecs_cluster" "cluster" {
  name = local.name_prefix

  tags = local.default_tags

  depends_on = [var.ecs_instance_role]
}
