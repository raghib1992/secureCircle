resource "aws_cloudwatch_log_metric_filter" "filesystemLog" {
  name           = "filesystemLog"
  pattern        = "filesystemLogs"
  log_group_name = "/var/log/audit/audit.log"

  metric_transformation {
    name      = "filesystemLog"
    namespace = "filesystem"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "filesystemAlarm" {
  alarm_name                = "filesystemAlarm"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "1"
  metric_name               = "filesystemLog"
  namespace                 = "filesystem"
  period                    = 60
  statistic                 = "Sum"
  threshold                 = 1
  treat_missing_data = "missing"
  alarm_actions = ["arn:aws:sns:ap-south-1:288677030145:raghib-sns-test"]
  alarm_description         = "This metric monitors ec2 filesystem logs"
}