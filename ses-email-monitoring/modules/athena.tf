data "aws_s3_bucket" "saas_bucket_query_result" {
  bucket = "saas-ses-email-query-result"
}

resource "aws_athena_database" "saas_athena" {
  name   = "saas_ses_email"
  bucket = data.aws_s3_bucket.saas_bucket_query_result.id
}

resource "aws_athena_named_query" "get_bounce_data" {
  name      = "get-bounce-data"
  database  = aws_athena_database.saas_athena.name
  query     = <<EOF
  CREATE EXTERNAL TABLE sesblog2 ( eventType string, mail struct<`timestamp`:string, source:string, sourceArn:string, sendingAccountId:string, messageId:string, destination:string, headersTruncated:boolean, headers:array<struct<name:string,value:string>>, commonHeaders:struct<`from`:array<string>,to:array<string>,messageId:string,subject:string>, tags:struct<ses_configurationset:string,ses_source_ip:string,ses_from_domain:string,ses_caller_identity:string> > ) ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe' WITH SERDEPROPERTIES ( "mapping.ses_configurationset"="ses:configuration-set", "mapping.ses_source_ip"="ses:source-ip", "mapping.ses_from_domain"="ses:from-domain", "mapping.ses_caller_identity"="ses:caller-identity" ) LOCATION 's3://saas-ses-email-monitor/athena/'
  EOF
}