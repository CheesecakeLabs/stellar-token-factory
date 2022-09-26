locals {
  name_prefix  = var.name_prefix
  default_tags = merge(var.default_tags, { "ckl:alias" = "scheduled-lambda" })
}


################################################
#
#            LAMBDA FUNCTIONS
#
################################################

module "lambda_functions" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "3.1.0"

  function_name = "${local.name_prefix}-${var.function_name}"
  description   = var.description
  handler       = var.handler
  runtime       = var.runtime

  publish = true

  environment_variables = var.environment_variables

  allowed_triggers = {
    "${var.function_name}" = {
      principal  = "events.amazonaws.com"
      source_arn = aws_cloudwatch_event_rule.this.arn
    }
  }

  vpc_subnet_ids         = var.access_private_network ? var.vpc_subnet_ids : null
  vpc_security_group_ids = var.access_private_network ? var.vpc_security_group_ids : null
  attach_network_policy  = var.access_private_network ? true : false

  source_path = var.source_path

  tags = local.default_tags
}

################################################
#
#            CLOUDWATCH EVENT
#
################################################

resource "aws_cloudwatch_event_rule" "this" {
  name                = "${local.name_prefix}-scheduled-lambda-${var.function_name}"
  description         = "Trigger Lambda scheduler"
  schedule_expression = var.cloudwatch_schedule_expression
  tags                = var.default_tags
}

resource "aws_cloudwatch_event_target" "this" {
  arn  = module.lambda_functions.lambda_function_arn
  rule = "${local.name_prefix}-scheduled-lambda-${var.function_name}"
}