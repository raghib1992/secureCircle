import json
import gzip
import base64
import boto3



def lambda_handler(event, context):
    # print(event)
    cloudwatch_log = event["awslogs"]["data"]
    decode_base64 = base64.b64decode(cloudwatch_log)
    decompress_data = gzip.decompress(decode_base64)
    log_data = json.loads(decompress_data)
    userdata = []
    filter_log_data = log_data["logEvents"][0]["message"]
    res = iamUsers.append(filter_log_data.split('"')[1::])
    UserData = userdata[0][14:29:2]
    send_notification = sns_notification(filter_log_data)
    print(UserData)
    return (UserData)
    
def sns_notification(UserData):
    client = boto3.client('sns')
    response = client.publish(
    TopicArn='arn:aws:sns:ap-south-1:079983867181:trialLogNotification',
    Message='details message is:\n' + UserData ,
    Subject='Alert...Someone had login into SaaS account'
    )
    print("successfully send the mail")