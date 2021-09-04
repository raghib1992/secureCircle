#!/bin/bash

# install audit deamon
echo
echo "Installing audit deamon into your server"
echo
sudo yum install audit -y
echo
echo "Successfully install the audit deamon"
echo "**************************************"

# create a rules for audit
if [ "$(whoami)" != "root" ]
then
        sudo su - <<EOF
        "$(sed -i -e '$a-a always,exit -F arch=b64 -S rename,rmdir,unlink,unlinkat,renameat -F auid>=500 -F auid!=-1 -F dir=/ -F key=delete\n-w /bin/sudo -p rwxa -k sudo\n-a never,exclude -F dir=/var/log -k exclude_dir' /etc/audit/rules.d/audit.rules)"
        exit
        EOF
else
sed -i -e '$a-a always,exit -F arch=b64 -S rename,rmdir,unlink,unlinkat,renameat -F auid>=500 -F auid!=-1 -F dir=/ -F key=delete\n-w /bin/sudo -p rwxa -k sudo\n-a never,exclude -F dir=/var/log -k exclude_dir' /etc/audit/rules.d/audit.rules
fi
echo
EOF
echo
echo "successfully edit the the audit.rules file"
echo "*****************************************"
echo
echo "Starting the audit services"
chkconfig auditd on

service auditd start

service auditd stop

service auditd restart