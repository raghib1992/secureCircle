module "ses_bounce_monitor" {
    source     = "./modules/"
    aws_region = local.region
    caller_id  = data.aws_caller_identity.current.id
    sns_topic  = aws_sns_topic.regional_saas_alerts
}