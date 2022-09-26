resource "aws_db_instance" "mariadb_db" {
  count = var.mariadb_config.enable ? 1 : 0

  #name       = replace(local.name_prefix, "-", "_")
  identifier = "${local.name_prefix}-mariadb"

  engine         = "mariadb"
  engine_version = "10.5.13"
  password       = random_string.mariadb_password.result
  username       = var.mariadb_config.username

  instance_class                        = var.mariadb_config.instance_type
  availability_zone                     = "${var.region}${var.availability_zone}"
  vpc_security_group_ids                = [var.security_group]
  db_subnet_group_name                  = aws_db_subnet_group.db_subnet.id
  backup_retention_period               = var.mariadb_config.backup_retention_period
  allocated_storage                     = var.mariadb_config.storage_size
  storage_encrypted                     = var.mariadb_config.storage_encrypted
  multi_az                              = var.mariadb_config.multi_az
  deletion_protection                   = var.mariadb_config.deletion_protection
  enabled_cloudwatch_logs_exports       = var.mariadb_config.monitoring_interval != 0 ? var.mariadb_config.enabled_cloudwatch_logs_exports : null
  monitoring_interval                   = var.mariadb_config.monitoring_interval
  monitoring_role_arn                   = var.mariadb_config.monitoring_interval != 0 ? var.rds_monitoring_role.arn : null
  performance_insights_enabled          = var.mariadb_config.performance_insights_enabled
  performance_insights_retention_period = var.mariadb_config.performance_insights_retention_period
  maintenance_window                    = var.mariadb_config.maintenance_window

  final_snapshot_identifier = replace("${local.name_prefix}-mariadb-final-snapshot", "_", "-")

  tags = merge(local.default_tags, var.mariadb_config.additional_tags)
}