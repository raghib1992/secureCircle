import boto3

# sns_notification()
def lambda_handler(event,context):
    client = boto3.client('sns')
    response = client.publish(
    TopicArn='arn:aws:sns:ap-south-1:079983867181:trialLogNotification',
    Message='Some had tried to login into saas account',
    Subject='Some had tried to login into saas account'
    )