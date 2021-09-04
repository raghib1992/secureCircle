data "aws_caller_identity" "current" {}

resource "aws_cloudtrail" "AdminUserLoginDetails" {
  name                          = "AdminUserLoginDetails"
  s3_bucket_name                = aws_s3_bucket.trail_login_details.id
  # s3_key_prefix                 = "AWSTrail"
  include_global_service_events = false
}

resource "aws_s3_bucket" "trail_login_details" {
  bucket        = "trail-login-details"
  force_destroy = true
  versioning {
    enabled = true
  }
  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck",
            "Effect": "Allow",
            "Principal": {
              "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::trail-login-details"
        },
        {
            "Sid": "AWSCloudTrailWrite",
            "Effect": "Allow",
            "Principal": {
              "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::trail-login-details/AWSLogs/${data.aws_caller_identity.current.account_id}/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
}
POLICY
}