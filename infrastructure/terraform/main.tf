// We can't use interpolation in terraform block :(
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.24.0"
    }
  }

  backend "s3" {
    # AWS Profile
    profile = "ckl-stellar-tf"
    # Bucket for "tfstate"
    bucket = "stellar-tf-terraform-state"
    # DynamoDB table for "tfstate"
    dynamodb_table = "stellar-tf-terraform-locks"
    key            = "terraform.tfstate"
    #Region to deploy "tfstate" resources
    region  = "us-east-2"
    encrypt = true
  }

}

provider "aws" {
  profile = var.aws_profile
  region  = var.region
}

# Module to generate a full VPC when is necessary
module "network" {
  # Network features provided by Registry
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.11.0"

  # A name prefix to use in all created resources
  name = local.name_prefix

  # CIDR to create VPC
  cidr = var.network_config.cidr_vpc

  # Avalilability Zones and subnets created dinamically
  azs              = [for az in var.network_config.availability_zones : format("%s%s", var.region, az)]
  public_subnets   = [for i, az in var.network_config.availability_zones : replace(var.network_config.cidr_public_subnet, "#SEQUENCE#", "${i}")]
  private_subnets  = [for i, az in var.network_config.availability_zones : replace(var.network_config.cidr_private_subnet, "#SEQUENCE#", "${i}" + 10)]
  database_subnets = [for i, az in var.network_config.availability_zones : replace(var.network_config.cidr_database_subnet, "#SEQUENCE#", "${i}" + 20)]

  # Create a database subnet group with a specific name
  create_database_subnet_group = true
  database_subnet_group_name   = local.name_prefix

  # NAT Gateway options
  enable_nat_gateway     = var.network_config.enable_nat_gateway
  single_nat_gateway     = var.network_config.single_nat_gateway
  one_nat_gateway_per_az = var.network_config.one_nat_gateway_per_az
  enable_vpn_gateway     = false

  # Enable DNS Hostnames
  enable_dns_hostnames = true

  # Default TAGs to apply in all created resources
  tags = local.default_tags

}

module "iam" {
  source       = "./modules/iam"
  region       = var.region
  project_name = var.project_name
  name_prefix  = local.name_prefix
  environment  = terraform.workspace
  ecr_arns = [
    module.backend_service.ecr_arn,
    module.frontend_service.ecr_arn,
    module.frontend_payment_service.ecr_arn,
  ]
  app_bucket = {
    public  = module.files.app_bucket_public
    private = module.files.app_bucket_private
  }
  cloudwatch_arns = {
    backend  = module.backend_service.cloudwatch_logs.arn
    frontend = module.frontend_service.cloudwatch_logs.arn
    frontend_payment = module.frontend_payment_service.cloudwatch_logs.arn
  }
  cluster_arn = module.cluster.cluster.arn
  task_definitions_arns = {
    backend  = values(module.backend_service.task_definitions).*.arn,
    frontend_payment = values(module.frontend_payment_service.task_definitions).*.arn,
  }
  services_config = var.services_config
  kms_alias       = module.security.kms_alias_arn
  bastion_arn     = try(module.ec2_bastion.arn, 0)
  default_tags    = local.default_tags
}

module "database" {
  source              = "./modules/database"
  region              = var.region
  project_name        = var.project_name
  name_prefix         = local.name_prefix
  environment         = terraform.workspace
  vpc_id              = module.network.vpc_id
  security_group      = module.security.database_security_group_id
  subnet_ids          = module.network.private_subnets
  availability_zone   = var.network_config.availability_zones[0]
  postgres_config     = var.postgres_config
  mariadb_config      = var.mariadb_config
  kong_config         = merge(var.kong_config, { security_group = module.security.kong_database_security_group_id }, { "KONG_DB_PASSWORD" = module.database.kong_password })
  rds_monitoring_role = module.iam.rds_monitoring_role
  default_tags        = local.default_tags
}

module "files" {
  source       = "./modules/files"
  project_name = var.project_name
  name_prefix  = local.name_prefix
  environment  = terraform.workspace
  default_tags = local.default_tags
}

module "security" {
  source           = "./modules/security"
  project_name     = var.project_name
  name_prefix      = local.name_prefix
  environment      = terraform.workspace
  vpc_id           = module.network.vpc_id
  services_config  = var.services_config
  scheduled_lambda = var.scheduled_lambda
  default_tags     = local.default_tags
  kong_config      = var.kong_config
  bastion_config   = var.bastion_config
}

module "acm" {
  source  = "terraform-aws-modules/acm/aws"
  version = "3.2.1"

  domain_name = var.domains["apex"]

  validate_certificate = false
  validation_method    = "DNS"

  subject_alternative_names = compact(flatten([for domains in var.domains.services : [for domain in domains : domain != var.domains["apex"] ? domain : null]]))

  wait_for_validation = true

  tags = merge({ "Name" = format("%s-${var.domains["apex"]}", local.name_prefix) }, local.default_tags)
}

module "load_balancer" {
  source            = "./modules/load-balancer"
  region            = var.region
  project_name      = var.project_name
  name_prefix       = local.name_prefix
  environment       = terraform.workspace
  vpc_id            = module.network.vpc_id
  subnet_ids        = module.network.public_subnets
  security_group_id = module.security.public_security_group_id
  certificate_arn   = module.acm.acm_certificate_arn
  default_tags      = local.default_tags
}

