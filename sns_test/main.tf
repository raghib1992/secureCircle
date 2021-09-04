provider "aws" {
  region = local.region
}

data "aws_caller_identity" "current" {}

locals {
  common_tags = {
    Name = "raghib-test"
  }
  region = "ap-south-1"
}

resource "aws_sns_topic" "regional_saas_alerts" {
  display_name = "${local.region} - SecureCircle regional SaaS alerts"
  name = "${local.region}-saas-alerts-sns-topic"
  tags = local.common_tags
}

module "sns_test" {
    source = "./modules/"
    sns_topic = aws_sns_topic.regional_saas_alerts
    calller_id = data.aws_caller_identity.current.id
    aws_region = local.region
}