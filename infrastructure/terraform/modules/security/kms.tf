resource "aws_kms_key" "this" {
  description = local.name_prefix

  tags = merge({ "Name" = local.name_prefix }, local.default_tags)
}

resource "aws_kms_alias" "this" {
  name          = format("alias/%s", local.name_prefix)
  target_key_id = aws_kms_key.this.key_id
}