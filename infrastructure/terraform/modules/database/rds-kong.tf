resource "aws_db_instance" "kong" {
  count      = var.kong_config.enabled && var.kong_config.rds.enabled ? 1 : 0
  identifier = format("%s-kong", local.name_prefix)


  engine            = "postgres"
  db_name           = replace(format("%s_kong", local.name_prefix), "-", "_")
  engine_version    = var.kong_config.rds.db_engine_version
  instance_class    = var.kong_config.rds.db_instance_class
  allocated_storage = var.kong_config.rds.db_storage_size
  storage_type      = "gp2"
  storage_encrypted = var.kong_config.rds.storage_encrypted

  backup_retention_period = var.kong_config.rds.db_backup_retention_period
  db_subnet_group_name    = aws_db_subnet_group.db_subnet.id
  multi_az                = var.kong_config.rds.db_multi_az
  parameter_group_name    = format("%s-kong", local.name_prefix)
  maintenance_window      = var.kong_config.rds.maintenance_window

  monitoring_interval             = var.kong_config.rds.monitoring_interval
  monitoring_role_arn             = var.kong_config.rds.monitoring_interval != 0 ? var.rds_monitoring_role.arn : null
  enabled_cloudwatch_logs_exports = var.kong_config.rds.monitoring_interval != 0 ? var.kong_config.rds.enabled_cloudwatch_logs_exports : null

  performance_insights_enabled          = var.kong_config.rds.performance_insights_enabled
  performance_insights_retention_period = var.kong_config.rds.performance_insights_retention_period

  username = "kong"
  password = random_string.kong_password.result

  vpc_security_group_ids = [var.kong_config.security_group]

  skip_final_snapshot       = false
  final_snapshot_identifier = replace("${local.name_prefix}-kong-final-snapshot", "_", "-")

  tags = merge({ "Name" = format("%s-kong", local.name_prefix) }, local.default_tags, var.postgres_config.additional_tags)

  depends_on = [var.kong_config]
}

resource "aws_db_parameter_group" "kong" {
  count = var.kong_config.enabled && var.kong_config.rds.enabled ? 1 : 0

  name        = format("%s-kong", local.name_prefix)
  family      = var.kong_config.rds.db_family
  description = var.kong_config.rds.description

  lifecycle {
    create_before_destroy = true
  }

  tags = merge({ "Name" = format("%s-kong", local.name_prefix) }, local.default_tags)
}