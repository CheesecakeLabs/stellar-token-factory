locals {
  name_prefix  = var.name_prefix
  default_tags = merge(var.default_tags, { "ckl:alias" = "database" })
}

resource "aws_db_subnet_group" "db_subnet" {
  name       = "${local.name_prefix}-db-subnet"
  subnet_ids = var.subnet_ids
}