provider "aws" {
  region = "ap-south-1"
}

locals {
  common_tags = {
    Name = "raghib-test"
    env = "test"
  }
}

data "aws_caller_identity" "current" {}