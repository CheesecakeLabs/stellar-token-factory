data "aws_iam_policy_document" "email_policy_document" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.ses }

  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "ses:SendEmail",
      "ses:SendRawEmail",
      "ses:GetSendQuota"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "email_policy" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.ses }

  name   = "${local.name_prefix}-ses-policy"
  policy = data.aws_iam_policy_document.email_policy_document[each.key].json
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_email_policy_attachment" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.ses }

  role       = aws_iam_role.ecs_task_roles[each.key].name
  policy_arn = aws_iam_policy.email_policy[each.key].arn
}
