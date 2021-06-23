terraform {
  backend "s3" {
    bucket = "deerpark-terraform-state"
    key = "stock-service/terraform.tfstate"
    region = "us-east-2"
  }
}

provider "aws" {}

data "aws_caller_identity" "current" {}

data "aws_region" "region" {}

data "terraform_remote_state" "remote_state" {
  backend = "s3"
  config = {
    bucket = "deerpark-terraform-state"
    key = "terraform-aws-ecs-free-tier/terraform.tfstate"
    region = "us-east-2"
  }
}
# data.terraform_remote_state.remote_state.outputs.ecs_cluster_id
# data.terraform_remote_state.remote_state.outputs.task_role
# data.terraform_remote_state.remote_state.outputs.task_execution_role
# data.terraform_remote_state.remote_state.outputs.rds_connection_url

resource "aws_cloudwatch_log_group" "cloudwatch_log_group" {
  name = var.cloudwatch_group
  retention_in_days = 7
}

data "template_file" "container_definition" {
  template = file("${path.module}/container-definition.json.tpl")
  vars = {
    image = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.region.name}.amazonaws.com/rent:${var.IMAGE_VERSION}"
    db_connection_url = data.terraform_remote_state.remote_state.outputs.rds_connection_url
    fugle_api_token = var.FUGLE_API_TOKEN
    awslogs_group = var.cloudwatch_group
    awslogs_region = data.aws_region.region.name
    awslogs_prefix = var.name_prefix
  }
}

resource "aws_ecs_task_definition" "ecs_task_definition" {
  family = "${var.name_prefix}-ecs-task-definition"
  task_role_arn = data.terraform_remote_state.remote_state.outputs.task_role
  execution_role_arn = data.terraform_remote_state.remote_state.outputs.task_execution_role
  container_definitions = data.template_file.container_definition.rendered
}

resource "aws_ecs_service" "ecs_service" {
  name = "${var.name_prefix}-ecs-service"
  cluster = data.terraform_remote_state.remote_state.outputs.ecs_cluster_id
  task_definition = aws_ecs_task_definition.ecs_task_definition.arn
  force_new_deployment = true
  desired_count = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent = 100
}
