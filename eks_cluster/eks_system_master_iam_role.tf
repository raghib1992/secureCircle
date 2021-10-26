data "aws_caller_identity" "current" {}

resource "aws_iam_role" "jenkins-eks-fg-saas-01-system_masters_role" {
  name = "jenkins-eks-fg-saas-01-system_masters"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:sts::288677030145:assumed-role/admins-from-gsuite/raghib.nadim@securecircle.com",
          "arn:aws:sts::288677030145:assumed-role/admins-from-gsuite/erik.webb@securecircle.com"
        ]
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringLike": {
          "sts:RoleSessionName": "root"
        }
      }
    }
  ]
}
EOF
}