module "cluster" {
  source               = "./modules/cluster"
  name_prefix          = local.name_prefix
  region               = var.region
  environment          = terraform.workspace
  project_name         = var.project_name
  vpc_id               = module.network.vpc_id
  subnet_ids           = module.network.private_subnets
  security_group_id    = module.security.cluster_private_security_group_id
  ecs_instance_profile = module.iam.ecs_instance_profile
  ecs_instance_role    = module.iam.ecs_instance_profile
  cluster_config       = var.cluster_config
  default_tags         = merge(local.default_tags, var.cluster_config.additional_tags)
  ec2_key_name         = var.cluster_public_key_name
}

module "frontend_service" {
  source              = "./modules/services/base"
  region              = var.region
  environment         = terraform.workspace
  project_name        = var.project_name
  name_prefix         = local.name_prefix
  alias_name          = "frontend"
  vpc_id              = module.network.vpc_id
  subnet_ids          = module.network.private_subnets
  security_group_id   = module.security.private_security_group_id
  cluster             = module.cluster.cluster
  task_role           = module.iam.ecs_task_roles.frontend
  task_execution_role = module.iam.ecs_task_execution_roles["frontend"].arn
  lb_listeners        = module.load_balancer.listeners
  memory_reservation  = 256
  kms_alias_arn       = module.security.kms_alias_arn
  service_config = merge(var.services_config.frontend, {
    domains                         = var.domains.services.frontend
    service_discovery_dns_namespace = try(aws_service_discovery_private_dns_namespace.discovery[0].id, null)
    protected_envs                  = var.services_config.frontend.protected_envs
    env_vars                        = var.services_config.frontend.env_vars
  })
  default_tags = local.default_tags
}

module "frontend_payment_service" {
  source              = "./modules/services/base"
  region              = var.region
  environment         = terraform.workspace
  project_name        = var.project_name
  name_prefix         = local.name_prefix
  alias_name          = "frontend-payment"
  vpc_id              = module.network.vpc_id
  subnet_ids          = module.network.private_subnets
  security_group_id   = module.security.private_security_group_id
  cluster             = module.cluster.cluster
  task_role           = module.iam.ecs_task_roles.frontend_payment
  task_execution_role = module.iam.ecs_task_execution_roles["frontend_payment"].arn
  lb_listeners        = module.load_balancer.listeners
  memory_reservation  = 256
  kms_alias_arn       = module.security.kms_alias_arn
  service_config = merge(var.services_config.frontend_payment, {
    domains                         = var.domains.services.frontend_payment
    service_discovery_dns_namespace = try(aws_service_discovery_private_dns_namespace.discovery[0].id, null)
    protected_envs                  = var.services_config.frontend_payment.protected_envs
    env_vars                        = var.services_config.frontend_payment.env_vars
  })
  default_tags = local.default_tags
}

module "backend_service" {
  source              = "./modules/services/base"
  region              = var.region
  environment         = terraform.workspace
  project_name        = var.project_name
  name_prefix         = local.name_prefix
  alias_name          = "backend"
  vpc_id              = module.network.vpc_id
  subnet_ids          = module.network.private_subnets
  security_group_id   = module.security.private_security_group_id
  cluster             = module.cluster.cluster
  task_role           = module.iam.ecs_task_roles.backend
  task_execution_role = module.iam.ecs_task_execution_roles["backend"].arn
  lb_listeners        = module.load_balancer.listeners
  memory_reservation  = 256
  kms_alias_arn       = module.security.kms_alias_arn
  service_config = merge(var.services_config.backend, {
    domains                         = var.domains.services.backend
    service_discovery_dns_namespace = try(aws_service_discovery_private_dns_namespace.discovery[0].id, null)
    protected_envs                  = var.services_config.backend.protected_envs,
    env_vars                        = var.services_config.backend.env_vars
  })
  default_tags = local.default_tags
}

module "ec2_bastion" {
  source = "./modules/bastion"

  enabled = var.bastion_config.enabled

  instance_type               = var.bastion_config.instance_type
  name_prefix                 = local.name_prefix
  security_groups             = [module.security.bastion_public_security_group_id]
  subnets                     = module.network.public_subnets
  key_name                    = var.bastion_public_key_name
  user_data_template          = "amazon-linux.sh"
  vpc_id                      = module.network.vpc_id
  associate_public_ip_address = var.bastion_config.enable_public_ip
  tags                        = merge(local.default_tags, { "ckl:alias" = "bastion" }, var.bastion_config.additional_tags)
}

resource "aws_service_discovery_private_dns_namespace" "discovery" {
  count = local.create_service_discovery_dns_namespace ? 1 : 0

  vpc  = module.network.vpc_id
  name = "${local.name_prefix}.local"

  tags = local.default_tags
}

module "database_security" {
  source = "./modules/database-security"

  services_config = var.services_config

}

module "scheduler_ec2_rds" {
  source = "./modules/ec2-rds-scheduler"

  count                 = var.ec2_rds_schedules_definitions.enable == true ? 1 : 0
  name                  = local.name_prefix
  schedules_definitions = var.ec2_rds_schedules_definitions.schedules
  tags                  = merge(local.default_tags, { "ckl:alias" = "ec2-rds-scheduler" })
}