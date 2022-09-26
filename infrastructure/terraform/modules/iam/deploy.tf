resource "aws_iam_user" "deploy_user" {
  name = "${local.name_prefix}-deploy-user"
  tags = {
    "ckl:project" = var.project_name
    "ckl:alias"   = "app"
  }
}

resource "aws_iam_user_policy_attachment" "policy_attachment" {
  policy_arn = aws_iam_policy.deploy_policy.arn
  user       = aws_iam_user.deploy_user.name
}

resource "aws_iam_policy" "deploy_policy" {
  name   = "${local.name_prefix}-deploy-policy"
  policy = data.aws_iam_policy_document.ecs_deploy_policy.json
}

data "aws_iam_policy_document" "ecs_deploy_policy" {
  statement {
    effect = "Allow"
    actions = [
      "ecs:DeregisterTaskDefinition",
      "ecs:DescribeServices",
      "ecs:DescribeTaskDefinition",
      "ecs:DescribeTasks",
      "ecs:ListTasks",
      "ecs:ListTaskDefinitions",
      "ecs:RegisterTaskDefinition",
      "ecs:StartTask",
      "ecs:StopTask",
      "ecs:UpdateService",
      "ecr:GetAuthorizationToken"
    ]
    resources = ["*"]
  }
  statement {
    effect    = "Allow"
    actions   = ["ecr:*"]
    resources = [for arn in var.ecr_arns : arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["iam:PassRole"]
    resources = [for role in aws_iam_role.ecs_task_execution_roles : role.arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["iam:PassRole"]
    resources = [for role in aws_iam_role.ecs_task_roles : role.arn]
  }
}

resource "aws_iam_access_key" "deploy" {
  user = aws_iam_user.deploy_user.name
}
