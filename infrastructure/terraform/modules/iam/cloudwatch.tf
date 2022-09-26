data "aws_iam_policy_document" "cloudwatch_policy_document" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.cloudwatch }

  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:DescribeLogStreams",
      "logs:PutRetentionPolicy",
    ]
    resources = ["${var.cloudwatch_arns[each.key]}"]
  }

  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "logs:GetLogEvents",
      "logs:PutLogEvents"
    ]
    resources = ["${var.cloudwatch_arns[each.key]}:log-stream:*"]
  }

  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup"
    ]
    resources = ["arn:aws:logs:*:*:log-group:*"]
  }
}

resource "aws_iam_policy" "cloudwatch_policy" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.cloudwatch }

  name   = "${local.name_prefix}-${each.key}-cloudwatch-policy"
  policy = data.aws_iam_policy_document.cloudwatch_policy_document[each.key].json
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_cloudwatch_policy_attachment" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.cloudwatch }

  role       = aws_iam_role.ecs_task_roles[each.key].name
  policy_arn = aws_iam_policy.cloudwatch_policy[each.key].arn
}
