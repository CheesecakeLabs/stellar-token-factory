# Service role definition
resource "aws_iam_role" "ecs_service_role" {
  name               = "${local.name_prefix}-ecs-service-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_service_policy.json
  tags = merge(local.default_tags, {
    "ckl:alias" = "deploy"
  })
}

data "aws_iam_policy_document" "ecs_service_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com"]
    }
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecs_service_role_attachment" {
  role       = aws_iam_role.ecs_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole"
}

# Task role
resource "aws_iam_role" "ecs_task_roles" {
  for_each           = { for k, v in var.services_config : k => v }
  name               = format("%s-%s-task-role", local.name_prefix, each.key)
  assume_role_policy = data.aws_iam_policy_document.ecs_task_role_policy.json

  tags = local.default_tags
}

data "aws_iam_policy_document" "ecs_task_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com"]
    }
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

# Instance role definition
resource "aws_iam_role" "ecs_instance_role" {
  name               = "${local.name_prefix}-ecs-instance-role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.ecs_instance_policy.json
}

data "aws_iam_policy_document" "ecs_instance_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecs_instance_role_attachment" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

# Instance profile definition
resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "${local.name_prefix}-ecs-instance-profile"
  path = "/"
  role = aws_iam_role.ecs_instance_role.id
}

# Task Definition Roles
data "aws_iam_policy_document" "ecs_task_execution_roles" {
  for_each = { for k, v in var.services_config : k => v }
  statement {
    actions   = ["ssm:DescribeParameters"]
    resources = ["*"]
  }

  statement {
    actions   = ["ssm:GetParameters"]
    resources = ["arn:aws:ssm:*:*:parameter/${local.name_prefix}/${each.key}/*"]
  }

  statement {
    actions   = ["kms:Decrypt"]
    resources = [var.kms_alias]
  }
}

resource "aws_iam_role_policy" "ecs_task_execution_roles" {
  for_each = { for k, v in var.services_config : k => v }
  name     = format("%s-%s-%s", local.name_prefix, each.key, "task-exec-role")
  role     = aws_iam_role.ecs_task_execution_roles["${each.key}"].id

  policy = data.aws_iam_policy_document.ecs_task_execution_roles["${each.key}"].json
}

data "aws_iam_policy_document" "ecs_task_execution_roles_assume" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_execution_roles" {
  for_each           = { for k, v in var.services_config : k => v }
  name               = format("%s-%s-%s", local.name_prefix, each.key, "task-exec-role")
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_roles_assume.json

  tags = local.default_tags
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_roles" {
  for_each   = { for k, v in var.services_config : k => v }
  role       = aws_iam_role.ecs_task_execution_roles["${each.key}"].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# RDS Enhanced monitoring
resource "aws_iam_role" "rds_monitoring_role" {

  name = "${local.name_prefix}-rds-monitoring-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "monitoring.rds.amazonaws.com"
        }
      },
    ]
  })

  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"]

  tags = local.default_tags
}