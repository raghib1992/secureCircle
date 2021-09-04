import json
import boto3
from datetime import datetime
from dateutil import tz
import re
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

now = datetime.now(tz=tz.tzlocal())

def getIAMUserList():
    client = boto3.client('iam')
    IAMdetails = client.list_users()
    userDetails = []
    for IAMdetail in IAMdetails['Users']:
        username = IAMdetail['UserName']
        userDetails.append(username)
    regex = re.compile("ses-smtp*")
    IAMUserLists = [i for i in userDetails if not regex.match(i)]
    # logging.info("List of all non-ses user is:\n" + str(IAMUserLists ))
    return IAMUserLists

def getUserLastActivity(userDetails):
    client = boto3.client('iam')
    UserLists = []
    for userDetail in userDetails:
        users = client.get_user(
            UserName=userDetail
        )
        print(users)
        UserLists.append(users['User'])
    usersLastActivity = []
    for user in UserLists:
        lastActive = {key: user[key] for key in user.keys() & {'UserName','PasswordLastUsed'}}
        if 'PasswordLastUsed' not in lastActive.keys():
            lastActive.update({'PasswordLastUsed' : now})
        usersLastActivity.append(lastActive)
    # print("user last activity" +str(usersLastActivity))
    return usersLastActivity

# def getinactiveUserLists(usersLastActivity):
#     InactiveUserLists = []
#     for userName in usersLastActivity:
#         x = (now - userName['PasswordLastUsed']).days
#         print(x)
#         if x >= 100:
#         # if (now - userName['PasswordLastUsed']).days >= 100:
#             IAMUsers = userName['UserName']
#             InactiveUserLists.append(IAMUsers)
#     # logging.info("List of user which is inactive from last one year:\n" +str(InactiveUserLists))
#     return InactiveUserLists

# def deleteAccessKey(IAMUserLists):
#     client = boto3.client('iam')
#     userAndAccessDetails = {}
#     for user in IAMUserLists:
#         userAccessIdList = []
#         response = client.list_access_keys(UserName=user)
#         for akm in response['AccessKeyMetadata']:
#             userAccessIdList.append(akm['AccessKeyId'])
#         userAndAccessDetails[user] = userAccessIdList
#     for key,value in userAndAccessDetails.items():
#         for id in value:
#             response = client.delete_access_key(
#                 UserName=key,
#                 AccessKeyId=id
#             )
#     logging.info("Successfully deleted the following Access Key:\n" +str(AccessKeyId))
#     return userAndAccessDetails

# def deleteLoginProfile(users):
#     iam = boto3.resource('iam')
#     for user in users:
#         login_profile = iam.LoginProfile(user)
#         try:
#             login_profile.create_date
#             client = boto3.client('iam')
#             response = client.delete_login_profile(
#                 UserName=user
#             )
#         except:
#             logging.info("No Login profile for this user")
#     logging.info("Successfully deleted the login profile of following user:\n" +str(users))

# def disableInactiveUser(users):
#     client = boto3.client('iam')
#     for user in users:
#         response = client.delete_user(
#             UserName=user
#         )
#     logging.info("Successfully delete the following user:\n" str(users))

# def notification(IAMUserLists):
#     client = boto3.client('sns')
#     response = client.publish(
#     TopicArn="{}".format(os.environ['snsTopicArn']),
#     Message='Alert!!!!\nFollowing users is disable/delelted as it was inactive from last One year:\n' +str(IAMUserLists),
#     Subject='non-ses inactive IAM user deleted'
#     )
#     logging.info("Successfully delete the user which was inactive from last one year")

# def lambda_handler(event, context):
def lambda_handler():
    userslist= getIAMUserList()
    usersactivity = getUserLastActivity(userslist)
    disableUser = getinactiveUserLists(usersactivity)
    # deactivateProfile = deleteLoginProfile(disableUser)
    # deleteKey = deleteAccessKey(disableUser)
    # deactivateUser = disableInactiveUser(disableUser)
    # sns_notification = notification(disableUser)

lambda_handler()

