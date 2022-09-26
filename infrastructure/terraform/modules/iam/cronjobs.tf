data "aws_iam_policy_document" "runtask_policy_document" {
  for_each = { for k, v in var.services_config : k => v if length(v.cronjobs) > 0 }

  statement {
    effect = "Allow"
    actions = [
      "ecs:RunTask"
    ]
    resources = [for td in var.task_definitions_arns[each.key] : "${replace(td, "/:\\d+$/", "")}"]
    condition {
      test     = "ArnLike"
      values   = [var.cluster_arn]
      variable = "ecs:cluster"
    }
  }
  statement {
    effect    = "Allow"
    actions   = ["iam:PassRole"]
    resources = ["*"]
    condition {
      test     = "StringLike"
      values   = ["ecs-tasks.amazonaws.com"]
      variable = "iam:PassedToService"
    }
  }
}

resource "aws_iam_policy" "runtask_policy" {
  for_each = { for k, v in var.services_config : k => v if length(v.cronjobs) > 0 }

  name   = "${local.name_prefix}-${each.key}-runtask-policy"
  policy = data.aws_iam_policy_document.runtask_policy_document[each.key].json
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_runtask_policy_attachment" {
  for_each = { for k, v in var.services_config : k => v if length(v.cronjobs) > 0 }

  role       = aws_iam_role.ecs_task_roles[each.key].name
  policy_arn = aws_iam_policy.runtask_policy[each.key].arn
}