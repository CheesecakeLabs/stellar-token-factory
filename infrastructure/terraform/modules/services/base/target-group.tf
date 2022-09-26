resource "aws_lb_target_group" "tg" {
  count = local.features.http ? 1 : 0

  name        = "${local.name_prefix}-${var.alias_name}"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path    = var.service_config.health_check_path
    matcher = try(var.service_config.health_check_matcher, "200")
  }

  tags = local.default_tags
}

resource "aws_lb_listener_rule" "host_based_routing_http" {
  count = local.features.http && !local.features.force_https_redirect ? 1 : 0

  listener_arn = var.lb_listeners.http.arn

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.0.arn
  }

  condition {
    host_header {
      values = var.service_config.domains
    }
  }
}

resource "aws_lb_listener_rule" "https_force_redirect" {
  count = local.features.http && local.features.force_https_redirect ? 1 : 0

  listener_arn = var.lb_listeners.http.arn

  action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }

  condition {
    host_header {
      values = var.service_config.domains
    }
  }
}

resource "aws_lb_listener_rule" "host_based_routing_https" {
  count = local.features.http ? 1 : 0

  listener_arn = var.lb_listeners.https.arn

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.0.arn
  }

  condition {
    host_header {
      values = var.service_config.domains
    }
  }
}
