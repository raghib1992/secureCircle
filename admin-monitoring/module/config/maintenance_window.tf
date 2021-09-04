resource "aws_ssm_maintenance_window" "SecurityUpdateWindow" {
  name     = "yumSecurityUpdate"
  schedule = "cron(0 */30 * * * ? *)"
  duration = 1
  cutoff   = 0
}

resource "aws_ssm_maintenance_window_target" "SecurityUpdateTarget" {
  window_id     = aws_ssm_maintenance_window.SecurityUpdateWindow.id
  name          = "SecurityUpdateTarget"
  description   = "This is a maintenance window target to update security"
  resource_type = "INSTANCE"


  targets {
    key    = "tag:sc_purpose"
    values = ["${var.SC_PURPOSE}"]
  }
}

resource "aws_ssm_maintenance_window_task" "SecurityUpdateTask" {
  max_concurrency = 1
  max_errors      = 0
  task_arn        = "AWS-RunShellScript"
  task_type       = "RUN_COMMAND"
  window_id       = aws_ssm_maintenance_window.SecurityUpdateWindow.id
  
  
  targets {
    key    = "WindowTargetIds"
    values = [aws_ssm_maintenance_window_target.SecurityUpdateTarget.id]
  }

  task_invocation_parameters {
    run_command_parameters {
      timeout_seconds      = 600

      notification_config {
        notification_arn    = data.aws_sns_topic.yumSecurityUpdateFailedNotification.arn
        notification_events = ["Failed", "TimedOut", "Cancelled"]
        notification_type   = "Command"
      }
      cloudwatch_config {
        cloudwatch_log_group_name = "SSMRunCommand"
        cloudwatch_output_enabled = true
      }
      parameter {
        name   = "commands"
        values = ["yum -t -y --exclude=kernel --exclude=nvidia* --exclude=cuda* --security --sec-severity=critical --sec-severity=important upgrade"]
      }
    }
  }
}