output "dns" {
  value = aws_lb.lb.dns_name
}
output "listeners" {
  value = {
    http  = aws_lb_listener.http_listener
    https = aws_lb_listener.https_listener
  }
}
