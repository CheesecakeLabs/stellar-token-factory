# Locals #
locals {
  name_prefix  = var.name_prefix
  alias_name   = "rmq"
  default_tags = merge(var.default_tags, { "ckl:alias" = "${local.alias_name}" })
}

# Datasource #
data "aws_vpc" "vpc" {
  id = var.vpc_id
}

data "aws_region" "current" {
}

data "aws_ami" "amazon-linux-2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

data "aws_iam_policy_document" "policy_doc" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "template_file" "cloud-init" {
  template = file("${path.module}/cloud-init.yaml")

  vars = {
    sync_node_count = 3
    asg_name        = "${local.name_prefix}-${local.alias_name}"
    region          = data.aws_region.current.name
    admin_password  = random_string.admin_password.result
    rabbit_password = random_string.rabbit_password.result
    secret_cookie   = random_string.secret_cookie.result
    rabbitmq_image  = var.ec2_config.rabbitmq_image
    aws_s3_bucket   = "${local.name_prefix}-${local.alias_name}"
    arr_plugins     = join(",", flatten([for plugin, enabled in var.ec2_config.plugins : enabled ? ["${plugin}"] : []]))
  }
}

# Secret and Passord #
resource "random_string" "admin_password" {
  length  = 32
  special = false
}

resource "random_string" "rabbit_password" {
  length  = 32
  special = false
}

resource "random_string" "secret_cookie" {
  length  = 64
  special = false
}

# IAM #
resource "aws_iam_role" "role" {
  name               = "${local.name_prefix}-${local.alias_name}-instance"
  assume_role_policy = data.aws_iam_policy_document.policy_doc.json
  tags               = local.default_tags
}

