data "aws_sns_topic" "regional_saas_alerts_sns_topic" {
  name = "raghib-sns-test"
}
data "aws_lb" "raghib-lb-test" {
  name = "raghib-lb-test"
}
data "aws_lb_target_group" "raghib-tg-test" {
  name = "raghib-tg-test"
}

resource "aws_cloudwatch_metric_alarm" "lb_healthy_host_count_alarm" {
  alarm_name = "raghib-lb-healthy-host-count-alarm"
  comparison_operator = "LessThanOrEqualToThreshold"
  dimensions = {
    LoadBalancer = data.aws_lb.raghib-lb-test.arn_suffix
    TargetGroup = data.aws_lb_target_group.raghib-tg-test.arn_suffix
  }
  evaluation_periods = 1
  metric_name = "HealthyHostCount"
  namespace = "AWS/NetworkELB"
  period = 60
  statistic = "Minimum"
  threshold = 0
  treat_missing_data = "breaching"
  alarm_actions = [ data.aws_sns_topic.regional_saas_alerts_sns_topic.arn ]
  tags = local.common_tags
  # depends_on = [
  #   aws_autoscaling_group.mumbai-ec2-asg
  # ]
}

