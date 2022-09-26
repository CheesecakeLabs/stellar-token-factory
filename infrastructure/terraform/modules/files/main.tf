locals {
  name_prefix  = var.name_prefix
  default_tags = merge(var.default_tags, { "ckl:alias" = "files" })
}

resource "aws_s3_bucket" "app_bucket_public" {
  bucket = "${local.name_prefix}-app-public"

  tags = local.default_tags
}

resource "aws_s3_bucket_policy" "app_bucket_public" {
  bucket = aws_s3_bucket.app_bucket_public.id
  policy = data.aws_iam_policy_document.app_bucket_public.json
}

data "aws_iam_policy_document" "app_bucket_public" {
  statement {
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    effect = "Allow"

    actions = [
      "s3:GetObject",
    ]

    resources = ["${aws_s3_bucket.app_bucket_public.arn}/*"]
  }
}

resource "aws_s3_bucket" "app_bucket_private" {
  bucket = "${local.name_prefix}-app-private"

  tags = local.default_tags
}

resource "aws_s3_bucket_acl" "app_bucket_private" {
  bucket = aws_s3_bucket.app_bucket_private.id

  acl = "private"
}

resource "aws_s3_bucket_public_access_block" "app_bucket_private" {
  bucket = aws_s3_bucket.app_bucket_private.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "app_bucket_private" {
  bucket = aws_s3_bucket.app_bucket_private.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}