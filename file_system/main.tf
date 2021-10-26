data "aws_ami" "amazon-linux-2" {
 most_recent = true
 owners      = ["amazon"]

 filter {
   name   = "name"
   values = ["amzn2-ami-hvm*-x86_64-ebs"]
 }
}

locals {
  common_tags = {
    sc_purpose = "testing"
    sc_customer = "sankalan"
  }
}

resource "aws_iam_instance_profile" "test_profile" {
  name = "filesystem_instance_profile"
  role = aws_iam_role.awslogs_ec2_role.name
}

resource "aws_launch_template" "raghib_launch_template" {
  name_prefix = "raghib_launch_template"
  image_id = data.aws_ami.amazon-linux-2.id
  instance_type = "t3.micro"
  #network_interfaces {
  #  associate_public_ip_address = true
  #}
  user_data = base64encode(data.template_file.ec2-userdata.rendered)
#   vpc_security_group_ids = [ aws_security_group.mumbai-ec2-sg.id ]
  iam_instance_profile {
    arn = aws_iam_instance_profile.test_profile.arn
  }
  instance_initiated_shutdown_behavior = "terminate"
  key_name = "sc-mumbai-key"
  security_group_names = ["sc-mumbai-sg"]

  credit_specification {
    cpu_credits = "unlimited"
  }

  tag_specifications {
      resource_type = "instance"
      tags = merge(
               local.common_tags,
               {
                 Name = "raghib-saas-member"
               }
      )
  }
  tags = local.common_tags
}

data "template_file" "ec2-userdata" {
  template = file("userdata.template")
}

