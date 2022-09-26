variable "region" {
  description = "AWS region where components are created"
  default     = "us-west-2"
}

variable "aws_profile" {
  # PS: there is an issue with Terraform that requires the AWS_PROFILE env var set up
  # before executing the commands. ie: export AWS_PROFILE=<profile>
  description = "Profile on ./aws/credentials used to authenticate requests"
  default     = "staging"
}

variable "project_name" {
  default = "stellar-tf"
}

variable "network_config" {
  description = "Base configuration to setup the underlaying network topology"
  type = object({
    cidr_vpc               = string
    cidr_public_subnet     = string
    cidr_private_subnet    = string
    cidr_database_subnet   = string
    availability_zones     = list(string)
    enable_nat_gateway     = bool
    single_nat_gateway     = bool
    one_nat_gateway_per_az = bool
  })
  default = {
    cidr_vpc               = "10.0.0.0/16"
    cidr_public_subnet     = "10.0.#SEQUENCE#.0/24"
    cidr_private_subnet    = "10.0.#SEQUENCE#.0/24"
    cidr_database_subnet   = "10.0.#SEQUENCE#.0/24"
    availability_zones     = ["a", "c"]
    enable_nat_gateway     = true
    single_nat_gateway     = true
    one_nat_gateway_per_az = false
  }
}

variable "cluster_config" {
  description = "Base configuration for setting up an ECS cluster"
  type = object({
    desired_instances     = number
    max_instances         = number
    min_instances         = number
    instances_type_weight = any
    instances_distribution = object({
      on_demand_base_capacity                  = number
      on_demand_percentage_above_base_capacity = number
      spot_allocation_strategy                 = string
    })
    root_block = object({
      device_name           = string
      volume_type           = string
      volume_size           = number
      encrypted             = bool
      iops                  = number
      delete_on_termination = bool
    })
    additional_tags = any
  })
  default = {
    desired_instances = 1
    max_instances     = 1
    min_instances     = 1
    instances_type_weight = {
      "t3.micro" = 1
      "t2.micro" = 1
    }
    instances_distribution = {
      on_demand_base_capacity                  = 0
      on_demand_percentage_above_base_capacity = 100
      spot_allocation_strategy                 = "capacity-optimized"
    }
    root_block = {
      device_name           = "/dev/xvda"
      volume_type           = "gp2"
      volume_size           = 30
      encrypted             = true
      iops                  = null
      delete_on_termination = true
    }
    additional_tags = {}
  }
}

variable "postgres_config" {
  description = "Base configuration for setting up a RDS MariaDB database"
  type = object({
    enable                                = bool
    engine_version                        = string
    instance_type                         = string
    username                              = string
    backup_retention_period               = number
    storage_size                          = number
    storage_encrypted                     = bool
    multi_az                              = bool
    deletion_protection                   = bool
    enabled_cloudwatch_logs_exports       = list(string)
    monitoring_interval                   = number
    performance_insights_enabled          = bool
    performance_insights_retention_period = number
    maintenance_window                    = string
    backup_window                         = string
    additional_tags                       = any
  })
  default = {
    enable                                = false
    engine_version                        = "14.2"
    instance_type                         = "db.t3.micro"
    username                              = null
    backup_retention_period               = 30
    storage_size                          = 50
    storage_encrypted                     = true
    multi_az                              = false
    deletion_protection                   = true
    enabled_cloudwatch_logs_exports       = ["postgresql"]
    monitoring_interval                   = 60
    performance_insights_enabled          = true
    performance_insights_retention_period = 7
    maintenance_window                    = "sat:03:30-sat:04:00"
    backup_window                         = "05:00-06:00"
    additional_tags                       = {}
  }
}

variable "mariadb_config" {
  description = "Base configuration for setting up a RDS MariaDB database"
  type = object({
    enable                                = bool
    instance_type                         = string
    username                              = string
    backup_retention_period               = number
    storage_size                          = number
    storage_encrypted                     = bool
    multi_az                              = bool
    deletion_protection                   = bool
    enabled_cloudwatch_logs_exports       = list(string)
    monitoring_interval                   = number
    performance_insights_enabled          = bool
    performance_insights_retention_period = number
    maintenance_window                    = string
    backup_window                         = string
    additional_tags                       = any
  })
  default = {
    enable                                = false
    instance_type                         = "db.t3.micro"
    username                              = null
    backup_retention_period               = 30
    storage_size                          = 50
    storage_encrypted                     = true
    multi_az                              = false
    deletion_protection                   = true
    enabled_cloudwatch_logs_exports       = ["audit", "error", "general", "slowquery"]
    monitoring_interval                   = 60
    performance_insights_enabled          = true
    performance_insights_retention_period = 7
    maintenance_window                    = "sat:03:30-sat:04:00"
    backup_window                         = "05:00-06:00"
    additional_tags                       = {}
  }
}

