resource "aws_iam_role" "test_role" {
  name = "test_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "test_attach_policy" {
  name       = "test_attach_policy"
  roles      = [aws_iam_role.test_role.name]
  policy_arn = aws_iam_policy.test_policy.arn
}

resource "aws_iam_policy" "test_policy" {
  name = "test_policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:*"
            ],
            "Resource": "*"
        },
        {
            "Action": [
                "sns:*"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:sns:${var.aws_region}:${var.caller}:${var.SNS_TOPIC.name}"
        }
    ]
}
EOF
}