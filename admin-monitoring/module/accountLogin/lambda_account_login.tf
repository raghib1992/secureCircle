data "archive_file" "code" {
  type        = "zip"
  source_file = "./module/accountLogin/lambda_function.py"
  output_path = "./module/accountLogin/lambda_function.zip"
}

output "archive_zip" {
  value = "data.archive_file.code"
}

resource "aws_lambda_permission" "logging" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.accountLogin_send_notification.function_name
  principal     = var.Lambda_accountLogin_principal
  source_arn    = "${aws_cloudwatch_log_group.trail_consoleLog_data.arn}:*"
}

resource "aws_lambda_function" "accountLogin_send_notification" {
  filename      = data.archive_file.code.output_path
  function_name = "accountLogin_send_notification"
  role          = aws_iam_role.lambda_accountLogin_role.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.code.output_base64sha256
  runtime = "python3.7"
  timeout = 60
  environment {
    variables = {
      snsTopicArn = var.sns_topic.arn
      REGION = var.aws_region
    }
  }
}
