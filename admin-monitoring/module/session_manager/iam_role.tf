data "aws_caller_identity" "current" {}

resource "aws_iam_role" "lambda_sessionManager_role" {
  name = "lambda_sessionManager_role"

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

resource "aws_iam_policy_attachment" "lambda_sessionManager_role_attach_policy" {
  name       = "lambda_admin_test_role_attach_policy"
  roles      = [aws_iam_role.lambda_sessionManager_role.name]
  policy_arn = aws_iam_policy.lambda_sessionManager_policy.arn
}

resource "aws_iam_policy" "lambda_sessionManager_policy" {
  name = "lambda_admin_test_policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "sns:*"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:sns:${var.aws_region}:${var.caller_id}:${var.sns_topic.name}"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams"
            ],
            "Resource": [
                "${data.aws_cloudwatch_log_group.system_manager_cloudwatch.arn}",
                "arn:aws:logs:${var.aws_region}:${var.caller_id}:log-group:/aws/lambda/sessionManager_send_notification:*"
            ]
        }
    ]
}
EOF
}
