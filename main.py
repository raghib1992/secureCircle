import boto3
import time
import logging

tableName = "cloudtrail_logs_aws_cloudtrail_logs_raghib_test"
eventName = "ConsoleLogin"
dbName    = "default"
output    = "s3://saas-ses-email-query-result/"
dynamotableName = "trial-test"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getIamUserListFromAthena():
    client = boto3.client('athena')
    # query = "SELECT * FROM "default"."cloudtrail_logs_aws_cloudtrail_logs_raghib_test" WHERE eventname = \'{}\'".format(EventType)
    # query = "SELECT * FROM {} WHERE eventname = \'{}\'".format(tableName, eventName)useridentity
    query = "SELECT useridentity.accountid,useridentity.username,eventtime FROM {} WHERE eventname = \'{}\'".format(tableName, eventName)
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
    dynamodb = update_dynamoDB(getQueryResult)
    return getQueryResult

def update_dynamoDB(userAndAccessDetails):   
    dynamodb = boto3.resource('dynamodb')
    expiryTimestamp = int(time.time()  + 60)
    table = dynamodb.Table(dynamotableName)
    with table.batch_writer(overwrite_by_pkeys=['userName']) as batch:
        for row in userAndAccessDetails['ResultSet']['Rows']:
            if row['Data'][0]['VarCharValue'] != 'accountid':
                account_ID = row['Data'][0]['VarCharValue']
                username = row['Data'][1]['VarCharValue']
                eventTime = row['Data'][2]['VarCharValue']
                batch.put_item(
                    Item={
                        'userName': eventTime,
                        'Account_ID': account_ID,
                        'EventTime': username,
                        'TTL' : expiryTimestamp
                    }
            )
        # logger.info("User \"{}\" access id \"{}\" updated in dynamodb".format(userName,userID))

getIamUserListFromAthena()