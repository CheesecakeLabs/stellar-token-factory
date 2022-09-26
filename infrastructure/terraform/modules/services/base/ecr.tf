resource "aws_ecr_repository" "ecr_repo" {
  name = "${local.name_prefix}-${var.alias_name}"

  tags = local.default_tags
}
