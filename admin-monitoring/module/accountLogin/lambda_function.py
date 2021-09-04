import json
import gzip
import base64
import boto3
import os
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

AWS_REGION = "{}".format(os.environ['REGION'])

def lambda_handler(event, context):
    print(event)
    cloudwatch_log = event["awslogs"]["data"]
    decode_base64 = base64.b64decode(cloudwatch_log)
    decompress_data = gzip.decompress(decode_base64)
    log_data = json.loads(decompress_data)
    logging.info("the event details is: " +str(log_data))
    send_notification = sns_notification(log_data)
    return (log_data)
    
def sns_notification(log_data):
    res = log_data["logEvents"][0]["message"]
    filter_log_data = json.loads(res)
    eventDetails = {key: filter_log_data[key] for key in filter_log_data.keys() & {'eventTime','sourceIPAddress', 'responseElements'}}
    extract = filter_log_data['userIdentity']
    userDetails = {key: extract[key] for key in extract.keys() & {'arn','accountId', 'userName', 'principalId'}}
    eventtime = log_data['logEvents'][0]['timestamp']/1000
    EVENT_TIME = datetime.datetime.fromtimestamp(eventtime).strftime('%c')
    if 'userName' in userDetails:
        USERNAME = userDetails['userName']
    elif 'principalId' in userDetails:
        USERNAME = userDetails['principalId']
    else:
        USERNAME = ''
    ARN = userDetails['arn']
    ACCOUNT_ID = userDetails['accountId']
    SOURCE_IP = eventDetails['sourceIPAddress']
    client = boto3.client('sns', region_name=AWS_REGION)
    response = client.publish(
    TopicArn="{}".format(os.environ['snsTopicArn']),
    Message = 'DETAILS LOG IS:\n\n' +'EVENT_TIME: ' +EVENT_TIME +'\nUSERNAME: ' +USERNAME +'\nARN: ' +ARN +'\nACCOUNT_ID: ' +ACCOUNT_ID +'\nSOURCE_IP: ' +SOURCE_IP,
    Subject= 'User: ' +USERNAME  +' had been login into SaaS account'
    )
    logging.info('SNS send successfully' +'\nUSER_DETAILS: ' + str(userDetails) +'EVENT_DETAILS: ' +str(eventDetails))
