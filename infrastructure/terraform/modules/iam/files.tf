# S3 App bucket PUBLIC 
data "aws_iam_policy_document" "app_bucket_public_policy_document" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.s3_public }

  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::${var.app_bucket.public}"
    ]
  }
  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "s3:DeleteObject",
      "s3:GetObject",
      "s3:PutObject",
      "s3:PutObjectAcl"
    ]
    resources = [
      "arn:aws:s3:::${var.app_bucket.public}/*"
    ]
  }
}

resource "aws_iam_policy" "app_bucket_public_policy" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.s3_public }

  name   = "${local.name_prefix}-s3-app-public-policy"
  policy = data.aws_iam_policy_document.app_bucket_public_policy_document[each.key].json
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_app_public_bucket_policy_attach" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.s3_public }

  role       = aws_iam_role.ecs_task_roles[each.key].name
  policy_arn = aws_iam_policy.app_bucket_public_policy[each.key].arn
}

# S3 App bucket PRIVATE 
data "aws_iam_policy_document" "app_bucket_private_policy_document" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.s3_private }

  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::${var.app_bucket.private}"
    ]
  }
  statement {
    sid    = ""
    effect = "Allow"
    actions = [
      "s3:DeleteObject",
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::${var.app_bucket.private}/*"
    ]
  }
}

resource "aws_iam_policy" "app_bucket_private_policy" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.s3_private }

  name   = "${local.name_prefix}-s3-app-private-policy"
  policy = data.aws_iam_policy_document.app_bucket_private_policy_document[each.key].json
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_app_private_bucket_policy_attach" {
  for_each = { for k, v in var.services_config : k => v if v.access_aws.s3_private }

  role       = aws_iam_role.ecs_task_roles[each.key].name
  policy_arn = aws_iam_policy.app_bucket_private_policy[each.key].arn
}