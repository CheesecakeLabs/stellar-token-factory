## What does it do?

1. Uses [official](https://hub.docker.com/_/rabbitmq/) RabbitMQ docker image.
1. Creates `N` nodes in `M` subnets
1. Creates Autoscaling Group and Network Load Balancer to load balance nodes
1. Makes sure nodes can talk to each other and create cluster
1. Make sure new nodes always join the cluster
1. Configures `/` vhost queues in High Available (Mirrored) mode with automatic synchronization (`"ha-mode":"all", "ha-sync-mode":"3"`)


## How to use it ?
Copy the module folder to your project modules folder and paste the code below in to your Terraform main configuration:
```
module "rabbitmq" {
  source                              = "./modules/rabbitmq"
  name_prefix                         = var.name_prefix
  vpc_id                              = var.vpc_id
  ec2_key_name                        = var.ec2_key_name
  subnet_ids                          = var.subnet_ids
  nodes_additional_security_group_ids = var.nodes_additional_security_group_ids
  bastion_security_group_ids          = var.bastion_security_group_ids
  default_tags                        = var.default_tags
  subnets_cidr                        = var.subnets_cidr
  rabbitmq_config                     = var.rabbitmq_config
}
```

then run `terraform init`, `terraform plan` and `terraform apply`.

Are 3 nodes not enough? Update sizes to `5` and run `terraform apply` again,
it will update Autoscaling Group and add `2` nodes more. Dead simple.

A node becomes unresponsive? Autoscaling group and Network Load Balancer Health Checks will automatically replace it with a new one, without data loss.

Note: The VPC must have `enableDnsHostnames` = `true` and `enableDnsSupport` = `true` for the private DNS names to be resolvable for the nodes to connect to each other.   
