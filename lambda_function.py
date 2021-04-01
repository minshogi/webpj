# import the json utility package since we will be working with a JSON object
import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
# import two packages to help us with dates and date formatting

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('Probs')


# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
# extract values from the event object we got from the Lambda service and store in a variable
    ID = event['getpic'] + '_' + event['ndol'] + '_' + event['stack']
    find = event['stack'] +'_'+ event['gacha']
# write name and time to the DynamoDB table using the object we instantiated and save response in a variable
    response = table.get_item(
        Key={"ID": ID})
    print(response)
    xs = response["Item"]["Prob"]
# return a properly formatted JSON object
    ret = "100%"

    if int(event['gacha']) <= 0:
        ret = "0%"   

    for str in xs:
        if find in str:
            ret = str.split()[1]
            break
    

    
    return {
        'statusCode': 200,
        'body': json.dumps(ret)
    }
    