output "ecr_arn" {
  value = aws_ecr_repository.ecr_repo.arn
}
output "ecr_url" {
  value = aws_ecr_repository.ecr_repo.repository_url
}
output "task_definitions" {
  value = {
    main = aws_ecs_task_definition.main_td
  }
}

output "ssm_parameters" {
  value = aws_ssm_parameter.ssm_parameters
}

output "cloudwatch_logs" {
  value = aws_cloudwatch_log_group.logs
}