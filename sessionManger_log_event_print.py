import json
import gzip
import base64
import boto3
import os
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler():
# def lambda_handler(event, context):
    # cloudwatch_log = event['awslogs']['data']
    cloudwatch_log = 'H4sIAAAAAAAAAJVVbU/jRhD+K5E/s/bu+iW2pap1A4dSClxJ4KQrp2hsb8z2/JLurgkp4r93vA4pRym6SpFi7zz7zMwzL350GqE1VGK52wgndY6zZbY6P1ksstMT58jptq1QeMzjOJpOqU9ZEOJx3VWnqus3aNGFBtCkqLu+NApkTXpNtkIbwkfgwigBzSuO1WzALwf86iVe97kulNwY2bUfZG2E0k76+0BTybZaLQwos8CA0ex8sfQn96I1A+jRkSV68SPfp34ShegppEES8iT2kzCKOEu4HwQJp1M/DinjjFE+ZRFlUxrSKTo3ErUw0GBaLOIJY8znYcjCo2eNkP7x1hGDxxuMDIO4ddJbh7k0vnWObp1eCzUv0SrNDi2INaiqxWRa940or7paWOhGybaQG6jn5Wi/usyuTy+WYXiSfbo547NldvMpVVDdydxtoZTNT1oUvRKFVEUt3KJrLA+oMQb8T2GrU210mr5UOoXRM1Ho2oOyka0ma9U1pNK9NML7Dh9F0fWt2Uf6kvzZjPKcid1zKov5IZXwt+vZ54tFZoF6LNysa414MKNA+7M5BinUK83+n1hvyiGheSXHf8jwPYkO5b2AZgzuLYonBG1FPi8/iFIoGJr4GAwMaQ0mMEbJvDdCj4kWOBh7zMjJKWeExoRFS0bTwE99/tl6btaQ9eZu6KwCwWN8a6j14PRp4LZNuZTNW0Shj1wjkYUtul4VI1DrxoUG/upaVOtQcIs6ZPpy6EaZtvpKVM/dfxjfscaWe/4xK0uFV/bR+C6LE5cHiRuwg5RZhV5GLbeaSGwK1ULt+ZPhVZdfyR9wDx5zGf6wCpNfZds/eIGLRFOfUJe5ULicR24cuL7P3UYYqJn7EEerKJhcbkT7y/EZPpKfpVkthLoXanVz7vHQ9SknOY0newexS1d4NMGsy055lwqw+1ezTm26sYiTYl15Shi1I01XCq8WFRQ7m4gSf/aY/UdQKNewrvY9DKoSY3KS0DUr12GUgCjyCHIRjZ2C+my6VouTWjTDDvt2IMYavzucSDylQUTXEE2DOOEBtSGZ7qtob6Dux/LZp8mdLHExTUp8NN3EMuGSmmAHaozBHWtnN/W1qu29rdap52GD7Jefdg+V/rZlvHvmldjmpLiDthX1+xvl30H/OIzkD5s+r6W+W+2/ALl4FsnqOz+2MYko4LyIsbGDxCcBrEsSM78gOWNFmEcJjcL1Px28v+SjRbCyxJKHUxKE64DkgMORJAA5i/AWhX0tobxs62F129k6jNVhiW91tpEzqOtxKqFFXYba2Y8QQozqhSXCbSXxKHt/oVj2GQ501amdhZwfKDF95+nL098H1qvioAcAAA=='
    decode_base64 = base64.b64decode(cloudwatch_log)
    decompress_data = gzip.decompress(decode_base64)
    log_data = json.loads(decompress_data)
    print('successfully get the session manager logs:' +str(log_data))
    print("----------------------------------------------------------------------------------")
    sns_noti = sns_notification(log_data)
    return log_data

def sns_notification(log_data):
    res = log_data["logEvents"][0]["message"]
    filter_log_data = json.loads(res)
    eventDetails = {key: filter_log_data[key] for key in filter_log_data.keys() & {'eventSource','eventName','sourceIPAddress','awsRegion'}}
    extract = filter_log_data['userIdentity']
    userDetails = {key: extract[key] for key in extract.keys() & {'arn','accountId','principalId', 'userName'}}
    print(userDetails)
    print("------------------------------------------------------------------------------------")
    eventtime = log_data['logEvents'][0]['timestamp']/1000
    EventTime = datetime.datetime.fromtimestamp(eventtime).strftime('%c')
    if 'userName' in userDetails:
        USERNAME = userDetails['userName']
    elif 'principalId' in userDetails:
        USERNAME = userDetails['principalId']
    else:
        USERNAME = ' '
    print(type(USERNAME))
    print("----------------------------------------------------------------------------------")
    client = boto3.client('sns', region_name='us-west-2')
    response = client.publish(
    # TopicArn = "{}".format(os.environ['snsTopicArn']),
    TopicArn = "arn:aws:sns:us-west-2:288677030145:us-west-2-saas-alerts-sns-topic",
    Message = 'LOGS DETAILS IS:\n' +'EVENT_TIME: ' +EventTime +'\n\nUSER_DETAILS: ' +str(userDetails) +'\n\nEVENT_DETAILS: ' +str(eventDetails),
    # Subject = 'User: ' +USERNAME +' access the EC2 Instance through SessionManager'
    Subject= 'User: ' +USERNAME  +' access the SessionManager'
    )
    print('successfully send the notification on mail:\n' +str(userDetails) +'\n' +str(eventDetails))

lambda_handler()
