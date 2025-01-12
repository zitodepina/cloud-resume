import json
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloud-resume')
def lambda_handler(event, context):
    print(table.creation_date_time)
    response = table.get_item(Key={
        'id':'0'
    })
    views = response['Item']['views']
    views = views + 1
    print(views)
    response = table.put_item(Item={
            'id':'0',
            'views': views
    })
    return views