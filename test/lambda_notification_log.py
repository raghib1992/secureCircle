import json
import boto3

def lambda_handler(event, context):
    print('------------------')
    try:
        # 1. Iterate over each record
        for record in event['Records']:
            # 2. Handle event type
            if record['eventName'] == 'INSERT':
                handle_insert(record)
        print('-------------------------')
    except Exception as e:
        print(e)
        print('-------------------')
        return "Oops!!!"

def handle_insert(record):
    print('Handling INSERT events')

    #3a Get Image Content
    newImage = record['dynamodb']['NewImage']

    #3b parse the value
    newAccountId = newImage['Account_ID']['S']
    newUserId = newImage['userName']['S']
    time = newImage['EventTime']['S']
    #3c print it out
    
    client = boto3.client('sns')
    response = client.publish(
    TopicArn='arn:aws:sns:ap-south-1:079983867181:getConsoleLoginNotification',
    Message='Alert!!!!\nAccount ID Username  and time' + newAccountId + newUserId + time,
    Subject='Concole Login mail: ' + newUserId,
    )

    print('Succesful')
    print('New row added with the Access_Key= ' + newUserId)
    print('Done handling INSERT event')