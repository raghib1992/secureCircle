resource "aws_eks_fargate_profile" "eks-fg" {
  cluster_name           = aws_eks_cluster.jenkins-eks-fg-saas-01.name
  fargate_profile_name   = "fg-profile"
  pod_execution_role_arn = aws_iam_role.fg-role.arn
  subnet_ids             = [aws_subnet.private_0.id,aws_subnet.private_1.id,aws_subnet.private_2.id]

  selector {
    namespace = "default"
  }
}

resource "aws_iam_role" "fg-role" {
  name = "eks-fargate-profile"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks-fargate-pods.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "AmazonEKSFargatePodExecutionRolePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy"
  role       = aws_iam_role.fg-role.name
}