variable "domains" {
  description = "Domains of each service that is used on ALB requests forwarding"
  type = object({
    apex     = string
    services = any
  })
  # Example:
  # {
  #   apex = "cheesecakelabs.com" -> root (used to create the SSL certificate wilcard)
  #   services = {
  #      backend = "api.cheesecakelabs.com" -> subdomain that points to the backend API
  #      frontend = "cheesecakelabs.com" -> domain that points to the frontend client
  #      kong = "api.cheesecakelabs.com" -> domain that points to the frontend client
  # }
  # }
}

variable "services_config" {
  description = "Cluster services config (including env vars)"
  type = object({
    backend = object({
      get_imagetag_ecs  = bool
      task_count        = number
      container_port    = number
      log_retention     = number
      health_check_path = string
      use_database      = list(string)
      features = object({
        http                 = bool
        force_https_redirect = bool
        service_discovery    = bool
      })
      # Allow the service access AWS Resources
      access_aws = object({
        s3_private = bool
        s3_public  = bool
        ses        = bool
        cloudwatch = bool
      })
      # Cronjob definition format
      # <cron-name> = {
      #   cron = "0/10 * * * ? *"
      #   command = ["python", "src/manage.py", "check"]
      # }
      cronjobs = any
      # Env var definition format
      # {
      #   <VAR1_NAME> = "__INJECT__"
      #   <VAR2_NAME> = value
      # }
      #
      # __INJECT__ is a placeholder that will be overwriten
      env_vars = any
      # Protected secrets to inject in container as environment variables.
      # Secrets protected in SSM using KMS
      # Format:
      # {
      #   ENVIRONMENT_NAME = "ENVIRONMENT_VALUE" 
      # }
      protected_envs = any
    })
    frontend = object({
      get_imagetag_ecs  = bool
      task_count        = number
      container_port    = number
      log_retention     = number
      health_check_path = string
      features = object({
        http                 = bool
        force_https_redirect = bool
        service_discovery    = bool
      })
      access_aws = object({
        s3_private = bool
        s3_public  = bool
        ses        = bool
        cloudwatch = bool
      })
      cronjobs       = any
      env_vars       = any
      protected_envs = any
    })
  })
}

variable "bastion_public_key_name" {
  description = "Public Key name created in AWS to access EC2 Instances"
  type        = string
}

variable "cluster_public_key_name" {
  description = "Public Key name created in AWS to access EC2 Instances"
  type        = string
}

variable "kong_config" {
  description = "Kong configuration"
  type = object({
    enabled = bool
    rds = object({
      enabled                               = bool
      db_username                           = string
      db_engine_version                     = string
      db_instance_class                     = string
      db_storage_size                       = string
      db_backup_retention_period            = string
      db_subnets_name                       = string
      db_multi_az                           = bool
      storage_encrypted                     = bool
      db_final_snapshot_identifier          = string
      db_family                             = string
      db_storage_type                       = string
      db_instance_count                     = string
      monitoring_interval                   = number
      enabled_cloudwatch_logs_exports       = list(string)
      description                           = string
      maintenance_window                    = string
      performance_insights_enabled          = bool
      performance_insights_retention_period = number
      backup_window                         = string
    })
  })
  default = {
    enabled = false
    rds = {
      enabled                               = false
      db_username                           = "root"
      db_engine_version                     = "11.4"
      db_instance_class                     = "db.t3.micro"
      db_storage_size                       = 10
      db_backup_retention_period            = 30
      db_subnets_name                       = "db-subnets"
      db_multi_az                           = false
      storage_encrypted                     = true
      db_final_snapshot_identifier          = ""
      db_family                             = "postgres11"
      db_storage_type                       = "gp2"
      db_instance_count                     = 1
      monitoring_interval                   = 60
      enabled_cloudwatch_logs_exports       = ["postgresql"]
      description                           = "Kong API Gateway"
      maintenance_window                    = "sat:03:30-sat:04:00"
      performance_insights_enabled          = true
      performance_insights_retention_period = 7
      backup_window                         = "05:00-06:00"
    }
  }
}

variable "default_tags" {
  description = "Default tags to apply in resources"
  type        = object({})
  default     = {}
}

variable "additional_tags" {
  description = "Addtional tags to apply in resources"
  type        = object({})
  default     = {}
}

