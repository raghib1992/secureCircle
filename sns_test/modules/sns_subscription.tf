resource "aws_sns_topic_subscription" "accountLogin_sns_subcription" {
  topic_arn = "${var.SNS_TOPIC}".arn
  protocol  = "email"
  endpoint  = "raghib.nadim@folium.cloud"
}

variable "SNS_TOPIC"{
    description = "this is for test"
}
variable "caller" {
  description = "test"
}

variable "aws_region" {
  description = "this is for test"
}