import json
import boto3
from datetime import datetime
from dateutil import tz
import re
import logging
import dryable
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
    # IAMUserLists = [i for i in userDetails if not regex.match(i)]
    IAMUserLists = list(filter(regex.match, userDetails))
    print("List of all non-ses user is: " + str(IAMUserLists ))
    return IAMUserLists

def getInactivityUsers(UserLists):
    client = boto3.client('iam')
    InactiveUsers = []
    for UserList in UserLists:
        users = client.get_user(
            UserName=UserList
        )    
        userDetails = users['User']
        filterusers = {key: userDetails[key] for key in userDetails.keys() & {'UserName','PasswordLastUsed','CreateDate'}}
        if 'PasswordLastUsed' not in filterusers.keys():
            if (now - filterusers['CreateDate']).days >=0:
                print('User: ' +str(UserList) +' had not been logged in since last one year')
                InactiveUsers.append(filterusers['UserName'])
        else:
            if (now - filterusers['PasswordLastUsed']).days >= 0:
                InactiveUsers.append(filterusers['UserName'])
    print('List of non-ses inactive users form last one year: ' +str(InactiveUsers))
    return InactiveUsers

def deleteAccessKey(InactiveUsers):
    client = boto3.client('iam')
    for user in InactiveUsers:
        activeIAMuserLists = []
        getAccessKey = client.list_access_keys(UserName=user)
        for akm in getAccessKey['AccessKeyMetadata']:
            accessKey = akm['AccessKeyId']
            accesskeyDetials = client.get_access_key_last_used(
                AccessKeyId=accessKey
            )
            if 'LastUsedDate' in accesskeyDetials['AccessKeyLastUsed']:
                accessKeyLastUsed = accesskeyDetials['AccessKeyLastUsed']['LastUsedDate']
                if (now - accesskeyDetials['AccessKeyLastUsed']['LastUsedDate']).days < 90:
                    activeIAMuserLists.append(user)
                else:
                    print('access key of the user: ' +str(user) +'not used since it was created')
                    response = client.delete_access_key(
                        UserName=user,
                        AccessKeyId=accessKey
                    )
            else:
                print('access key of the user: ' +str(user) +'not used since it was created')
                response = client.delete_access_key(
                    AccessKeyId=accessKey,
                    UserName=user
                )
    for element in activeIAMuserLists:
        if element in InactiveUsers:
            InactiveUsers.remove(element)
    print('inactiveIAMuserLists are : ' +str(InactiveUsers))
    return InactiveUsers

@dryable.Dryable()
def deleteIAMUser(users):
    if len(users):
        client = boto3.client('iam')
        iam = boto3.resource('iam')
        for user in users:
            login_profile = iam.LoginProfile(user)
            try:
                login_profile.create_date
                response = client.delete_login_profile(
                    UserName=user
                )
                print("Successfully deleted the login profile" +user)
            except:
                print("No Login profile for this user" +user)

            response = client.delete_user(UserName=user)
            print("Successfully delete the user: " +str(users))
    else:
        pass
     
@dryable.Dryable()
def notification(IAMUserLists):
    if len(IAMUserLists):
        client = boto3.client('sns')
        sendNotification = client.publish(
            # TopicArn="{}".format(os.environ['snsTopicArn']),
            TopicArn = 'arn:aws:sns:ap-south-1:288677030145:raghib-sns-test',
            Message='Alert!!!!\nFollowing users is disable/delelted as it was inactive from last One year:\n' +str(IAMUserLists),
            Subject='non-ses inactive IAM user deleted'
        )
        print("Successfully delete the user which was inactive from last one year")
    else:
        pass

def lambda_handler():
# def lambda_handler(event, context):
    userslist= getIAMUserList()
    InactiveUser = getInactivityUsers(userslist)
    deactivateAccessKey = deleteAccessKey(InactiveUser)
    dryable.set(False) # when dry is False, it will allow to run the function
    deleteUser = deleteIAMUser(deactivateAccessKey)
    dryable.set(False)
    sns_notification = notification(deactivateAccessKey)


lambda_handler()