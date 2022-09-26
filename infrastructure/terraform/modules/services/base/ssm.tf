resource "aws_ssm_parameter" "ssm_parameters" {

  for_each = local.obj_envs

  name  = format("/%s/%s/%s", local.name_prefix, var.alias_name, replace(each.key, "${var.alias_name}:", ""))
  type  = "SecureString"
  value = each.value

  key_id = var.kms_alias_arn

  tags = merge({ "Name" = format("%s", local.name_prefix) }, local.default_tags)
}