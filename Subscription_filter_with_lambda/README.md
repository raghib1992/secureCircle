# Create role
aws iam create-role --role-name CWloguser --assume-role-policy-document file://trust-policy.json


# attach policy
aws iam attach-role-policy --role-name CWloguser --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Create Lambda Function
aws lambda create-function --function-name helloworld --zip-file fileb://helloWorld.zip --role arn:aws:iam::079983867181:role/CWloguser --handler helloWorld.handler --runtime nodejs14.x

# Create CloudWatch log group
aws logs create-log-group --log-group-name trailLog

# Grant CloudWatch Logs the permission to execute your Function
aws lambda add-permission --function-name "helloworld" --statement-id "helloworld12" --principal "logs.ap-south-1.amazonaws.com" --action "lambda:InvokeFunction" --source-arn "arn:aws:logs:ap-south-1:079983867181:log-group:trailLog:*" --source-account "079983867181"

# remove statement id
aws lambda remove-permission --function-name helloworld --statement-id helloworld

# Create a subscription filter using the following command
aws logs put-subscription-filter --log-group-name trailLog --filter-name console-login-log --filter-pattern "" --destination-arn arn:aws:lambda:ap-south-1:079983867181:function:helloworld

# test
aws logs put-log-events --log-group-name trailLog --log-stream-name test-log --log-events "[{\"timestamp\": 1625749474 , \"message\": \"Simple Lambda Test 1\"}]"

aws logs put-log-events --log-group-name trailLog --log-stream-name test-log --log-events file://events --sequence-token "49617197776791566618540528674177724173865833156566938738"