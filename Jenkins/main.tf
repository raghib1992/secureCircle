provider "aws" {
    region = "ap-south-1"
}

resource "aws_s3_bucket" "raghib-test-bucket" {
  bucket = "raghib-test-bucket"
  acl    = "private"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

terraform {
  backend "s3" {
    bucket = "raghib-sc-terraform-backend"
    key    = "dev/terraform.tfstate"
    region = "ap-south-1"
  }
}