output "rabbitmq_nlb_dns" {
  value = try(aws_lb.rabbitmq_nlb[0].dns_name, null)
}

output "rabbitmq_alb_dns" {
  value = try(aws_lb.rabbitmq_alb[0].dns_name, null)
}

output "rabbitmq_clb_dns" {
  value = try(aws_elb.rabbitmq_clb[0].dns_name, null)
}

output "admin_password" {
  value     = random_string.admin_password.result
  sensitive = true
}

output "rabbit_password" {
  value     = random_string.rabbit_password.result
  sensitive = true
}

output "rabbitmq_autoscaling_group_name" {
  value = aws_autoscaling_group.rabbitmq.name
}