resource "aws_autoscaling_group" "mumbai-ec2-asg" {

  availability_zones = ["ap-south-1a"]
  desired_capacity   = 2
  max_size           = 3
  min_size           = 2

  launch_template {
    id      = aws_launch_template.raghib_launch_template.id
    version = "$Latest"
  }
}
