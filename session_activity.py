import json
import gzip
import base64
import boto3
import os
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# def lambda_handler(event, context):
def lambda_handler():
    # cloudwatch_log = event["awslogs"]["data"]
    cloudwatch_log = 'H4sIAAAAAAAAALVSTYvbMBD9K8LtratEX5Zs59BNabqFsqfsLQlBsVVHYEtBkpuWZf97x/mgpCxlLwUhDfPevKcZ5jnrTYy6NU+/Diarss/zp/n2cbFczh8W2V3mj84ESLOikEoRTqjIId359iH44QCIPkZcd35oUtC2w4BEHHS7tzucTExn8jIFo3tgn5GJ043t76Oph2BqG+rOTGrfY1J8F+VO6V1OCSE1lVAdh12sgz0k690X2yUTYlatsgi/hswWxLPNyWPxw7g0Ys+ZbcCKSy5yqeCRiiiqmOA5U5IXsuCSccUUK0VZCKXyvGBSlSTnlCgGnsnCUJLuoT8qWalKCfRC8rvrsEB+efoUAlpIpkHeIUYYhRYwE4iUFWVVTj9AG2Tt1gMh9NPqIyVc7OMeiwl7j9bhkv52zcSh8XCNyKVkQ2bB+3RvDxgawJxiLjAj1XSIYbqzJxZRN/Kr1woQcDfvUN2g6d73ZmpqhodowvQNVjcFZ8PXPa4cMOoiwl0Ko3rySXeIjGETjj8DHg9iaJQ4XxLNhxaNU5MVF+jSDekvAS9m+Yypftwm69qtd62H9w/tLcplRST6S/C8i1vd9NbdqP2HgXzVrh0OJ3F32ZzGO/OvtcleNi+/AUTHc2CeAwAA'
    decode_base64 = base64.b64decode(cloudwatch_log)
    decompress_data = gzip.decompress(decode_base64)
    log_data = json.loads(decompress_data)
    session_log = log_data['logEvents'][0]['message']
    print(session_log)


lambda_handler()



# {'messageType': 'DATA_MESSAGE', 'owner': '288677030145', 'logGroup': 'aws-cloudtrail-logs-raghib-test', 'logStream': 'raghib.nadim@securecircle.com-08f49b7ab51000c16', 'subscriptionFilters': ['session_log'], 'logEvents': [{'id': '36345673636707172435276386836237272949847755826790531072', 'timestamp': 1629796372863, 'message': 'Script started on 2021-08-24 09:12:51+0000\n\x1b[?1034hsh-4.2$ \r\x1b[Ksh-4.2$ sudo su \r\n\x1b]0;root@ip-172-31-34-20:/usr/bin\x07\x1b[?1034h[root@ip-172-31-34-20 bin]# cd /home/ec2-user/\r\n\x1b]0;root@ip-172-31-34-20:/home/ec2-user\x07[root@ip-172-31-34-20 ec2-user]# ls -ltr\r\ntotal 0\r\ndrwxr-xr-x 2 root root 6 Aug 24 06:34 \x1b[0m\x1b[38;5;27mtesting_ongoing\x1b[0m\r\ndrwxr-xr-x 2 root root 6 Aug 24 09:06 \x1b[38;5;27mraghib_admin\x1b[0m\r\n\x1b]0;root@ip-172-31-34-20:/home/ec2-user\x07[root@ip-172-31-34-20 ec2-user]# Hangup\r\n\nScript done on 2021-08-24 09:12:51+0000'}]}