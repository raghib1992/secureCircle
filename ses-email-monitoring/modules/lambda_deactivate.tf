data "archive_file" "code_deactivate" {
  type        = "zip"
  source_file = "./modules/lambda_function_deactivate.py"
  output_path = "./modules/lambda_function_deactivate.zip"
}

data "aws_s3_bucket" "saas_bucket" {
  bucket = "saas-ses-email-monitor"
}

resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  bucket = data.aws_s3_bucket.saas_bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.ses_email_deactivate.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ses_email_deactivate.arn
  principal     = "s3.amazonaws.com"
  source_arn    = data.aws_s3_bucket.saas_bucket.arn
}

resource "aws_lambda_function" "ses_email_deactivate" {
  filename      = data.archive_file.code_deactivate.output_path
  function_name = "ses_email_deactivate"
  role          = aws_iam_role.lambda_ses_email_deactivation_role.arn
  handler       = "lambda_function_deactivate.lambda_handler"
  source_code_hash = data.archive_file.code_deactivate.output_base64sha256
  runtime = "python3.7"
  timeout = 63
  
}