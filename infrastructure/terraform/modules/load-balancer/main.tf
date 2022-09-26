locals {
  name_prefix  = var.name_prefix
  default_tags = merge(var.default_tags, { "ckl:alias" = "load-balancer" })
}

resource "aws_lb" "lb" {
  name               = local.name_prefix
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.security_group_id]
  subnets            = var.subnet_ids

  tags = merge(local.default_tags, {
    Name = local.name_prefix
  })
}

resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
  #  default_action {
  #    type = "fixed-response"
  #
  #    fixed_response {
  #      content_type = "text/plain"
  #      message_body = "Pong"
  #      status_code  = "200"
  #    }
  #  }
}

resource "aws_lb_listener" "https_listener" {
  load_balancer_arn = aws_lb.lb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "Pong"
      status_code  = "200"
    }
  }
}
