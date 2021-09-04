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
        print (IAMdetail)
    # regex = re.compile("ses-smtp.*")
    # IAMUserLists = list(filter(regex.match, userDetails))
    # IAMUserLists = [i for i in userDetails if not regex.match(i)]
    # print("List of all non-ses user is: " + str(IAMUserLists ))
    # inactiveUser = getUserLastActivity(IAMUserLists)
    return IAMUserLists

# def getUserLastActivity(userDetails):
#     client = boto3.client('iam')
#     UserLists = []
#     for userDetail in userDetails:
#         users = client.get_user(
#             UserName=userDetail
#         )
#         UserLists.append(users['User'])
#     inactiveUsers = []
#     for user in UserLists:
#         lastActive = {key: user[key] for key in user.keys() & {'UserName','PasswordLastUsed','AccessKey'}}
#         if 'PasswordLastUsed' not in lastActive.keys():
#             lastActive.update({'PasswordLastUsed' : now})
#         inactiveUsers.append(lastActive)
#     print(inactiveUsers)
#     print("------------------------")
#     disableUser = inactiveUser(inactiveUsers)
#     return inactiveUsers

# def inactiveUser(userLists):
#     print(now)
#     print("-------------------------")
#     InactiveUserLists = []
#     for userName in userLists:
#         if (now - userName['PasswordLastUsed']).days >= 0:
#             IAMUsers = userName['UserName']
#             InactiveUserLists.append(IAMUsers)
#     print(InactiveUserLists)
#     print("------------------------")
#     logging.info("List of user which had been deleted: " +str(InactiveUserLists))
#     deactivateProfile = deleteLoginProfile(InactiveUserLists)
#     deleteAccessKey = getAccessKey(InactiveUserLists)
#     deactivateUser = disableInactiveUser(InactiveUserLists)
#     sns_notification = notification(InactiveUserLists)

#     return InactiveUserLists

# def getAccessKey(IAMUserLists):
#     client = boto3.client('iam')
#     userAndAccessDetails = {}
#     for user in IAMUserLists:
#         userAccessIdList = []
#         response = client.list_access_keys(UserName=user)
#         for akm in response['AccessKeyMetadata']:
#             userAccessIdList.append(akm['AccessKeyId'])
#         userAndAccessDetails[user] = userAccessIdList
#     print(userAndAccessDetails)
#     print("---------------------------------------")
#     for key,value in userAndAccessDetails.items():
#         for id in value:
#             response = client.delete_access_key(
#                 UserName=key,
#                 AccessKeyId=id
#             )
#     logging.info("Successfully deleted the Access Key")
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
#             print ("No Login profile for this user")
#     logging.info("Successfully deleted the login profile")

# def disableInactiveUser(users):
#     client = boto3.client('iam')
#     for user in users:
#         response = client.delete_user(
#             UserName=user
#         )
#     logging.info("Successfully delete the user")

# def notification(IAMUserLists):
#     client = boto3.client('sns')
#     response = client.publish(
#     # TopicArn="{}".format(os.environ['snsTopicArn']),
#     TopicArn = "arn:aws:sns:ap-south-1:079983867181:ap-south-1-saas-alerts-sns-topic",
#     Message='Alert!!!!\nFollowing users is disable/delelted as it was inactive from last One year:\n' +str(IAMUserLists),
#     Subject='non-ses inactive IAM user deleted'
#     )


getIAMUserList()
