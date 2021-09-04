import json
import boto3
from datetime import datetime
from dateutil import tz
import re
import logging
import os

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

now = datetime.now(tz=tz.tzlocal())

def getIAMUserList():
    client = boto3.client('iam')
    IAMdetails = client.list_users()
    for key in IAMdetails['Users']:
        # flaggedUser = {}
        username = key['UserName']
        print(username)
#     userDetails = []
#     for IAMdetail in IAMdetails['Users']:
#         username = IAMdetail['UserName']
#         userDetails.append(username)
#     regex = re.compile("ses-smtp*")
#     IAMUserLists = [i for i in userDetails if not regex.match(i)]
#     # logging.info("List of all non-ses user is:\n" + str(IAMUserLists ))
#     return IAMUserLists

# def getUserLastActivity(userDetails):
#     client = boto3.client('iam')
#     UserLists = []
#     for userDetail in userDetails:
#         users = client.get_user(
#             UserName=userDetail
#         )
#         print(users)
#         UserLists.append(users['User'])
#     usersLastActivity = []
#     for user in UserLists:
#         lastActive = {key: user[key] for key in user.keys() & {'UserName','PasswordLastUsed'}}
#         if 'PasswordLastUsed' not in lastActive.keys():
#             lastActive.update({'PasswordLastUsed' : now})
#         usersLastActivity.append(lastActive)
#     # print("user last activity" +str(usersLastActivity))
#     return usersLastActivity

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
#     usersactivity = getUserLastActivity(userslist)
#     disableUser = getinactiveUserLists(usersactivity)
    # deactivateProfile = deleteLoginProfile(disableUser)
    # deleteKey = deleteAccessKey(disableUser)
    # deactivateUser = disableInactiveUser(disableUser)
    # sns_notification = notification(disableUser)

lambda_handler()
