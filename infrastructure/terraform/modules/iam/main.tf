locals {
  name_prefix  = var.name_prefix
  default_tags = merge(var.default_tags, { "ckl:alias" = "iam" })

}