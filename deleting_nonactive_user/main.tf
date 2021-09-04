provider "aws" {
  region = local.region
}

data "aws_caller_identity" "current" {}

provider "archive" {}

locals {
  common_tags = {
    sc_purpose = "sc-saas"
  }
  region = "ap-south-1"
}

resource "aws_sns_topic" "test_sns" {
  name = "test_sns"
}

module "deleting_inactive_user" {
  source = "./modules/"
  aws_region = local.region
  caller_id = data.aws_caller_identity.current.id
  sns_topic = aws_sns_topic.test_sns
}