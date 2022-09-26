output "ecs_service_role" {
  value = aws_iam_role.ecs_service_role
}
output "ecs_task_roles" {
  value = aws_iam_role.ecs_task_roles
}
output "ecs_task_execution_roles" {
  value = aws_iam_role.ecs_task_execution_roles
}
output "ecs_instance_role" {
  value = aws_iam_role.ecs_instance_role
}
output "ecs_instance_profile" {
  value = aws_iam_instance_profile.ecs_instance_profile
}
output "rds_monitoring_role" {
  value = aws_iam_role.rds_monitoring_role
}


output "deploy_keys" {
  value = {
    access_key_id     = aws_iam_access_key.deploy.id
    access_key_secret = aws_iam_access_key.deploy.secret
  }
}
