provider "aws" {
    region = "ap-south-1"
}

# resource "aws_instance" "web" {
#   ami           = "ami-04db49c0fb2215364"
#   instance_type = "t3.micro"
#   user_data     = data.template_file.series.rendered
#   key_name = "sc-mumbai-key"
#   security_groups = ["sc-mumbai-sg"]
#   iam_instance_profile = aws_iam_instance_profile.test_profile.name

#   tags = {
#     Name = "usertemplate"
#   }
# }

# data "template_file" "series" {
#   template = file("userdata.template")
# }

# output "test" {
#     value = data.template_file.series
# }