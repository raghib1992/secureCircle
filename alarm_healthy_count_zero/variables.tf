# variable "region" {
#     default = "ap-south-1" 
# }

# variable "name_prefix" {
#     default = "raghib-test"  
# }

# variable "nlb_http_health_checks_enabled" {
#     type = bool
#     default = true  
# }

# variable "regional_saas_alerts_topic_id" {
#     type = string
#     default = ""  
# }

# variable "domainname" {
#   type = string
#   default = "ap1.saas.securecircle.com"
# }

# variable "spot_max_price" {
#   type = number
#   default = 0.0188
#   description = "Maximum price to pay for spot instances"
# }

# variable "asg_lt_instance_type_overrides" {
#   type = map(list(object({instance_type = string})))
#   default = {
#     us-west-2 = [
#       {
#         instance_type = "t3a.small"
#       },
#       {
#         instance_type = "t3.small"
#       },
#       {
#         instance_type = "t2.medium"
#       },
#       {
#         instance_type = "m5a.large"
#       },
#       {
#         instance_type = "m5.large"
#       },
#       {
#         instance_type = "m4.large"
#       },
#       {
#         instance_type = "c5.large"
#       },
#       {
#         instance_type = "c4.large"
#       }
#     ],
#     us-east-2 = [
#       {
#         instance_type = "t3a.small"
#       },
#       {
#         instance_type = "t3.small"
#       },
#       {
#         instance_type = "t2.medium"
#       },
#       {
#         instance_type = "m5a.large"
#       },
#       {
#         instance_type = "m5.large"
#       },
#       {
#         instance_type = "m4.large"
#       },
#       {
#         instance_type = "c5.large"
#       },
#       {
#         instance_type = "c4.large"
#       }
#     ],
#     ap-south-1 = [
#       {
#         instance_type = "t3a.small"
#       },
#       {
#         instance_type = "t3.small"
#       },
#       {
#         instance_type = "t2.medium"
#       },
#       {
#         instance_type = "m5a.large"
#       },
#       {
#         instance_type = "m5.large"
#       },
#       {
#         instance_type = "m4.large"
#       },
#       {
#         instance_type = "c5.large"
#       },
#       {
#         instance_type = "c4.large"
#       }
#     ],
#     ap-southeast-1 = [
#       {
#         instance_type = "t3a.small"
#       },
#       {
#         instance_type = "t3.small"
#       },
#       {
#         instance_type = "t2.medium"
#       },
#       {
#         instance_type = "m5a.large"
#       },
#       {
#         instance_type = "m5.large"
#       },
#       {
#         instance_type = "m4.large"
#       },
#       {
#         instance_type = "c5.large"
#       },
#       {
#         instance_type = "c4.large"
#       }
#     ],
#     ap-northeast-1 = [
#       {
#         instance_type = "t3a.small"
#       },
#       {
#         instance_type = "t3.small"
#       },
#       {
#         instance_type = "t2.medium"
#       },
#       {
#         instance_type = "m5a.large"
#       },
#       {
#         instance_type = "m5.large"
#       },
#       {
#         instance_type = "m4.large"
#       },
#       {
#         instance_type = "c5.large"
#       },
#       {
#         instance_type = "c4.large"
#       }
#     ]
#     eu-west-1 = [
#       {
#         instance_type = "t3a.small"
#       },
#       {
#         instance_type = "t3.small"
#       },
#       {
#         instance_type = "t2.medium"
#       },
#       {
#         instance_type = "m5a.large"
#       },
#       {
#         instance_type = "m5.large"
#       },
#       {
#         instance_type = "m4.large"
#       },
#       {
#         instance_type = "c5.large"
#       },
#       {
#         instance_type = "c4.large"
#       }
#     ],
#     me-south-1 = [
#       {
#         instance_type = "t3.small"
#       },
#       {
#         instance_type = "t3.medium"
#       },
#       {
#         instance_type = "m5.large"
#       },
#       {
#         instance_type = "c5.large"
#       }
#     ],
#     sa-east-1 = [
#       {
#         instance_type = "t3a.small"
#       },
#       {
#         instance_type = "t3.small"
#       },
#       {
#         instance_type = "t2.medium"
#       },
#       {
#         instance_type = "m5a.large"
#       },
#       {
#         instance_type = "m5.large"
#       },
#       {
#         instance_type = "m4.large"
#       },
#       {
#         instance_type = "c5.large"
#       },
#       {
#         instance_type = "c4.large"
#       }
#     ]
#   }
# }

# variable "vpc_cidr_block" {
#   type = string
#   default = "192.168.180.0/24"
#   description = "VPC CIDR Block"
# }

# variable "private_subnet_cidrs" {
#   type = list(string)
#   default = [
#     "192.168.180.0/26",
#     "192.168.180.64/26"
#   ]
#   description = "Subnet ranges"
# }

# variable "public_subnet_cidrs" {
#   type = list(string)
#   default = [
#     "192.168.180.128/26",
#     "192.168.180.192/26"
#   ]
#   description = "Subnet ranges"
# }

# variable "eipcount" {
#   default = 2
# }

# variable "ipsec_vpn_map" {
#   type = map(object({
#       remote_private_subnet_cidrs = list(string)
#       dynamic = bool
#     })
#   )
#   default = {}
# }

# variable "glowroot_subnets" {
#   type = list(string)
#   default = [
#     "96.72.187.0/29"
#   ]
#   description = "Subnet ranges"
# }

# variable "percent_on_demand" {
#   default = 10
# }
