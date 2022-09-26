resource "aws_cloudwatch_log_group" "logs" {
  name              = "${local.name_prefix}-${var.alias_name}"
  retention_in_days = var.service_config.log_retention

  tags = local.default_tags
}
