resource "aws_autoscaling_group" "asg" {
  name_prefix         = local.name_prefix
  max_size            = var.cluster_config.max_instances
  min_size            = var.cluster_config.min_instances
  desired_capacity    = var.cluster_config.desired_instances
  vpc_zone_identifier = var.subnet_ids
  health_check_type   = "EC2"

  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = var.cluster_config.instances_distribution.on_demand_base_capacity
      on_demand_percentage_above_base_capacity = var.cluster_config.instances_distribution.on_demand_percentage_above_base_capacity
      spot_allocation_strategy                 = var.cluster_config.instances_distribution.spot_allocation_strategy
    }

    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.lt.id
        version            = "$Latest"
      }

      dynamic "override" {
        for_each = var.cluster_config.instances_type_weight
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
    value               = "${local.name_prefix}-ecs-instance"
  }

  tag {
    key                 = "ckl:alias"
    propagate_at_launch = true
    value               = "cluster"
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

data "aws_ami" "ecs_optimized" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"]
}

resource "aws_launch_template" "lt" {
  name                   = local.name_prefix
  update_default_version = true
  image_id               = data.aws_ami.ecs_optimized.id
  key_name               = var.ec2_key_name
  vpc_security_group_ids = [var.security_group_id]

  iam_instance_profile {
    name = var.ecs_instance_profile.id
  }

  monitoring {
    enabled = true
  }

  block_device_mappings {
    device_name = var.cluster_config.root_block.device_name

    ebs {
      volume_type           = var.cluster_config.root_block.volume_type
      volume_size           = var.cluster_config.root_block.volume_size
      iops                  = var.cluster_config.root_block.iops
      delete_on_termination = var.cluster_config.root_block.delete_on_termination
      encrypted             = var.cluster_config.root_block.encrypted
    }
  }

  tag_specifications {
    resource_type = "instance"
    tags          = local.default_tags
  }

  user_data = base64encode(<<EOF
      #!/bin/bash
      echo ECS_CLUSTER=${aws_ecs_cluster.cluster.name} >> /etc/ecs/ecs.config
      EOF
  )
}