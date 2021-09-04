#!/bin/bash

# Update the software package of the instance using the below command:
sudo yum update -y
echo
echo 'Successfully update the system'
echo '**************************************************'

# Add the Jenkins repo:
sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo
echo
echo 'Successfully download the Jenkins pkg'
echo '**************************************************'

# Import the key file:
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
echo
echo 'Successfully import the key'
echo '**************************************************'

# Install java packages and remove the oldest version of java if any:
sudo yum install java-openjdk11 -y

echo
echo 'Successfully install Java-1.8.0 and remove Java-1.7.0'
echo '**************************************************'

# Install Jenkins using the below command:
sudo yum install jenkins -y
echo
echo 'Successfully install the jenkins'
echo '**************************************************'

# Start the Jenkins service:
sudo systemctl daemon-reload
sudo systemctl start jenkins
echo
echo 'Successfully start the jenkins service'
echo '**************************************************'

# enable the Jenkins Service
sudo systemctl enable jenkins
echo
echo 'Successfully enable the jenkins service'
echo '**************************************************'

# check the status of Jenkins Service
sudo systemctl status jenkins
echo
echo 'Check the status of jenkins service'
echo '**************************************************'

echo '*******************************************************'
echo 'Jenkins installation script successfully run'
echo '*******************************************************'
