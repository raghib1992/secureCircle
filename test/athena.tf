resource "aws_s3_bucket" "trail_workgroup_result" {
  bucket = "trail-workgroup-result"
}

resource "aws_athena_database" "trail_login_db" {
  name   = "trail_login_db"
  bucket = aws_s3_bucket.trail_login_details.id
}

resource "aws_athena_workgroup" "trail_workgroup" {
  name = "trail_workgroup"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.trail_workgroup_result.bucket}/output/"

    #   encryption_configuration {
    #     encryption_option = "SSE_KMS"
    #     kms_key_arn       = aws_kms_key.example.arn
    #   }
    }
  }
}

resource "aws_athena_named_query" "trail_login_data" {
  name      = "trail-login-data"
  workgroup = aws_athena_workgroup.trail_workgroup.id
  database  = aws_athena_database.trail_login_db.name
  query     = <<EOF
  "CREATE EXTERNAL TABLE cloudtrail_logs (
    eventVersion STRING,
    userIdentity STRUCT<
        type: STRING,
        principalId: STRING,
        arn: STRING,
        accountId: STRING,
        invokedBy: STRING,
        accessKeyId: STRING,
        userName: STRING,
        sessionContext: STRUCT<
            attributes: STRUCT<
                mfaAuthenticated: STRING,
                creationDate: STRING>,
            sessionIssuer: STRUCT<
                type: STRING,
                principalId: STRING,
                arn: STRING,
                accountId: STRING,
                userName: STRING>>>,
    eventTime STRING,
    eventSource STRING,
    eventName STRING,
    awsRegion STRING,
    sourceIpAddress STRING,
    userAgent STRING,
    errorCode STRING,
    errorMessage STRING,
    requestParameters STRING,
    responseElements STRING,
    additionalEventData STRING,
    requestId STRING,
    eventId STRING,
    resources ARRAY<STRUCT<
        arn: STRING,
        accountId: STRING,
        type: STRING>>,
    eventType STRING,
    apiVersion STRING,
    readOnly STRING,
    recipientAccountId STRING,
    serviceEventDetails STRING,
    sharedEventID STRING,
    vpcEndpointId STRING
)
COMMENT 'CloudTrail table for trail-login-details bucket'
ROW FORMAT SERDE 'com.amazon.emr.hive.serde.CloudTrailSerde'
STORED AS INPUTFORMAT 'com.amazon.emr.cloudtrail.CloudTrailInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://trail-login-details/AWSTrail/AWSLogs/'
TBLPROPERTIES ('classification'='cloudtrail');"
  EOF
}