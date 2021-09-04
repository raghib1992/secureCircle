resource "aws_iam_role" "lambda_ses_email_activation_role" {
  name = "lambda_ses_email_activation_role"

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

resource "aws_iam_policy_attachment" "ses_email_activate_attach_policy" {
  name       = "lambda_ses_email_activation_role"
  roles      = [aws_iam_role.lambda_ses_email_activation_role.name]
  policy_arn = aws_iam_policy.ses_email_activate_policy.arn
}

resource "aws_iam_policy" "ses_email_activate_policy" {
  name = "ses_email_activate_policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:DescribeStream",
                "dynamodb:GetRecords",
                "dynamodb:Scan",
                "dynamodb:Query",
                "dynamodb:GetShardIterator",
                "dynamodb:ListStreams",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:dynamodb:${var.aws_region}:${var.caller_id}:table/ses-email-dynoTable/stream/*"
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
        },
        {
            "Action": [
                "sns:Publish",
                "sns:ListTopics",
                "sns:GetTopicAttributes"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:sns:${var.aws_region}:${var.caller_id}:${var.sns_topic.name}"
        }
    ]
}
EOF
}