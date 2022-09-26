resource "aws_cloudwatch_event_rule" "cronjobs" {
  for_each = var.service_config.cronjobs

  name                = "${local.name_prefix}-cronjobs-${each.key}"
  schedule_expression = "cron(${each.value.cron})"
}

resource "aws_cloudwatch_event_target" "cronjobs" {
  for_each = var.service_config.cronjobs

  target_id = "${local.name_prefix}-cronjobs-${each.key}"
  rule      = aws_cloudwatch_event_rule.cronjobs[each.key].name
  arn       = var.cluster.arn
  role_arn  = var.task_role.arn

  input = <<DOC
{
  "containerOverrides": [
    {
      "name": "${local.name_prefix}-${var.alias_name}",
      "command": ${jsonencode(each.value.command)}
    }
  ]
}
DOC

  ecs_target {
    task_count          = 1
    task_definition_arn = replace(aws_ecs_task_definition.main_td.arn, "/:[0-9]*$/", "")
    launch_type         = "EC2"

    network_configuration {
      assign_public_ip = false
      security_groups  = [var.security_group_id]
      subnets          = var.subnet_ids
    }
  }

  lifecycle {
    ignore_changes = [
      role_arn
    ]
  }
}
