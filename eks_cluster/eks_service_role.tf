resource "aws_iam_role" "jenkins-eks-fg-saas-01-cluster-ServiceRole_role" {
  name = "jenkins-eks-fg-saas-01-cluster-ServiceRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "eks-cluster-attach_policy" {
  name       = "eks-cluster-policy"
  roles      = [aws_iam_role.jenkins-eks-fg-saas-01-cluster-ServiceRole_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_iam_policy_attachment" "eks-vpc-attach_policy" {
  name       = "eks-vpc-policy"
  roles      = [aws_iam_role.jenkins-eks-fg-saas-01-cluster-ServiceRole_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
}

resource "aws_iam_policy_attachment" "eks-cloudwatch-metric-attach_policy" {
  name       = "eks-vpc-policy"
  roles      = [aws_iam_role.jenkins-eks-fg-saas-01-cluster-ServiceRole_role.name]
  policy_arn = aws_iam_policy.eks_cloudwatch_metric_policy.arn
}

resource "aws_iam_policy_attachment" "eks_elb_policy-attach_policy" {
  name       = "eks-elb-policy"
  roles      = [aws_iam_role.jenkins-eks-fg-saas-01-cluster-ServiceRole_role.name]
  policy_arn = aws_iam_policy.eks_elb_policy.arn
}

resource "aws_iam_policy" "eks_cloudwatch_metric_policy" {
  name = "ieks_cloudwatch_metric_policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "cloudwatch:PutMetricData"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
EOF
}

resource "aws_iam_policy" "eks_elb_policy" {
  name = "iamUserAccessKeyRotation_policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "ec2:DescribeAccountAttributes",
                "ec2:DescribeAddresses",
                "ec2:DescribeInternetGateways"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
EOF
}