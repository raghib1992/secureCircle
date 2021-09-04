data "archive_file" "code_activate" {
  type        = "zip"
  source_file = "./modules/lambda_function_activate.py"
  output_path = "./modules/lambda_function_activate.zip"
}

resource "aws_lambda_event_source_mapping" "ses-email-activate-lambda-trigger" {
  event_source_arn  = aws_dynamodb_table.ses_email_dynoTable.stream_arn
  function_name     = aws_lambda_function.ses_email_activate.arn
  starting_position = "LATEST"
}

resource "aws_lambda_function" "ses_email_activate" {
  filename         = data.archive_file.code_activate.output_path
  function_name    = "ses_email_activate"
  role             = aws_iam_role.lambda_ses_email_activation_role.arn
  handler          = "lambda_function_activate.lambda_handler"
  source_code_hash = data.archive_file.code_activate.output_base64sha256
  runtime          = "python3.7"
  timeout          = 63
  environment {
    variables = {
      snsTopicArn = var.sns_topic.arn
    }
  }
}