resource "aws_iam_role_policy" "policy" {
  name = "${local.name_prefix}-${local.alias_name}"
  role = aws_iam_role.role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "autoscaling:DescribeAutoScalingInstances",
                "ec2:DescribeInstances"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::${local.name_prefix}-${local.alias_name}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::${local.name_prefix}-${local.alias_name}/*"
            ]
        }
    ]
}
EOF

}

resource "aws_iam_instance_profile" "profile" {
  name_prefix = "${local.name_prefix}-${local.alias_name}-instance"
  role        = aws_iam_role.role.name
  tags        = local.default_tags
}

# Security Group #
resource "aws_security_group" "rabbitmq_nodes" {
  name        = "${local.name_prefix}-${local.alias_name}-nodes"
  vpc_id      = var.vpc_id
  description = "Security Group for the Rabbitmq nodes"

  ingress {
    protocol    = -1
    from_port   = 0
    to_port     = 0
    self        = true
    description = "Allow connection inside Security Group"
  }

  dynamic "ingress" {
    for_each = var.create_network_load_balancer || var.create_classic_load_balancer ? [1] : [] // Conditional workaround
    content {
      from_port       = 5672
      to_port         = 5672
      protocol        = "tcp"
      cidr_blocks     = var.create_network_load_balancer ? [for cidr in var.subnets_cidr : cidr] : null
      security_groups = var.create_classic_load_balancer ? [aws_security_group.rabbitmq_lb[0].id] : null
      description     = "Allow connection from Private Subnet"
    }
  }

  dynamic "ingress" {
    for_each = var.create_application_load_balancer || var.create_classic_load_balancer ? [1] : [] // Conditional workaround
    content {
      protocol        = "tcp"
      from_port       = 15672
      to_port         = 15672
      security_groups = [aws_security_group.rabbitmq_lb[0].id]
      description     = "Allow connection from RabbitMQ Load Balancer"
    }
  }

  ingress {
    protocol        = -1
    from_port       = 0
    to_port         = 0
    security_groups = var.bastion_security_group_ids
    description     = "Allow connection from Bastion Host - Access through Instances IPs"
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    description = "Allow connection to outside"

    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }

  tags = merge(local.default_tags, { Name = "${local.name_prefix}-${local.alias_name}-nodes" })
}

resource "aws_security_group" "rabbitmq_lb" {
  count = var.create_application_load_balancer || var.create_classic_load_balancer ? 1 : 0

  name        = "${local.name_prefix}-${local.alias_name}-lb"
  vpc_id      = var.vpc_id
  description = "Security Group for the RabbitMQ Load Balancer"

  ingress {
    from_port       = 15672
    to_port         = 15672
    protocol        = "tcp"
    security_groups = [for id in var.security_group_ids : id]
    description     = "Allow connection from Security Group"
  }

  ingress {
    from_port       = 15672
    to_port         = 15672
    protocol        = "tcp"
    security_groups = var.bastion_security_group_ids
    description     = "Allow connection from Bastion Security Group"
  }

  dynamic "ingress" {
    for_each = var.create_classic_load_balancer ? [1] : [] // Conditional workaround
    content {
      from_port       = 5672
      to_port         = 5672
      protocol        = "tcp"
      security_groups = [for id in var.security_group_ids : id]
      description     = "Allow connection from Security Group"
    }
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    description = "Allow connection to outside"

    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }

  tags = merge(local.default_tags, { Name = "${local.name_prefix}-${local.alias_name}-alb" })
}

# EC2 #
resource "aws_launch_template" "rabbitmq" {
  name                   = "${local.name_prefix}-${local.alias_name}-cluster"
  update_default_version = true
  image_id               = data.aws_ami.amazon-linux-2.id
  key_name               = var.ec2_key_name
  vpc_security_group_ids = concat([aws_security_group.rabbitmq_nodes.id], var.nodes_additional_security_group_ids)
  user_data              = base64encode(data.template_file.cloud-init.rendered)

  iam_instance_profile {
    name = aws_iam_instance_profile.profile.id
  }

  block_device_mappings {
    device_name = var.ec2_config.instance_volume_device_name

    ebs {
      volume_type           = var.ec2_config.instance_volume_type
      volume_size           = var.ec2_config.instance_volume_size
      iops                  = var.ec2_config.instance_volume_iops
      delete_on_termination = true
      encrypted             = true
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "rabbitmq" {
  name_prefix               = "${local.name_prefix}-${local.alias_name}"
  min_size                  = var.ec2_config.min_size
  desired_capacity          = var.ec2_config.desired_size
  max_size                  = var.ec2_config.max_size
  health_check_grace_period = 600
  health_check_type         = "ELB"
  force_delete              = true
  target_group_arns         = var.create_application_load_balancer ? [aws_lb_target_group.rabbitmq_tg.arn, aws_lb_target_group.rabbitmq_tg_http[0].arn] : (var.create_network_load_balancer ? [aws_lb_target_group.rabbitmq_tg.arn] : null)
  load_balancers            = var.create_classic_load_balancer ? [aws_elb.rabbitmq_clb[0].name] : null
  vpc_zone_identifier       = var.subnet_ids

  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = var.ec2_config.instances_distribution.on_demand_base_capacity
      on_demand_percentage_above_base_capacity = var.ec2_config.instances_distribution.on_demand_percentage_above_base_capacity
      spot_allocation_strategy                 = var.ec2_config.instances_distribution.spot_allocation_strategy
    }

    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.rabbitmq.id
        version            = "$Latest"
      }

      dynamic "override" {
        for_each = var.ec2_config.instances_type_weight
        content {
          instance_type     = override.key
          weighted_capacity = override.value
        }
      }
    }
  }

  tag {
    key                 = "Name"
    propagate_at_launch = true
    value               = "${local.name_prefix}-${local.alias_name}-instance"
  }

  dynamic "tag" {
    for_each = local.default_tags

    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}

# Target Group #
resource "aws_lb_target_group" "rabbitmq_tg" {

  name                 = "${local.name_prefix}-${local.alias_name}"
  port                 = 5672
  protocol             = "TCP"
  vpc_id               = var.vpc_id
  target_type          = "instance"
  deregistration_delay = 30

  health_check {
    protocol            = "TCP"
    interval            = 30
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }

  tags = local.default_tags

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb_target_group" "rabbitmq_tg_http" {
  count = var.create_application_load_balancer ? 1 : 0

  name                 = "${local.name_prefix}-${local.alias_name}-http"
  port                 = 15672
  protocol             = "HTTP"
  vpc_id               = var.vpc_id
  target_type          = "instance"
  deregistration_delay = 30

  health_check {
    protocol            = "HTTP"
    interval            = 30
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }

  tags = local.default_tags

  lifecycle {
    create_before_destroy = true
  }
}

# Load Balancer #
resource "aws_elb" "rabbitmq_clb" {
  count = var.create_classic_load_balancer ? 1 : 0

  name = "${local.name_prefix}-${local.alias_name}-clb"

  listener {
    instance_port     = 5672
    instance_protocol = "tcp"
    lb_port           = 5672
    lb_protocol       = "tcp"
  }

  listener {
    instance_port     = 15672
    instance_protocol = "http"
    lb_port           = 15672
    lb_protocol       = "http"
  }

  health_check {
    interval            = 30
    unhealthy_threshold = 10
    healthy_threshold   = 2
    timeout             = 3
    target              = "TCP:5672"
  }

  subnets         = var.subnet_ids
  idle_timeout    = 3600
  internal        = true
  security_groups = ["${aws_security_group.rabbitmq_lb[0].id}"]

  tags = merge(local.default_tags, { Name = "${local.name_prefix}" })
}

resource "aws_lb" "rabbitmq_nlb" {
  count = var.create_network_load_balancer ? 1 : 0

  name               = "${local.name_prefix}-${local.alias_name}-nlb"
  internal           = true
  load_balancer_type = "network"
  subnets            = var.subnet_ids
  idle_timeout       = 3600

  tags = merge(local.default_tags, { Name = "${local.name_prefix}" })
}

resource "aws_lb" "rabbitmq_alb" {
  count = var.create_application_load_balancer ? 1 : 0

  name               = "${local.name_prefix}-${local.alias_name}-alb"
  internal           = true
  load_balancer_type = "application"
  subnets            = var.subnet_ids
  idle_timeout       = 3600
  security_groups    = [aws_security_group.rabbitmq_lb[0].id]

  tags = merge(local.default_tags, { Name = "${local.name_prefix}" })
}

# Load Balancer Listener #
resource "aws_lb_listener" "rabbitmq-console" {
  count = var.create_application_load_balancer ? 1 : 0

  load_balancer_arn = aws_lb.rabbitmq_alb[0].arn
  port              = "15672"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.rabbitmq_tg_http[0].arn
  }
}

resource "aws_lb_listener" "rabbitmq-socket" {
  count = var.create_network_load_balancer ? 1 : 0

  load_balancer_arn = aws_lb.rabbitmq_nlb[0].arn
  port              = "5672"
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.rabbitmq_tg.arn
  }
}

# S3 Bucket #
resource "aws_s3_bucket" "rabbitmq" {
  bucket = "${local.name_prefix}-${local.alias_name}"
  acl    = "private"
  tags   = local.default_tags
}

resource "aws_s3_bucket_object" "object" {
  for_each = fileset("${path.module}/plugins/", "*")

  bucket = aws_s3_bucket.rabbitmq.id
  key    = "plugins/${each.value}"
  acl    = "private"
  source = "${path.module}/plugins/${each.value}"
  etag   = filemd5("${path.module}/plugins/${each.value}")
}