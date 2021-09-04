data "aws_caller_identity" "current" {}

resource "aws_iam_role" "awslogs_ec2_role" {
  name = "awslogs_ec2_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "awslogs_ec2_attach_policy" {
  name       = "awslogs_ec2_attach_policy"
  roles      = [aws_iam_role.awslogs_ec2_role.name]
  policy_arn = aws_iam_policy.awslogs_ec2_policy.arn
}

resource "aws_iam_policy" "awslogs_ec2_policy" {
  name = "awslogs_ec2_policy"

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
        "*"
    ]
  }
 ]
}
EOF
}
