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
    cloudwatch_log = 'H4sIAAAAAAAAAH1UbY+bOBD+Kwhpq1ZKiG3AEKrVHbdJtrlutnsN7d5LqsiAQ6wCzmG43Ha1/71jQ7J796EfEPbMM+/P+NGuuFKs4MnDgduRPYuTeLuar9fx9dwe2fJY8wbEKJhOQzekAQ4xiEtZXDeyO4CmbZgot5mslSz5jSy2OWtZD1m3DWfV/6y3V6Xs8sRYscNYya7dj7VP1aUqa8ShFbJeiLLljbKjv7SfQtTF9uocQdT2F+N//g+vWw16tEUOYVxKqEcDEiLqBi7yXM/3vHDqeXiKXRp6IA0JCnzfdakHHyKE+hhRCN4KaEPLKqgIgxdMPRwghNHo1B5w/7ixuY74GTKDHDd2tLGxg8KNPdrYneLNMgetaB9AA9gWGmowy3j1CbQGdmhEnYkDK5e50cXLWfxx8c5d0k/3v98tbv5IfiW/GSRr+gjwj9hRRYJVUfSykZEOOWlYsRepU7NcVD/vZCm6ysl0h3snWSa7uh2CvbQ+J33Lqj7NH3h6Gg2lJ2IAE0TwGAVj7CYojNA0csmfxqWBrWXXZD1QiaIWtcMq9k3WUIeTyeoZeA7+crp95kf1kRenNj8TxSiV8b+8i/O8gfGcMnJw4DqYeA7Bwbm+uIA4BrGS30RZsonvIOv1vahzeVTWbWJh5KC3Fgio99b6l3pvrPhwKPk9T9+LduK7geNS6/X7d8nqZmSV4iu3rnn2Vb6xrvaNrPhkCiRwPC8gOra1ZjvWiMHMZNHwvzsg1x1roFpNa8im7srSqNQBKufzkleayz1z/tsMyHzdZZmpUw+C5bnQO8JKw/8ZrFtvZvCJNBb7tj2oaDJ5bpwzrKijh9CPQ89iYkZ8ZG22n+yhmp8a0/XLZ8NXsBctv9wztY+bQl0QF1ZPfSYXbgyHcaHfAZAuzhc4XxCP+GQBoYZTyao0Zydxz0qT71bxOt/WshU7kTFd1+DK8EP71VQbDFEwHDAZDubn/9LfvJs4ma+TXjaD9cUUpXhKSO5lOU7DYIpSmrIwB5fMfSUUgwIzmfPLtum4mdVKpqLkLzf8VvaKRQxLnJ9F55VYzozMTVNCEc7HO0bp2HN9NmbId8cEYR/RFKHpDg9sYPmHutSPxI6Vip9X6/RcxEc1EGANu7Ps16FiNTxCmiNm6ADUKZ9sr2BAhWweepqfoUM8eG8E3OIfvAVP9tOXp+/+pK/hCwYAAA=='
    decode_base64 = base64.b64decode(cloudwatch_log)
    decompress_data = gzip.decompress(decode_base64)
    log_data = json.loads(decompress_data)
    print(log_data)
    # logging.info("the event details is: " +str(log_data))
    send_notification = sns_notification(log_data)
    return (log_data)
    
# def sns_notification(log_data):
#     res = log_data["logEvents"][0]["message"]
#     filter_log_data = json.loads(res)
#     eventDetails = {key: filter_log_data[key] for key in filter_log_data.keys() & {'eventTime','sourceIPAddress', 'responseElements'}}
#     extract = filter_log_data['userIdentity']
#     userDetails = {key: extract[key] for key in extract.keys() & {'arn','accountId', 'userName'}}
#     eventtime = log_data['logEvents'][0]['timestamp']/1000
#     EVENT_TIME = datetime.datetime.fromtimestamp(eventtime).strftime('%c')
#     print(EVENT_TIME)
#     USERNAME = userDetails['userName']
#     ARN = userDetails['arn']
#     ACCOUNT_ID = userDetails['accountId']
#     SOURCE_IP = eventDetails['sourceIPAddress']
#     CONSOLE_LOGIN = eventDetails['responseElements']['ConsoleLogin']
#     client = boto3.client('sns')
#     response = client.publish(
#     # # TopicArn="{}".format(os.environ['snsTopicArn']),
#     TopicArn = 'arn:aws:sns:ap-south-1:079983867181:admin_test',
#     Message = 'DETAILS LOG IS:\n\n' +'EVENT_TIME: ' +EVENT_TIME +'\nUSERNAME: ' +USERNAME +'\nARN: ' +ARN +'\nACCOUNT_ID: ' +ACCOUNT_ID +'\nSOURCE_IP: ' +SOURCE_IP +'\nCONSOLE_LOGIN: ' +CONSOLE_LOGIN,
#     Subject= 'User: ' +USERNAME  +' had been login into SaaS account'
#     )
    # logging.info('SNS send successfully' +'\nUSER_DETAILS: ' + str(userDetails) +'EVENT_DETAILS: ' +str(eventDetails))