variable "bastion_config" {
  description = "Bastion configuration"
  type = object({
    enabled = bool
    # allowed_cidrs   = {"#CIDR" = "Description"}
    allowed_cidrs    = any
    instance_type    = string
    enable_public_ip = bool
    security_group = object({
      private  = bool
      database = bool
      kong     = bool
      cluster  = bool
    })
    additional_tags = any
  })
  default = {
    enabled          = true
    allowed_cidrs    = {}
    instance_type    = "t2.micro"
    enable_public_ip = true
    security_group = {
      private  = false
      database = false
      kong     = true
      cluster  = true
    }
    additional_tags = {}
  }
}

variable "ec2_rds_schedules_definitions" {
  description = "Schedule definition to EC2 and RDS instances to turn on and turn off"
  type = object({
    enable    = bool
    schedules = any
  })
  default = {
    enable    = false
    schedules = []
  }
}

variable "stellar_pckl_website" {
  description = "Module stellar_pckl_website definitions"
  type = object({
    website_cors_allow_all_origins = bool
    cloudfront_response_header_policy = object({
      force_origin_header              = bool
      access_control_allow_credentials = bool
      origin_override                  = bool
      access_control_allow_headers     = list(string)
      access_control_allow_methods     = list(string)
    })
  })
  default = {
    website_cors_allow_all_origins = false
    cloudfront_response_header_policy = {
      force_origin_header              = true
      access_control_allow_credentials = false
      origin_override                  = true
      access_control_allow_headers     = ["Authorization", "Content-Length"]
      access_control_allow_methods     = ["GET"]
    }
  }
}

variable "rabbitmq_config" {
  description = "RabbitMQ configurations"
  /*
  enabled              = Enable or disable the module
  create_network_load_balancer = Create Network Load Balancer
  create_application_load_balancer = Create Application Load Balancer
  create_classic_load_balancer = Create Classic Load Balancer
  ec2_config = {
    instance_volume_device_name = Root device name
    instance_volume_type = Type of instance volume
    instance_volume_size = Volume size of the instance
    instance_volume_iops = Volume provisioned IOPS. 0 equals to not provision.
    rabbitmq_image = image to use when deploy RabbitMQ container
    min_size = Minimum instances to deploy
    max_size = Maximum instances to deploy
    desired_size = Desired instance quantity to deploy
    create_network_load_balancer = Create Network Load Balancer
    create_application_load_balancer = Create Application Load Balancer
    create_classic_load_balancer = Create Classic Load Balancer
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
  }
  additional_tags = additional tags to apply to resources
  */
  type = object({
    enabled                          = bool
    create_network_load_balancer     = bool
    create_application_load_balancer = bool
    create_classic_load_balancer     = bool
    ec2_config = object({
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
    additional_tags = any
  })

  default = {
    enabled                          = false
    create_network_load_balancer     = true
    create_application_load_balancer = true
    create_classic_load_balancer     = false
    ec2_config = {
      instance_volume_device_name = "/dev/xvda"
      instance_type               = "t3.micro"
      instance_volume_type        = "standard"
      instance_volume_size        = 8
      instance_volume_iops        = 0
      rabbitmq_image              = "rabbitmq:3.9.0-management"
      min_size                    = 3
      max_size                    = 3
      desired_size                = 3
      plugins = {
        rabbitmq_management               = true
        rabbitmq_delayed_message_exchange = false
      }
      instances_type_weight = {
        "t3.micro" = 1
        "t2.micro" = 1
      }
      instances_distribution = {
        on_demand_base_capacity                  = 0
        on_demand_percentage_above_base_capacity = 100
        spot_allocation_strategy                 = "capacity-optimized"
      }
    }
    additional_tags = {}
  }
}

variable "scheduled_lambda" {
  description = "Schedule Lambda functions"
  type        = any
  default     = {}
  /*
  Example:
  scheduled_lambda = {
    testing = {
      description = "Testing Lambda"
      handler     = "example.handler"
      runtime     = "python3.8"
      source_path = "../scheduled-lambda/example"
      environment_variables = {
        "TEST"  = "testing"
      }
      cloudwatch_schedule_expression = "cron(0 * ? * 2-6 *)"
      access_private_network = true
    }
  }
  */
}

variable "stellar_coin_website" {
  description = "Module stellar_coin_website definitions"
  type = object({
    website_cors_allow_all_origins = bool
    cloudfront_response_header_policy = object({
      force_origin_header              = bool
      access_control_allow_credentials = bool
      origin_override                  = bool
      access_control_allow_headers     = list(string)
      access_control_allow_methods     = list(string)
    })
  })
  default = {
    website_cors_allow_all_origins = false
    cloudfront_response_header_policy = {
      force_origin_header              = true
      access_control_allow_credentials = false
      origin_override                  = true
      access_control_allow_headers     = ["Authorization", "Content-Length"]
      access_control_allow_methods     = ["GET"]
    }
  }
}