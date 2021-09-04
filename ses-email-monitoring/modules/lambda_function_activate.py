import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print('------------------')
    try:
        # 1. Iterate over each record
        for record in event['Records']:
            # 2. Handle event type
            if record['eventName'] == 'INSERT':
                handle_insert(record)
            elif record['eventName'] == 'MODIFY':
                handle_modify(record)
            elif record['eventName'] == 'REMOVE':
                handle_remove(record)
        logging.info('-------------------------')
    except Exception as e:
        logging.info(e)
        logging.info('-------------------')
        return "Oops!!!"

def handle_insert(record):
    logging.info('Handling INSERT events')

    #3a Get Image Content
    newImage = record['dynamodb']['NewImage']

    #3b parse the value
    newAccessId = newImage['Access_Key']['S']
    newUserId = newImage['IAM_User']['S']
    
    #3c print it out
    client = boto3.client('sns')
    response = client.publish(
    TopicArn="{}".format(os.environ['snsTopicArn']),
    Message='Alert!!!!\nUser has been Deactivated as BOUNCE mail was sent by following user:\n' + newUserId,
    Subject='Bounce mail is send by ' + newUserId,
    )

    logging.info('Succesful')
    logging.info('New row added with the Access_Key= ' + newUserId)
    logging.info('Done handling INSERT event')
    logging.info("successful send the email and deactivate the user")

def handle_modify(record):
    logging.info('Handling INSERT events')

    #3a Parse old image and score
    oldImage = record['dynamodb']['OldImage']
    oldScore = oldImage['Status']['N']

    #3b parse the value
    newImage = record['dynamodb']['NewImage']
    newScore = newImage['Status']['N']

    #3c check for change
    if oldScore != newScore:
        logging.info('Scores changed' + str(oldScore) + ', newScore=' + str(newScore))
    
    logging.info('Done handling MODIFY event')

def handle_remove(record):
    logging.info('Handling REMOVE events')

    #3a Get Old Image
    oldImage = record['dynamodb']['OldImage']

    #3b parse Old Image Value
    oldAccessId = oldImage['Access_Key']['S']
    oldUserID = oldImage['IAM_User']['S']
    

    #3c print it out
    iam = boto3.resource('iam')
    access_key = iam.AccessKey(oldUserID,oldAccessId)
    response = access_key.activate()
    
    client = boto3.client('sns')
    response = client.publish(
    TopicArn="{}".format(os.environ['snsTopicArn']),
    Message='Alert!!!!\nThe User has been Activated' + oldUserID,
    Subject='User Has Been Activated ' + oldUserID,
    )
    logging.info('row removed with User Name= ' + oldUserID)
    logging.info('row removed with User Name= ' + oldUserID)
    logging.info('Done handling REMOVE event')
    logging.info('successfully sent the mail and activate the user')