# {'User': {'Path': '/', 'UserName': 'admin', 'UserId': 'AIDAYH7GG6GJIVKAWUXAH', 'Arn': 'arn:aws:iam::566881612178:user/admin', 'CreateDate': datetime.datetime(2021, 8, 10, 11, 44, 35, tzinfo=tzutc()), 'PasswordLastUsed': datetime.datetime(2021, 8, 11, 14, 44, 41, tzinfo=tzutc())}, 'ResponseMetadata': {'RequestId': '2edb166e-10b8-412c-803a-8d26ee21c387', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '2edb166e-10b8-412c-803a-8d26ee21c387', 'content-type': 'text/xml', 'content-length': '523', 'date': 'Wed, 11 Aug 2021 15:04:23 GMT'}, 'RetryAttempts': 0}}
# {'User': {'Path': '/', 'UserName': 'eksAdmin', 'UserId': 'AIDAYH7GG6GJL3HPAYZAC', 'Arn': 'arn:aws:iam::566881612178:user/eksAdmin', 'CreateDate': datetime.datetime(2021, 3, 19, 16, 15, 19, tzinfo=tzutc())}, 'ResponseMetadata': {'RequestId': '36b01753-4255-4bfe-8ec9-4d397a64c126', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '36b01753-4255-4bfe-8ec9-4d397a64c126', 'content-type': 'text/xml', 'content-length': '465', 'date': 'Wed, 11 Aug 2021 15:04:23 GMT'}, 'RetryAttempts': 0}}
# {'User': {'Path': '/', 'UserName': 'eksViewer', 'UserId': 'AIDAYH7GG6GJNOC64GAP6', 'Arn': 'arn:aws:iam::566881612178:user/eksViewer', 'CreateDate': datetime.datetime(2021, 3, 19, 19, 50, 30, tzinfo=tzutc())}, 'ResponseMetadata': {'RequestId': '5942eb95-9c15-47f7-b626-42067bade725', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '5942eb95-9c15-47f7-b626-42067bade725', 'content-type': 'text/xml', 'content-length': '467', 'date': 'Wed, 11 Aug 2021 15:04:24 GMT'}, 'RetryAttempts': 0}}
# {'User': {'Path': '/', 'UserName': 'F_shaheen', 'UserId': 'AIDAYH7GG6GJDT3IGF4K6', 'Arn': 'arn:aws:iam::566881612178:user/F_shaheen', 'CreateDate': datetime.datetime(2021, 2, 6, 12, 53, 26, tzinfo=tzutc()), 'Tags': [{'Key': 'env', 'Value': 'test'}, {'Key': 'team', 'Value': 'developers'}]}, 'ResponseMetadata': {'RequestId': '04c27345-28d1-41cf-b71c-4749b0d69550', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '04c27345-28d1-41cf-b71c-4749b0d69550', 'content-type': 'text/xml', 'content-length': '681', 'date': 'Wed, 11 Aug 2021 15:04:24 GMT'}, 'RetryAttempts': 0}}
# {'User': {'Path': '/', 'UserName': 'lion', 'UserId': 'AIDAYH7GG6GJPWHZ43263', 'Arn': 'arn:aws:iam::566881612178:user/lion', 'CreateDate': datetime.datetime(2021, 8, 11, 14, 47, 27, tzinfo=tzutc())}, 'ResponseMetadata': {'RequestId': '0da4fc68-1f25-4bb1-a186-8fee28472400', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '0da4fc68-1f25-4bb1-a186-8fee28472400', 'content-type': 'text/xml', 'content-length': '457', 'date': 'Wed, 11 Aug 2021 15:04:24 GMT'}, 'RetryAttempts': 0}}
# {'User': {'Path': '/', 'UserName': 'nadim', 'UserId': 'AIDAYH7GG6GJLFFG6ZROF', 'Arn': 'arn:aws:iam::566881612178:user/nadim', 'CreateDate': datetime.datetime(2021, 3, 28, 19, 42, 41, tzinfo=tzutc())}, 'ResponseMetadata': {'RequestId': 'abbfdc5e-4222-44b1-ac85-476b0a49e6c2', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'abbfdc5e-4222-44b1-ac85-476b0a49e6c2', 'content-type': 'text/xml', 'content-length': '459', 'date': 'Wed, 11 Aug 2021 15:04:24 GMT'}, 'RetryAttempts': 0}}
# {'User': {'Path': '/', 'UserName': 'prod-viewer', 'UserId': 'AIDAYH7GG6GJL2UYG5K5W', 'Arn': 'arn:aws:iam::566881612178:user/prod-viewer', 'CreateDate': datetime.datetime(2021, 3, 19, 19, 59, 10, tzinfo=tzutc())}, 'ResponseMetadata': {'RequestId': '3bc1e1e8-1fbf-4a00-92b5-4f96337d317b', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '3bc1e1e8-1fbf-4a00-92b5-4f96337d317b', 'content-type': 'text/xml', 'content-length': '471', 'date': 'Wed, 11 Aug 2021 15:04:25 GMT'}, 'RetryAttempts': 0}}
# {'User': {'Path': '/', 'UserName': 'royal', 'UserId': 'AIDAYH7GG6GJFYB6AAGTR', 'Arn': 'arn:aws:iam::566881612178:user/royal', 'CreateDate': datetime.datetime(2021, 8, 11, 14, 37, 20, tzinfo=tzutc())}, 'ResponseMetadata': {'RequestId': '06d8ec32-bab5-417a-adf9-7ec09a83006c', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '06d8ec32-bab5-417a-adf9-7ec09a83006c', 'content-type': 'text/xml', 'content-length': '459', 'date': 'Wed, 11 Aug 2021 15:04:25 GMT'}, 'RetryAttempts': 0}}
# {'User': {'Path': '/', 'UserName': 'tiger', 'UserId': 'AIDAYH7GG6GJMPTKAPQJW', 'Arn': 'arn:aws:iam::566881612178:user/tiger', 'CreateDate': datetime.datetime(2021, 8, 11, 14, 43, 26, tzinfo=tzutc()), 'PasswordLastUsed': datetime.datetime(2021, 8, 11, 14, 43, 55, tzinfo=tzutc())}, 'ResponseMetadata': {'RequestId': 'bff3fea5-a7e5-47cd-9bf8-cc0646fea99f', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'bff3fea5-a7e5-47cd-9bf8-cc0646fea99f', 'content-type': 'text/xml', 'content-length': '523', 'date': 'Wed, 11 Aug 2021 15:04:25 GMT'}, 'RetryAttempts': 0}}