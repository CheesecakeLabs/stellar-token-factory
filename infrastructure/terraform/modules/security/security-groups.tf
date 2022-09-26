# Public access to Load Balancer
resource "aws_security_group" "public_security_group" {
  name        = "${local.name_prefix}-public"
  description = "Allow access HTTP and HTTPS access"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow everyone access HTTP port"
    from_port   = 80
    protocol    = "tcp"
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow everyone access HTTPS port"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound access"
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.default_tags
}

# Private Access to ECS tasks
resource "aws_security_group" "private_security_group" {
  name        = "${local.name_prefix}-private"
  description = "Allow access from Bastion, Kong and Public Security Groups"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.bastion_config.enabled && var.bastion_config.security_group.private ? [1] : []
    content {
      description     = "Allow Bastion Security Group access all ports"
      from_port       = 0
      to_port         = 0
      protocol        = "-1"
      security_groups = [aws_security_group.bastion_public_security_group[0].id]
    }
  }

  dynamic "ingress" {
    for_each = var.kong_config.enabled ? [1] : []
    content {
      description     = "Allow Kong Security Group access all ports"
      from_port       = 0
      to_port         = 0
      protocol        = "-1"
      security_groups = [aws_security_group.kong_private_security_group[0].id]
    }
  }

  dynamic "ingress" {
    for_each = var.kong_config.enabled ? [] : [1]
    content {
      description     = "Allow Public Security Group access from 3000 to 9000 port"
      from_port       = 3000
      to_port         = 9000
      protocol        = "tcp"
      security_groups = [aws_security_group.public_security_group.id]
    }
  }

  dynamic "ingress" {
    for_each = length(var.scheduled_lambda) > 0 ? [1] : []
    content {
      description     = "Allow Lambda Security Group access 8000 port"
      from_port       = 8000
      to_port         = 8000
      protocol        = "tcp"
      security_groups = [aws_security_group.lambda_private_security_group[0].id]
    }
  }

  egress {
    description = "Allow all outbound access"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.default_tags
}

# Create a Security Group that allows access by Public Security Group if Kong is enabled and there is a service that requires
resource "aws_security_group" "frontend_public_security_group" {
  count       = var.kong_config.enabled && length(local.obj_frontend_security_group) > 0 ? 1 : 0
  name        = "${local.name_prefix}-frontend"
  description = "Allow access from Public Security Group when Kong is enabled. Used ONLY to Frontend Service, when it needs to be exposed directly."
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = local.obj_frontend_security_group
    content {
      description     = "Allow Public Security Group access in specific ports"
      from_port       = ingress.value
      to_port         = ingress.value
      security_groups = [aws_security_group.public_security_group.id]
      protocol        = "tcp"
    }
  }

  egress {
    description = "Allow all outbound access"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.default_tags
}

# Database access to Bastion Security Group and Private Security Group
resource "aws_security_group" "database_security_group" {
  name        = "${local.name_prefix}-database"
  description = "Allow access from Bastion and Private Security Groups"
  vpc_id      = var.vpc_id


  dynamic "ingress" {
    for_each = var.bastion_config.enabled && var.bastion_config.security_group.database ? [1] : []
    content {
      description     = "Allow Bastion Security Group access all ports"
      from_port       = 0
      to_port         = 0
      security_groups = [aws_security_group.bastion_public_security_group[0].id]
      protocol        = "-1"
    }
  }

  ingress {
    description     = "Allow Private Security Group access all ports"
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.private_security_group.id]
  }

  egress {
    description = "Allow all outbound access"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.default_tags
}


# If Kong API Gateway is enabled, create specific Security Groups
resource "aws_security_group" "kong_private_security_group" {
  count       = var.kong_config.enabled ? 1 : 0
  name        = "${local.name_prefix}-private-kong"
  description = "Allow access from Bastion and Public Security Groups"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow Public Security Group access 8000 (default Kong Endpoint) port"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.public_security_group.id]
  }

  dynamic "ingress" {
    for_each = var.bastion_config.enabled && var.bastion_config.security_group.kong ? [1] : []
    content {
      description     = "Allow Bastion Security Group access 1337 (default Konga GUI) port"
      from_port       = 1337
      to_port         = 1337
      protocol        = "tcp"
      security_groups = [aws_security_group.bastion_public_security_group[0].id]
    }
  }

  ingress {
    description = "Allow Kong Security Group access 8001 (default Kong Admin API) port (to Konga administrate)"
    from_port   = 8001
    to_port     = 8001
    protocol    = "tcp"
    self        = true
  }

  egress {
    description = "Allow all outbound access"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.default_tags
}

# Kong Database Access to Kong Private Security Group
resource "aws_security_group" "kong_database_security_group" {
  count       = var.kong_config.enabled ? 1 : 0
  name        = "${local.name_prefix}-database-kong"
  description = "Private access allowed from Kong Private Security Group"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow Kong Security Group access 5432 port"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.kong_private_security_group[0].id]
  }

  egress {
    description = "Allow all outbound access"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.default_tags
}

# Kong Database Access to Kong Private Security Group
resource "aws_security_group" "cluster_private_security_group" {
  name        = "${local.name_prefix}-private-cluster"
  description = "Private access allowed from Bastion Security Group"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.bastion_config.enabled && var.bastion_config.security_group.cluster ? [1] : []
    content {
      description     = "Allow Bastion Security Group access 22 port"
      from_port       = 22
      to_port         = 22
      protocol        = "tcp"
      security_groups = [aws_security_group.bastion_public_security_group[0].id]
    }
  }

  egress {
    description = "Allow all outbound access"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.default_tags
}

# Lambda Function access in Private Security Group
resource "aws_security_group" "lambda_private_security_group" {
  count       = length(var.scheduled_lambda) > 0 ? 1 : 0
  name        = "${local.name_prefix}-private-scheduled-lambda"
  description = "Lambda Function access in Private Security Group"
  vpc_id      = var.vpc_id

  egress {
    description = "Allow all outbound access"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.default_tags
}

# If Bastion Host is enabled, create specific Security Group
resource "aws_security_group" "bastion_public_security_group" {
  count       = var.bastion_config.enabled ? 1 : 0
  name        = "${local.name_prefix}-public-bastion"
  description = "Public access from SSH"
  vpc_id      = var.vpc_id

  tags = local.default_tags
}

resource "aws_security_group_rule" "bastion_public_security_group_ingress" {
  for_each          = var.bastion_config.enabled ? var.bastion_config.allowed_cidrs : {}
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["${each.key}"]
  description       = each.value
  security_group_id = aws_security_group.bastion_public_security_group[0].id
}

resource "aws_security_group_rule" "bastion_public_security_group_egress" {
  count             = var.bastion_config.enabled ? 1 : 0
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  description       = "Allow all outbound access"
  security_group_id = aws_security_group.bastion_public_security_group[0].id
}