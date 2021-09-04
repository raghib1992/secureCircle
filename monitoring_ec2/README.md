## Run the following command to install the audit package

```
sudo yum install audit #REDHAT and Centos
sudo zypper install audit #SUSE
sudo apt install auditd #Ubuntu
```
## Command to get list of file system
```
mount | column -t
```

## command to find where file system is mounted
```
findmnt
```

## command to monitor all activity where your file system is mounted
```
auditctl -w / -k efs_changes
```

## command to check logs
```
ausearch -k efs_changes
ausearch -k efs_changes | aureport -f -i
```

