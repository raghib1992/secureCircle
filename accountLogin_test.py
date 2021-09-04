import json
import gzip
import base64
import boto3
import os
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# def lambda_handler(event, context):
def lambda_handler():
    # cloudwatch_log = event["awslogs"]["data"]
    cloudwatch_log = 'H4sIAAAAAAAAAJVUa2/bNhT9K4Y+NVgoi6IsS+qXCbaTGG2dIPLSYUsR0BIlE9OrJBU1C/zfdyn6kSVd0X2xIfLw3HPPfTxbFZOSFmz91DIrsubxOn74tEiS+HJhnVtNXzMBx24Q+NOpQxzsTeC4bIpL0XQt3MhUUipRWjZdpgTlJeok6plUyDXARAlGq1ccDzONX2v8w0u87DYyFbxVvKkveKmYkFb0p6YpeF08zJpaNiX72MCX9WWgXzyyWmnQs8UziEJ8QlyMvTD0pn4YuphMfCckExI4ToAxmRISYNfzfDfwQ9+ZOIHnkCnWWSkOXihaQVrYd0McBCRwCcHnB4+A/vneYjriHSgDjfdWdG9h2wnurfN7q5NMLDO45eoJbgCrwNUBE0vZVSy7BfUDtBW8TnlLy2Vm7m+v498uV+vJZBF/vvvgztbx3edI0GLLN3ZNM179KlnaCZZykZbMTptq4KHCaID/iPYykkpG0UunI2oiIwGhxzSreC1RLpoKFbLjio1/IkaaNl2t9kpfkh+uwZ4P7OmQSrI8pTK7Xv0+v1gNQAkw8AyKqNg3ZQzany1BJBOvPPt/Zn3XDk6rV3b8hw0/k6gu74pWRtz3KHYA6tlmmV2wjAmqm3hOFdVp6SuqlOCbTjFpEk1hMPYYw+k6LkZOgPB07Uwjz40c8scQucpp3Kmt7qwUwEZfTkupg+4099CUa169JQoiPI1cbIgGWNJ0IjVAGCBp04r+3dRg17HiA+yY6pzpmdyw5O1wGtt6ecuKwzQcx9nUfIi1vImzTECp9+qIjYPQdr3QJqfJiQsIaup7sxrDUI2uqNzyWSPa4WvNhKB5I6qxY2PPDkfvftkq1cpoPO773laHa5s3Z6PjF2pF88ihHAhkjont+UB1eilAuFTi6V/Px4c3crzVElItAZ6fjeAHyewvVDQgiQS2j0fvigbb2H8/6nmdNb18P6JV5ntnQ16Cfe3AjBsqwExjmK78YX8eLf7BFh148sFuDb8RLOffDsV7sxVNE4LVLRyyRckqvR4BXndleRK0nJvNleYeSTcUEd8LkOfhENFNliIPbxje5GnOJvmpIfaPfMKclFCGMMkY8oJNiIIcT5Dn5yQkue84eb5PnmbXdalXoRIdO3bpcSf2Mm75jJalaaOWv9yqLsydQ1zTHxWtYf/qXIZ9f2LUy6rlcBT/eHaHyDOYnaIRTwPk05FyAKhSzpkC5/clgu+XatYfk0dsm2JAxC0TiZl5uFvM5lcLdJvEKF4k2A1QchUbYKmV3Zhmyq4aqa7AkmHP7UfvWOXXQ7jbWbsvu38AdpCQMZ4HAAA='
    # cloudwatch_log = 'H4sIAAAAAAAAAI1T227bOBD9FUFPLWBdqIslqi8rOK7XSJMGkZoAXRcBLdIKUUrUklTdNMi/7+gSr5uHxT4Jmjkzc3jmzLPdMK1JzcqnjtmZfZGX+cPVuijyzdpe2PLYMgXhIE2XSeKHPopiCAtZb5TsO8joShOinUrInhpFuHB67RyZNk4wAQujGGne9HhYDfhywD+c43W/15XineGy/ciFYUrb2V9Dm5q39cNKtloK9knCn/1tbL/+wVozgJ5tTmFKuAzDAC0RTnwU+n4UhsiPgyTGcYKXEczGCcZxGiVpmmKcxAh+MMRhuOGghSENPAstA4ywH6VpkuDFq0bQ/nlns2HiHTADjjs729nI9dOdvdjZvWZqSyHLzRNkAGtA1RGTa903jN4C+xHaKd5WvCNiS6f87ef8y+a6jON1fn93GazK/O4+U6R+5Hu3JZQ3f2hW9YpVXFWCuZVsxj5ETRzgm5GjzrTRWXaudEamyY6C0R6hDW+1c1CycWrdc8O8/zGjqmTfmpnpefOd/bKYBSlBvCnvB8jxUwclpZ9mEcqC5OvYZoQVslfVBNS8bnnrkob8ki1wP80bgddk7ne+84nOUd+y+lV8cA8j4B405vTYfnuTU6pgZzOh0EUpdoMIu+G/i8prmDICruQvLgTxYte33t3zlsqjtq5LC/mu/8GCwDL6YP1cRu+tvOsEu2f7S268OEzccGm9u/yzvPq0sAT/zqwNq77L99bqEfRlHg5c341iFLsoxlZBDkTxuWxkodjfPRjuhih462B1YNP2Qowp3cG72VqwZvD35KbfpQDmRV9V4zOHNRBK+XA3RIw3cUEMmcpGfCnHikdjOp15XjW1cgfdpw0M8r+GvUfZTD69knsu2Lnbr+WU+Jh/0YyehwrSiBslf3AK6r7xJSfNG19qQDvdDPc2xWDGMz9tL8b6QxDuQ4KJQ2kaOVHgHxxMUOxUZH+oUkaXGKFZTEI/t2K4uwMRmp18ebrAo571K8B428lLDWnhrgeJR80AaFR/ql0Rw2qpniaXnKDzPDhfDn/5f12H/fLt5R8Jk82bYwUAAA=='
    decode_base64 = base64.b64decode(cloudwatch_log)
    decompress_data = gzip.decompress(decode_base64)
    log_data = json.loads(decompress_data)
    print("the log_data details is: " +str(log_data))
    print('--------------------------------------------------------------------')
    send_notification = sns_notification(log_data)
    return (log_data)
    
