resource "aws_db_instance" "postgres_db" {
  count = var.postgres_config.enable ? 1 : 0

  db_name    = replace(local.name_prefix, "-", "_")
  identifier = "${local.name_prefix}-postgres"

  engine         = "postgres"
  engine_version = var.postgres_config.engine_version
  password       = random_string.postgres_password.result
  username       = var.postgres_config.username

  instance_class                        = var.postgres_config.instance_type
  availability_zone                     = "${var.region}${var.availability_zone}"
  vpc_security_group_ids                = [var.security_group]
  db_subnet_group_name                  = aws_db_subnet_group.db_subnet.id
  backup_retention_period               = var.postgres_config.backup_retention_period
  allocated_storage                     = var.postgres_config.storage_size
  storage_encrypted                     = var.postgres_config.storage_encrypted
  multi_az                              = var.postgres_config.multi_az
  deletion_protection                   = var.postgres_config.deletion_protection
  enabled_cloudwatch_logs_exports       = var.postgres_config.monitoring_interval != 0 ? var.postgres_config.enabled_cloudwatch_logs_exports : null
  monitoring_interval                   = var.postgres_config.monitoring_interval
  monitoring_role_arn                   = var.postgres_config.monitoring_interval != 0 ? var.rds_monitoring_role.arn : null
  performance_insights_enabled          = var.postgres_config.performance_insights_enabled
  performance_insights_retention_period = var.postgres_config.performance_insights_retention_period
  maintenance_window                    = var.postgres_config.maintenance_window

  final_snapshot_identifier = replace("${local.name_prefix}-postgres-final-snapshot", "_", "-")

  tags = merge(local.default_tags, var.postgres_config.additional_tags)
}