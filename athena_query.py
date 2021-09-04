import time
import boto3
import logging
import os

dbName = 'saas_ses_email'
tableName = 'sesblog2'
sesEventType = 'Bounce'
output='s3://saas-ses-email-query-result/'
dynamodbtableName = 'ses-email-dynoTable'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getIamUserListFromAthena():
    client = boto3.client('athena')
    query = "SELECT mail.tags.ses_caller_identity as User FROM {} WHERE eventType = \'{}\'".format(tableName,sesEventType)
    queryResult = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': dbName
        },
        ResultConfiguration={
            'OutputLocation': output,
        }
    )
    queryId = queryResult['QueryExecutionId']
    time.sleep(5)
    getQueryResult = client.get_query_results(
        QueryExecutionId=queryId
    )
    iamUsers=[]
    print(getQueryResult)
    for row in getQueryResult['ResultSet']['Rows']:
        if row['Data'][0]['VarCharValue'] != 'User':
            sesUser = row['Data'][0]['VarCharValue']
            iamUsers.append(sesUser.split('"')[1])
            logging.info("List of IAM users: \"{}\"".format(iamUsers))
    print(iamUsers)
    return iamUsers

# def getIamUserAccessId(iamUserNames):
#     client = boto3.client('iam')
#     userAndAccessDetails = {}
#     for iamUser in iamUserNames:
#         userAccessIdList = []
#         paginator = client.get_paginator('list_access_keys')
#         for userJsonData in paginator.paginate(UserName=iamUser):
#             for akm in userJsonData['AccessKeyMetadata']:
#                 userAccessIdList.append(akm['AccessKeyId'])
#         logger.info("User \"{}\" access id list \"{}\"".format(iamUser, userAccessIdList))
#         userAndAccessDetails[iamUser] = userAccessIdList
#     return userAndAccessDetails


# def deactiveIamUser(iamUser, userAccessIds):
#     iam = boto3.resource('iam')
#     for userAccessId in userAccessIds:
#         access_key = iam.AccessKey(iamUser,userAccessId)
#         userDeactivationResult = access_key.deactivate()
#         logger.info("User \"{}\" access id \"{}\" has been disabled.".format(iamUser,userAccessId))

# def getUserAccessStatus(iamUserNames):
#     client = boto3.client('iam')
#     userAndAccessDetails = []
#     for iamUser in iamUserNames:
#         paginator = client.get_paginator('list_access_keys')
#         for userJsonData in paginator.paginate(UserName=iamUser):
#             for sts in userJsonData['AccessKeyMetadata']:
#                 res = {key: sts[key] for key in sts.keys() & {'UserName','AccessKeyId', 'Status'}}
#                 userAndAccessDetails.append(res)
#     return userAndAccessDetails

# def update_dynamoDB(userAndAccessDetails):    
#     dynamodb = boto3.resource('dynamodb')
#     expiryTimestamp = int(time.time()  + 60)
#     table = dynamodb.Table(dynamodbtableName)
#     with table.batch_writer(overwrite_by_pkeys=['IAM_User']) as batch:
#         for id in userAndAccessDetails:
#             userID = id['AccessKeyId']
#             userName = id['UserName']
#             status = id['Status']
#             batch.put_item(
#                 Item={
#                     'IAM_User': userName,
#                     'Access_Key': userID,
#                     'Status': status,
#                     'TTL' : expiryTimestamp
#                 }
#             )
#         logger.info("User \"{}\" access id \"{}\" updated in dynamodb".format(userName,userID))

# # lambda_handler()
# def lambda_handler(event, context):
#     userList = getIamUserListFromAthena()
#     usersAndKeys = getIamUserAccessId(userList)
#     for user,keys in usersAndKeys.items():
#         deactiveIamUser(user, keys)
#     usersAndStatus = getUserAccessStatus(userList)
#     dynamodb_update = update_dynamoDB(usersAndStatus)

getIamUserListFromAthena()