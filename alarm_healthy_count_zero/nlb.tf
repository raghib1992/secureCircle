# resource "aws_lb" "ec2-nlb" {
#  internal           = false
#  load_balancer_type = "network"
#  name               = "saas-${var.name_prefix}-ec2-nlb"
#  subnet_mapping {
#   subnet_id = aws_subnet.public_0.id
#   allocation_id = aws_eip.nlb-eip[0].id
#  }

#  subnet_mapping {
#   subnet_id = aws_subnet.public_1.id
#   allocation_id = aws_eip.nlb-eip[1].id
#  }

#  enable_deletion_protection = true
#  enable_cross_zone_load_balancing = true

#  tags = local.common_tags

#  depends_on = [aws_internet_gateway.gw]
 
#  lifecycle {
#     prevent_destroy = true
#   }
# }

# resource "aws_lb_target_group" "ec2-nlb-target-group" {
#     name                = "${var.name_prefix}-ec2-nlb-tg-group"
#     vpc_id              = aws_vpc.mumbai-vpc.id
#     port                = "80"
#     protocol            = "TCP"
#     health_check {
#         healthy_threshold   = "3"
#         unhealthy_threshold   = "3"
#         interval            = "10"
#         port                = "80"
#         path                = var.nlb_http_health_checks_enabled ? "/index.html" : null
#         protocol            = var.nlb_http_health_checks_enabled ?  "HTTP" : "TCP"
#     }
    
#     deregistration_delay = 300

#     lifecycle {
#         create_before_destroy = true
#         # prevent_destroy = true
#     }

#     tags = merge(
#              local.common_tags,
#              {
#                Name = "${var.name_prefix}-ec2-nlb-target-group"
#              }
#     )   
# }

# resource "aws_lb_listener" "nlb-listener-443" {
#     load_balancer_arn = aws_lb.ec2-nlb.arn
#     port              = "80"
#     protocol          = "TCP"
#     # ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
#     # certificate_arn   = aws_acm_certificate_validation.mumbai-cert.certificate_arn
#     default_action {
#        target_group_arn = aws_lb_target_group.ec2-nlb-target-group.arn
#        type             = "forward"
#    }

#    lifecycle {
#         # create_before_destroy = false
#         prevent_destroy = true
#     }
# }