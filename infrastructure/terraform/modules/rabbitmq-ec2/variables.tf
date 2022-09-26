variable "vpc_id" {
  description = "ID from VPC to deploy instances"
  type        = string
}

variable "ec2_key_name" {
  description = "EC2 SSH key name to use in instances"
  type        = string
}


variable "subnet_ids" {
  description = "Subnets for RabbitMQ nodes"
  type        = list(string)
}

variable "nodes_additional_security_group_ids" {
  description = "Additional Security Groups to attach in RabbitMQ instances"
  type        = list(string)
  default     = []
}

variable "bastion_security_group_ids" {
  description = "Bastion Security Group to allow access in RabbitMQ"
  type        = list(string)
  default     = []
}

variable "name_prefix" {
  description = "Name prefix to use in resourcers creation"
  type        = string
}

variable "default_tags" {
  description = "Default tags to apply in resources"
  type        = any
}

variable "subnets_cidr" {
  description = "Subnets to give access in RabbitMQ"
  type        = list(string)
  default     = []
}

variable "security_group_ids" {
  description = "Security Groups to give access in RabbitMQ HTTP console"
  type        = list(string)
  default     = []
}

variable "create_network_load_balancer" {
  description = "Create Network Load Balancer for AMQP"
  type        = bool
  default     = true
}

variable "create_application_load_balancer" {
  description = "Create Application Load Balancer for HTTP console/API"
  type        = bool
  default     = false
}

variable "create_classic_load_balancer" {
  description = "Create Classic Load Balancer for AMQP and HTTP console/API"
  type        = bool
  default     = false
}

variable "ec2_config" {
  description = "RabbitMQ configurations"
  /*
  instance_volume_type = Type of instance volume
  instance_volume_size = Volume size of the instance
  instance_volume_iops = Volume provisioned IOPS. 0 equals to not provision.
  rabbitmq_image = image to use when deploy RabbitMQ container
  min_size = Minimum instances to deploy
  max_size = Maximum instances to deploy
  desired_size = Desired instance quantity to deploy 
  plugins = {
    rabbitmq_management = enable or disable rabbitmq_management plugin
    rabbitmq_delayed_message_exchange = enable or disable rabbitmq_delayed_message_exchange plugin
  }
  instances_type_weight = Object containing the instances types (key) and the weight (value) to consider in the Auto Scaling Group
  instances_distribution = {
    on_demand_base_capacity = Absolute minimum amount of desired capacity that must be fulfilled by on-demand instances
    on_demand_percentage_above_base_capacity = Percentage split between on-demand and Spot instances above the base on-demand capacity
    spot_allocation_strategy = How to allocate capacity across the Spot pools
  }
  */
  type = object({
    instance_volume_device_name = string
    instance_volume_type        = string
    instance_volume_size        = number
    instance_volume_iops        = number
    rabbitmq_image              = string
    min_size                    = number
    max_size                    = number
    desired_size                = number
    plugins = object({
      rabbitmq_management               = bool
      rabbitmq_delayed_message_exchange = bool
    })
    instances_type_weight = any
    instances_distribution = object({
      on_demand_base_capacity                  = number
      on_demand_percentage_above_base_capacity = number
      spot_allocation_strategy                 = string
    })
  })

  default = {
    instance_volume_device_name = "/dev/xvda"
    instance_volume_type        = "standard"
    instance_volume_size        = 8
    instance_volume_iops        = 0
    rabbitmq_image              = "rabbitmq:3-management"
    min_size                    = 3
    max_size                    = 3
    desired_size                = 3
    plugins = {
      rabbitmq_management               = true
      rabbitmq_delayed_message_exchange = false
    }
    instances_type_weight = {
      "t3.micro" = 1
    }
    instances_distribution = {
      on_demand_base_capacity                  = 0
      on_demand_percentage_above_base_capacity = 100
      spot_allocation_strategy                 = "capacity-optimized"
    }
  }
}