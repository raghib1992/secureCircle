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
            # elif record['eventName'] == 'MODIFY':
            #     handle_modify(record)
            # elif record['eventName'] == 'REMOVE':
            #     handle_remove(record)
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

# def handle_modify(record):
#     print('Handling INSERT events')

#     #3a Parse old image and score
#     oldImage = record['dynamodb']['OldImage']
#     oldScore = oldImage['Status']['N']

#     #3b parse the value
#     newImage = record['dynamodb']['NewImage']
#     newScore = newImage['Status']['N']

#     #3c check for change
#     if oldScore != newScore:
#         print('Scores changed' + str(oldScore) + ', newScore=' + str(newScore))
    
#     print('Done handling MODIFY event')

# def handle_remove(record):
#     print('Handling REMOVE events')

#     #3a Get Old Image
#     oldImage = record['dynamodb']['OldImage']

#     #3b parse Old Image Value
#     oldAccessId = oldImage['Access_Key']['S']
#     oldUserID = oldImage['IAM_User']['S']
    

#     #3c print it out
    
#     print('row removed with Access_Key= ' + oldAccessId)
#     print('row removed with Access_Key= ' + oldUserID)
#     print('Done handling REMOVE event')