lambda_handler()


# log_data:
# {'messageType': 'DATA_MESSAGE', 'owner': '079983867181', 'logGroup': 'trail_consoleLog_data', 'logStream': '079983867181_CloudTrail_ap-south-1', 'subscriptionFilters': ['logging_ConsoleLogin'], 'logEvents': [{'id': '36264672806373043454489441913684637820755336433602265106', 'timestamp': 1626164170010, 'message': '{"eventVersion":"1.08","userIdentity":{"type":"IAMUser","principalId":"AIDARFH3I6UWXPFLYTJ2Q","arn":"arn:aws:iam::079983867181:user/raghib.nadim@folium.cloud","accountId":"079983867181","userName":"raghib.nadim@folium.cloud"},"eventTime":"2021-07-13T08:09:32Z","eventSource":"signin.amazonaws.com","eventName":"ConsoleLogin","awsRegion":"ap-south-1","sourceIPAddress":"202.173.124.217","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36","requestParameters":null,"responseElements":{"ConsoleLogin":"Success"},"additionalEventData":{"LoginTo":"https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1&state=hashArgs%23logsV2%3Alog-groups%2Flog-group%2F%24252Faws%24252Flambda%24252FaccountLogin_send_notification%2Flog-events%2F2021%24252F07%24252F12%24252F%24255B%242524LATEST%24255D001160b1922d4cd1b8790b6ba8d202a3&isauthcode=true","MobileVersion":"No","MFAUsed":"No"},"eventID":"3bb2601d-fa66-435a-a053-201506b009f1","readOnly":false,"eventType":"AwsConsoleSignIn","managementEvent":true,"eventCategory":"Management","recipientAccountId":"079983867181"}'}]}

# filter_log_data:
# {"eventVersion":"1.08","userIdentity":{"type":"IAMUser","principalId":"AIDARFH3I6UWXPFLYTJ2Q","arn":"arn:aws:iam::079983867181:user/raghib.nadim@folium.cloud","accountId":"079983867181","userName":"raghib.nadim@folium.cloud"},"eventTime":"2021-07-13T08:09:32Z","eventSource":"signin.amazonaws.com","eventName":"ConsoleLogin","awsRegion":"ap-south-1","sourceIPAddress":"202.173.124.217","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36","requestParameters":null,"responseElements":{"ConsoleLogin":"Success"},"additionalEventData":{"LoginTo":"https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1&state=hashArgs%23logsV2%3Alog-groups%2Flog-group%2F%24252Faws%24252Flambda%24252FaccountLogin_send_notification%2Flog-events%2F2021%24252F07%24252F12%24252F%24255B%242524LATEST%24255D001160b1922d4cd1b8790b6ba8d202a3&isauthcode=true","MobileVersion":"No","MFAUsed":"No"},"eventID":"3bb2601d-fa66-435a-a053-201506b009f1","readOnly":false,"eventType":"AwsConsoleSignIn","managementEvent":true,"eventCategory":"Management","recipientAccountId":"079983867181"}

# res:
# {'eventVersion': '1.08', 'userIdentity': {'type': 'IAMUser', 'principalId': 'AIDARFH3I6UWXPFLYTJ2Q', 'arn': 'arn:aws:iam::079983867181:user/raghib.nadim@folium.cloud', 'accountId': '079983867181', 'userName': 'raghib.nadim@folium.cloud'}, 'eventTime': '2021-07-13T08:09:32Z', 'eventSource': 'signin.amazonaws.com', 'eventName': 'ConsoleLogin', 'awsRegion': 'ap-south-1', 'sourceIPAddress': '202.173.124.217', 'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'requestParameters': None, 'responseElements': {'ConsoleLogin': 'Success'}, 'additionalEventData': {'LoginTo': 'https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1&state=hashArgs%23logsV2%3Alog-groups%2Flog-group%2F%24252Faws%24252Flambda%24252FaccountLogin_send_notification%2Flog-events%2F2021%24252F07%24252F12%24252F%24255B%242524LATEST%24255D001160b1922d4cd1b8790b6ba8d202a3&isauthcode=true', 'MobileVersion': 'No', 'MFAUsed': 'No'}, 'eventID': '3bb2601d-fa66-435a-a053-201506b009f1', 'readOnly': False, 'eventType': 'AwsConsoleSignIn', 'managementEvent': True, 'eventCategory': 'Management', 'recipientAccountId': '079983867181'}

# eventDetails:
# {'eventTime': '2021-07-13T08:09:32Z', 'responseElements': {'ConsoleLogin': 'Success'}, 'sourceIPAddress': '202.173.124.217'}

# userDetails:
# {'arn': 'arn:aws:iam::079983867181:user/raghib.nadim@folium.cloud', 'accountId': '079983867181', 'userName': 'raghib.nadim@folium.cloud'}
