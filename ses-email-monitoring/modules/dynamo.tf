resource "aws_dynamodb_table" "ses_email_dynoTable" {
  name             = "ses-email-dynoTable"
  billing_mode     = "PROVISIONED"
  read_capacity    = 50
  write_capacity   = 50
  hash_key         = "IAM_User"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
  
  attribute {
    name = "IAM_User"
    type = "S"
  }

  ttl {
    attribute_name = "TTL"
    enabled        = true
  }

  tags = {
    Name        = "ses-email-dynoTable"
    Environment = "Raghib-test"
  }
}