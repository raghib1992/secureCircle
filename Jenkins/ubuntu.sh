#!/bin/bash

# Import the key file:
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
echo
echo 'Successfully import the key'
echo '**************************************************'

# Add the Jenkins repo:
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
echo
echo 'Successfully download the Jenkins pkg'
echo '**************************************************'

# Install java packages and remove the oldest version of java if any:
sudo apt install openjdk-11-jre-headless -y

echo
echo 'Successfully install Java-1.8.0 and remove Java-1.7.0'
echo '**************************************************'

# Update the software package of the instance using the below command:
sudo apt update -y
echo
echo 'Successfully update the system'
echo '**************************************************'

# Install Jenkins using the below command:
sudo apt install jenkins -y
echo
echo 'Successfully install the jenkins'
echo '**************************************************'

# Start the Jenkins service:
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
