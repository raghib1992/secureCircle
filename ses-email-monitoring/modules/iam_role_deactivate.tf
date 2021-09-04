resource "aws_iam_role" "lambda_ses_email_deactivation_role" {
  name = "lambda_ses_email_deactivation_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "ses_email_deactivate_attach_policy" {
  name       = "lambda_ses_email_deactivation_role"
  roles      = [aws_iam_role.lambda_ses_email_deactivation_role.name]
  policy_arn = aws_iam_policy.ses_email_deactivate_policy.arn
}

resource "aws_iam_policy" "ses_email_deactivate_policy" {
  name = "ses_email_deactivate_policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGetItem",
                "dynamodb:BatchWriteItem",
                "dynamodb:ConditionCheckItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:Query"
            ],
            "Resource": "arn:aws:dynamodb:${var.aws_region}:${var.caller_id}:table/ses-email-dynoTable"
        },
        {
            "Effect": "Allow",
            "Action": [
                "athena:StartQueryExecution",
                "athena:GetWorkGroup",
                "athena:GetQueryResults"
            ],
            "Resource": "arn:aws:athena:${var.aws_region}:${var.caller_id}:workgroup/primary"
        },
        {
            "Effect": "Allow",
            "Action": [
                "glue:UpdateTable",
                "glue:GetTable"
            ],
            "Resource": [
                "arn:aws:glue:${var.aws_region}:${var.caller_id}:catalog",
                "arn:aws:glue:${var.aws_region}:${var.caller_id}:database/saas_ses_email",
                "arn:aws:glue:${var.aws_region}:${var.caller_id}:table/saas_ses_email/sesblog2"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketLocation",
                "s3:GetObject*",
                "s3:ListBucketMultipartUploads",
                "s3:ListMultipartUploadParts",
                "s3:AbortMultipartUpload",
                "s3:PutObject*"
            ],
            "Resource": [
                "arn:aws:s3:::saas-ses-email-query-result",
                "arn:aws:s3:::saas-ses-email-query-result/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject*",
                "s3:ListBucket",
                "s3:PutObject*"
            ],
            "Resource": [
                "arn:aws:s3:::saas-ses-email-monitor",
                "arn:aws:s3:::saas-ses-email-monitor/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:*AccessKey*"
            ],
            "Resource": "arn:aws:iam::${var.caller_id}:user/*"
        },
        {
            "Action": [
                "logs:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
EOF
}