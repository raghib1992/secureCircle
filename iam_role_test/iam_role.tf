data "aws_caller_identity" "current" {}

resource "aws_iam_role" "lambda_accountLogin_role" {
  name = "lambda_accountLogin_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "cloudwatch.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_admin_test_role_attach_policy" {
  name       = "lambda_admin_test_role_attach_policy"
  roles      = [aws_iam_role.lambda_accountLogin_role.name]
  policy_arn = aws_iam_policy.lambda_accountLogin_policy.arn
}

resource "aws_iam_policy" "lambda_accountLogin_policy" {
  name = "lambda_accountLogin_policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams"
            ],
            "Resource": [
                "${aws_cloudwatch_log_group.trail_consoleLog_data.arn}:*",
                "arn:aws:logs:${var.aws_region}:${var.caller_id}:log-group:/aws/lambda/accountLogin_send_notification:*"
            ]
        }
    ]
}
EOF
}