output "public_security_group_id" {
  value = aws_security_group.public_security_group.id
}
output "private_security_group_id" {
  value = aws_security_group.private_security_group.id
}
output "database_security_group_id" {
  value = aws_security_group.database_security_group.id
}
output "kong_private_security_group_id" {
  value = try(aws_security_group.kong_private_security_group[0].id, null)
}
output "kong_database_security_group_id" {
  value = try(aws_security_group.kong_database_security_group[0].id, null)
}
output "bastion_public_security_group_id" {
  value = try(aws_security_group.bastion_public_security_group[0].id, null)
}
output "frontend_public_security_group_id" {
  value = try(aws_security_group.frontend_public_security_group[0].id, null)
}
output "lambda_private_security_group_id" {
  value = try(aws_security_group.lambda_private_security_group[0].id, null)
}
output "cluster_private_security_group_id" {
  value = aws_security_group.cluster_private_security_group.id
}
output "kms_alias_arn" {
  value = aws_kms_alias.this.target_key_arn
}