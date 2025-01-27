import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloud-resume')

def lambda_handler(event, context):
    response = table.get_item(Key={'id':'0'})
    views = response['Item']['views']
    views = views + 1
    print(views)
    
    response = table.update_item(
        Key={'id':'0'},
        UpdateExpression='SET #v = :val',
        ExpressionAttributeNames={'#v': 'views'},
        ExpressionAttributeValues={':val': views}
    )
    return views