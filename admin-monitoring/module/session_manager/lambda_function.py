import json
import gzip
import base64
import boto3
import os
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

AWS_REGION = "{}".format(os.environ['REGION'])

def lambda_handler(event, context):
    print(event)
    cloudwatch_log = event['awslogs']['data']
    decode_base64 = base64.b64decode(cloudwatch_log)
    decompress_data = gzip.decompress(decode_base64)
    log_data = json.loads(decompress_data)
    logging.info('successfully get the session manager logs:' +str(log_data))
    sns_noti = sns_notification(log_data)
    return log_data

def sns_notification(log_data):
    res = log_data["logEvents"][0]["message"]
    filter_log_data = json.loads(res)
    eventDetails = {key: filter_log_data[key] for key in filter_log_data.keys() & {'eventSource','eventName','sourceIPAddress','awsRegion'}}
    extract = filter_log_data['userIdentity']
    userDetails = {key: extract[key] for key in extract.keys() & {'arn','accountId','principalId', 'userName'}}
    eventtime = log_data['logEvents'][0]['timestamp']/1000
    EventTime = datetime.datetime.fromtimestamp(eventtime).strftime('%c')
    if 'userName' in userDetails:
        USERNAME = userDetails['userName']
    elif 'principalId' in userDetails:
        USERNAME = userDetails['principalId']
    else:
        USERNAME = ' '
    client = boto3.client('sns', region_name=AWS_REGION)
    response = client.publish(
    TopicArn = "{}".format(os.environ['snsTopicArn']),
    Message = 'LOGS DETAILS IS:\n' +'EVENT_TIME: ' +EventTime +'\n\nUSER_DETAILS: ' +str(userDetails) +'\n\nEVENT_DETAILS: ' +str(eventDetails),
    Subject= 'User: ' +USERNAME  +' access the SessionManager'
    )
    logging.info('successfully send the notification on mail:\n' +'UserDeatails are: '+str(userDetails) +'\nEventDetails are: ' +str(eventDetails))