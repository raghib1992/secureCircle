resource "aws_security_group" "eks-ControlPlaneSecurityGroup" {
  name = "eksctl-jenkins-eks-fg-raghib-cluster-ControlPlaneSecurityGroup"
  vpc_id = aws_vpc.eks-vpc.id

  tags = {
      Name = "eksctl-jenkins-eks-fg-raghib-cluster/ControlPlaneSecurityGroup"
  }
}

resource "aws_security_group_rule" "egress-1" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.eks-ControlPlaneSecurityGroup.id
}

resource "aws_security_group" "eks-SharedNodeSecurityGroup" {
  name = "eksctl-jenkins-eks-fg-saas-01-cluster-ClusterSharedNodeSecurityGroup"
  vpc_id = aws_vpc.eks-vpc.id

  tags = {
      Name = "eksctl-jenkins-eks-fg-saas-01-cluster/ClusterSharedNodeSecurityGroup"
  }
}


# data "aws_security_group" "selected" {
#   id = "sg-0e78d129b26438465"
# }

resource "aws_security_group_rule" "ingress-1" {
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.eks-SharedNodeSecurityGroup.id
}

# resource "aws_security_group_rule" "ingress-2" {
#   type              = "ingress"
#   from_port         = 0
#   to_port           = 0
#   protocol          = "-1"
#   cidr_blocks       = ["0.0.0.0/0"]
#   security_group_id = data.aws_security_group.selected.id
# }

resource "aws_vpc" "eks-vpc" {
  cidr_block = var.vpc_cidr_block
  assign_generated_ipv6_cidr_block = false
  enable_dns_hostnames = false
  tags = {
    Name = "eksctl-jenkins-eks-fg-saas-01-cluster/VPC"
  }
}

data "aws_availability_zones" "available" {}

resource "aws_subnet" "private_0" {
  vpc_id = aws_vpc.eks-vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]
  cidr_block = var.private_subnet_cidrs[0]
  map_public_ip_on_launch = false
  
  tags = tomap({
    "Name"                                      = "eksctl-jenkins-eks-fg-saas-01-cluster/Subnet-private-${data.aws_availability_zones.available.names[0]}",
    "kubernetes.io/cluster/jenkins-eks-fg-saas-01" = "jenkins-eks-fg-saas-01",
  })
}

resource "aws_subnet" "private_1" {
  vpc_id = aws_vpc.eks-vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]
  cidr_block = var.private_subnet_cidrs[1]
  map_public_ip_on_launch = false
  
  tags = tomap({
    "Name"                                      = "eksctl-jenkins-eks-fg-saas-01-cluster/Subnet-private-${data.aws_availability_zones.available.names[1]}",
    "kubernetes.io/cluster/jenkins-eks-fg-saas-01" = "jenkins-eks-fg-saas-01",
  })
}

resource "aws_subnet" "private_2" {
  vpc_id = aws_vpc.eks-vpc.id
  availability_zone = data.aws_availability_zones.available.names[2]
  cidr_block = var.private_subnet_cidrs[2]
  map_public_ip_on_launch = false
  
  tags = tomap({
    "Name"                                      = "eksctl-jenkins-eks-fg-saas-01-cluster/Subnet-private-${data.aws_availability_zones.available.names[2]}",
    "kubernetes.io/cluster/jenkins-eks-fg-saas-01" = "jenkins-eks-fg-saas-01",
  })
}

resource "aws_subnet" "public_0" {
  vpc_id = aws_vpc.eks-vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]
  cidr_block = var.public_subnet_cidrs[0]
  map_public_ip_on_launch = true
  
  tags = tomap({
    "Name"                                      = "eksctl-jenkins-eks-fg-saas-01-cluster/Subnet-public-${data.aws_availability_zones.available.names[0]}",
    "kubernetes.io/cluster/jenkins-eks-fg-saas-01" = "jenkins-eks-fg-saas-01",
  })
}

resource "aws_subnet" "public_1" {
  vpc_id = aws_vpc.eks-vpc.id
  availability_zone = data.aws_availability_zones.available.names[1]
  cidr_block = var.public_subnet_cidrs[1]
  map_public_ip_on_launch = true
    tags = tomap({
    "Name"                                      = "eksctl-jenkins-eks-fg-saas-01-cluster/Subnet-public-${data.aws_availability_zones.available.names[1]}",
    "kubernetes.io/cluster/jenkins-eks-fg-saas-01" = "jenkins-eks-fg-saas-01",
  })
}

resource "aws_subnet" "public_2" {
  vpc_id = aws_vpc.eks-vpc.id
  availability_zone = data.aws_availability_zones.available.names[2]
  cidr_block = var.public_subnet_cidrs[2]
  map_public_ip_on_launch = true
  tags = tomap({
    "Name"                                      = "eksctl-jenkins-eks-fg-saas-01-cluster/Subnet-public-${data.aws_availability_zones.available.names[2]}",
    "kubernetes.io/cluster/jenkins-eks-fg-saas-01" = "jenkins-eks-fg-saas-01",
  })
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.eks-vpc.id
  tags = {
    Name = "eksctl-jenkins-eks-fg-saas-01-cluster/InternetGateway"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.eks-vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
  tags = {
    Name = "eksctl-jenkins-eks-fg-saas-01-cluster/PublicRouteTable"
  }

  depends_on = [aws_internet_gateway.gw]
}

resource "aws_route_table_association" "public_0" {
  subnet_id = aws_subnet.public_0.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_1" {
  subnet_id = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_2" {
  subnet_id = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}

resource "aws_eip" "nat-eip" {
  vpc      = true
  tags = {
    Name = "eksctl-jenkins-eks-fg-saas-01-cluster/NATIP"
  }
}

resource "aws_nat_gateway" "public" {
  allocation_id = aws_eip.nat-eip.id
  subnet_id     = aws_subnet.public_0.id

  tags = {
    Name = "eksctl-jenkins-eks-fg-saas-01-cluster/NATGateway"
  }
  depends_on = [aws_internet_gateway.gw]
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.eks-vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.public.id
  }
  tags = {
    Name = "eksctl-jenkins-eks-fg-saas-01-cluster/PrivateRouteTable"
  }
}

resource "aws_route_table_association" "private_0" {
  subnet_id = aws_subnet.private_0.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_1" {
  subnet_id = aws_subnet.private_1.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id = aws_subnet.private_2.id
  route_table_id = aws_route_table.private.id
}
