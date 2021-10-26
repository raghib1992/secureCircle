# locals {
#   hostname = substr(sha256("${var.name_prefix}:ponyo"),-10,-1)
# }

# output "hostname" {
#   value = "${local.hostname}.${var.domainname}"
# }

# data "template_file" "ec2-userdata" {
#   template = file("userdata.template")
# }

# resource "aws_launch_template" "mumbai-ec2-lt" {
#   name_prefix = "${var.name_prefix}-mumbai-ec2-lt-"
#   image_id = data.aws_ami.amazon-linux-2.id
#   instance_type = "t2.micro"
#   #network_interfaces {
#   #  associate_public_ip_address = true
#   #}
#   user_data = base64encode(data.template_file.ec2-userdata.rendered)
#   vpc_security_group_ids = [ aws_security_group.mumbai-ec2-sg.id ]
#   # iam_instance_profile {
#   #   arn = aws_iam_instance_profile.ecs-instance-profile.arn
#   # }
#   instance_initiated_shutdown_behavior = "terminate"

#   credit_specification {
#     cpu_credits = "unlimited"
#   }

#   tag_specifications {
#       resource_type = "instance"
#       tags = merge(
#                local.common_tags,
#                {
#                  Name = "${var.name_prefix}-saas-member"
#                }
#       )
#   }
#   tags = local.common_tags
# }

# resource "aws_autoscaling_group" "mumbai-ec2-asg" {

#   mixed_instances_policy {
#     instances_distribution {
#       on_demand_allocation_strategy = "prioritized"
#       on_demand_percentage_above_base_capacity = var.percent_on_demand
#       spot_allocation_strategy = "capacity-optimized"
#       spot_max_price = var.spot_max_price
#     }

#     launch_template {
#       launch_template_specification {
#         launch_template_id = aws_launch_template.mumbai-ec2-lt.id
#         version = "$Latest"
#       }
#       dynamic "override" {
#         for_each = var.asg_lt_instance_type_overrides[var.region]
#         content {
#           instance_type = override.value.instance_type
#         }
#       }
#     }
#   }
#   name_prefix = "${var.name_prefix}-ec2-asg-"
#   max_size = 2
#   min_size = 2
#   desired_capacity = 2
#   vpc_zone_identifier = [aws_subnet.private_0.id, aws_subnet.private_1.id]
#   health_check_grace_period = 900
#   health_check_type = "ELB"
#   target_group_arns = [aws_lb_target_group.ec2-nlb-target-group.arn]
#   wait_for_capacity_timeout = "15m"
#   wait_for_elb_capacity = 1
#   tag {
#     key = "Name"
#     value = "${var.name_prefix}-ec2-member"
#     propagate_at_launch = true
#   }
#   dynamic "tag" {
#     for_each = local.common_tags
#     content {
#       key = tag.key
#       value = tag.value
#       propagate_at_launch = true
#     }
#   }
# }