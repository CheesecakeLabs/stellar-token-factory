locals {
  name_prefix  = var.name_prefix
  default_tags = merge(var.default_tags, { "ckl:alias" = "${var.alias_name}" })

  features = merge({
    http                 = var.service_config.features.http ? true : false
    force_https_redirect = var.service_config.features.force_https_redirect ? true : false
    service_discovery    = var.service_config.features.service_discovery
  }, var.service_config.features)

  # Objects to create SSM parameters
  obj_envs = {
    for k, v in var.service_config.protected_envs : "${var.alias_name}:${k}" => v
  }

  container_ports = concat([var.service_config.container_port], try(var.service_config.additional_ports, []))
}

# Gets the current task definition from AWS, reflecting anything that's been deployed
# outside of Terraform (ie. CI build with ecs-deploy).
data "aws_ecs_task_definition" "current_task_definition" {
  task_definition = aws_ecs_task_definition.main_td.family
}

# If var.service_config.get_imagetag_ecs is enabled, gets the container definition to fill  
# the data "template_file" "main_container" with the current image tag
data "aws_ecs_task_definition" "current_task_definition_container" {
  count           = lookup(var.service_config, "get_imagetag_ecs", false) ? 1 : 0
  task_definition = "${local.name_prefix}-${var.alias_name}"
}

data "aws_ecs_container_definition" "current_container_definition" {
  count           = lookup(var.service_config, "get_imagetag_ecs", false) ? 1 : 0
  task_definition = data.aws_ecs_task_definition.current_task_definition_container[0].id
  container_name  = "${local.name_prefix}-${var.alias_name}"
}

resource "aws_ecs_service" "service_with_lb" {
  count                              = local.features.http ? 1 : 0
  name                               = "${local.name_prefix}-${var.alias_name}"
  cluster                            = var.cluster.id
  task_definition                    = "${aws_ecs_task_definition.main_td.family}:${max(aws_ecs_task_definition.main_td.revision, data.aws_ecs_task_definition.current_task_definition.revision)}"
  launch_type                        = "EC2"
  desired_count                      = var.service_config.task_count
  deployment_minimum_healthy_percent = 50

  network_configuration {
    subnets         = var.subnet_ids
    security_groups = [var.security_group_id]
  }

  ordered_placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  ordered_placement_strategy {
    type  = "spread"
    field = "instanceId"
  }

  dynamic "service_registries" {
    for_each = local.features.service_discovery ? [1] : [] # Workaround to apply condition to blocks

    content {
      registry_arn = aws_service_discovery_service.sd[0].arn
    }

  }

  dynamic "load_balancer" {
    for_each = local.features.http ? [1] : [] # Workaround to apply condition to blocks

    content {
      target_group_arn = aws_lb_target_group.tg.0.arn
      container_name   = "${local.name_prefix}-${var.alias_name}"
      container_port   = var.service_config.container_port
    }
  }

  tags = local.default_tags

  depends_on = [
    var.lb_listeners,
    aws_lb_target_group.tg.0,
    aws_ecs_task_definition.main_td
  ]

  lifecycle {
    ignore_changes = [task_definition]
  }
}

resource "aws_ecs_service" "service_no_lb" {
  count                              = !local.features.http ? 1 : 0
  name                               = "${local.name_prefix}-${var.alias_name}"
  cluster                            = var.cluster.id
  task_definition                    = "${aws_ecs_task_definition.main_td.family}:${max(aws_ecs_task_definition.main_td.revision, data.aws_ecs_task_definition.current_task_definition.revision)}"
  launch_type                        = "EC2"
  desired_count                      = var.service_config.task_count
  deployment_minimum_healthy_percent = 50

  network_configuration {
    subnets         = var.subnet_ids
    security_groups = [var.security_group_id]
  }

  ordered_placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  ordered_placement_strategy {
    type  = "spread"
    field = "instanceId"
  }

  dynamic "service_registries" {
    for_each = local.features.service_discovery ? [1] : [] # Workaround to apply condition to blocks

    content {
      registry_arn = aws_service_discovery_service.sd[0].arn
    }

  }

  tags = local.default_tags

  depends_on = [
    aws_ecs_task_definition.main_td
  ]

  lifecycle {
    ignore_changes = [task_definition]
  }
}

data "template_file" "main_container" {
  template = file("${path.module}/container.json")

  vars = {
    env_vars = jsonencode([
      for name, value in var.service_config.env_vars : {
        name  = name
        value = value
      }
    ])
    protected_envs = jsonencode([
      for name, value in var.service_config.protected_envs : {
        name      = name
        valueFrom = aws_ssm_parameter.ssm_parameters["${var.alias_name}:${name}"].arn
      }
    ])
    container_ports = jsonencode([
      for name, value in local.container_ports : {
        hostPort      = value
        protocol      = "tcp"
        containerPort = value
      }
    ])
    aws_region           = var.region
    container_name       = "${local.name_prefix}-${var.alias_name}"
    container_image      = try(var.service_config.image_name, (lookup(var.service_config, "get_imagetag_ecs", false) ? data.aws_ecs_container_definition.current_container_definition[0].image : "${aws_ecr_repository.ecr_repo.repository_url}:latest"))
    memory_reservation   = jsonencode(var.memory_reservation)
    cloudwatch_log_group = aws_cloudwatch_log_group.logs.name
  }
}

resource "aws_ecs_task_definition" "main_td" {
  family                   = "${local.name_prefix}-${var.alias_name}"
  requires_compatibilities = ["EC2"]
  network_mode             = "awsvpc"
  container_definitions    = data.template_file.main_container.rendered
  execution_role_arn       = var.task_execution_role
  task_role_arn            = var.task_role.arn

  tags = local.default_tags
}