def sns_notification(log_data):
    res = log_data["logEvents"][0]["message"]
    filter_log_data = json.loads(res)
    eventDetails = {key: filter_log_data[key] for key in filter_log_data.keys() & {'eventTime','sourceIPAddress', 'responseElements'}}
    print("Event details are: " +str(eventDetails))
    print("-------------------------------------------------------------------")
    extract = filter_log_data['userIdentity']
    userDetails = {key: extract[key] for key in extract.keys() & {'arn','accountId', 'userName', 'principalId'}}
    print("User details are: " +str(userDetails))
    print("-------------------------------------------------------------------")
    eventtime = log_data['logEvents'][0]['timestamp']/1000
    EVENT_TIME = datetime.datetime.fromtimestamp(eventtime).strftime('%c')
    if 'userName' in userDetails:
        USERNAME = userDetails['userName']
    elif 'principalId' in userDetails:
        USERNAME = userDetails['principalId']
    else:
        USERNAME = ''
    print(type(USERNAME))
    print("------------------------------------------------------------")
    ARN = userDetails['arn']
    ACCOUNT_ID = userDetails['accountId']
    SOURCE_IP = eventDetails['sourceIPAddress']
    client = boto3.client('sns', region_name = 'us-west-2')
    response = client.publish(
    # TopicArn="{}".format(os.environ['snsTopicArn']),
    TopicArn = "arn:aws:sns:us-west-2:288677030145:us-west-2-saas-alerts-sns-topic",
    Message = 'DETAILS LOG IS:\n\n' +'EVENT_TIME: ' +EVENT_TIME +'\nUSERNAME: ' +USERNAME +'\nARN: ' +ARN +'\nACCOUNT_ID: ' +ACCOUNT_ID +'\nSOURCE_IP: ' +SOURCE_IP,
    Subject= 'User: ' +USERNAME  +' had been login into SaaS account'
    )
    print('SNS send successfully' +'\nUSER_DETAILS: ' + str(userDetails) +'\nEVENT_DETAILS: ' +str(eventDetails))


lambda_handler()