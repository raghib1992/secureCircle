# resource "aws_security_group" "mumbai-ec2-sg" {
#   name = "${var.name_prefix}-ec2-sg"
#   vpc_id = aws_vpc.mumbai-vpc.id

#   ingress {
#     from_port = 443
#     to_port = 443
#     protocol = "tcp"
#     cidr_blocks = [ "0.0.0.0/0" ]
#     ipv6_cidr_blocks = [ "::/0" ]
#   }

#   ingress {
#     from_port = 4443
#     to_port = 4443
#     protocol = "tcp"
#     cidr_blocks = [ "0.0.0.0/0" ]
#     ipv6_cidr_blocks = [ "::/0" ]
#   }

#   ingress {
#     from_port = 4444
#     to_port = 4444
#     protocol = "tcp"
#     cidr_blocks = [ "0.0.0.0/0" ]
#     ipv6_cidr_blocks = [ "::/0" ]
#   }

#   ingress {
#     from_port = 8080
#     to_port = 8080
#     protocol = "tcp"
#     cidr_blocks = [ aws_vpc.mumbai-vpc.cidr_block ]
#   }

#   egress {
#     from_port = 0
#     to_port = 0
#     protocol = "-1"
#     cidr_blocks = [ "0.0.0.0/0" ]
#     ipv6_cidr_blocks = [ "::/0" ]
#   }

#   ingress {
#     from_port = 4000
#     to_port = 4000
#     protocol = "tcp"
#     cidr_blocks = var.glowroot_subnets
#   }

#   tags = local.common_tags
# }
