#!/bin/bash

# become root user
sudo su

#Install awslogs
echo "Updating the os"
yum update -y

yum install awslogs -y

sed -i -e '$a[/var/log/audit/audit.log]\ndatetime_format = %b %d %H:%M:%S\nfile = /var/log/audit/audit.log\nbuffer_duration = 5000\nlog_stream_name = {instance_id}\ninitial_position = start_of_file\nlog_group_name = /var/log/audit/audit.log' /etc/awslogs/awslogs.conf

#start awslogs service
systemctl start awslogsd
systemctl enable awslogsd.service