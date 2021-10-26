resource "aws_eks_cluster" "jenkins-eks-fg-saas-01" {
  name     = "jenkins-eks-fg-saas-01"
  role_arn = aws_iam_role.jenkins-eks-fg-saas-01-cluster-ServiceRole_role.arn

  vpc_config {
    security_group_ids = [aws_security_group.eks-ControlPlaneSecurityGroup.id, aws_security_group.eks-SharedNodeSecurityGroup.id]
    subnet_ids         = [aws_subnet.private_0.id,aws_subnet.private_1.id,aws_subnet.private_2.id,aws_subnet.public_0.id,aws_subnet.public_1.id,aws_subnet.public_2.id]
  }

#   depends_on = [
#     aws_iam_role_policy_attachment.eks-cluster-attach_policy,
#     aws_iam_role_policy_attachment.eks-vpc-attach_policy,
#     aws_iam_role_policy_attachment.eks-cloudwatch-metric-attach_policy,
#     aws_iam_role_policy_attachment.eks_elb_policy-attach_policy,
#   ]
}
