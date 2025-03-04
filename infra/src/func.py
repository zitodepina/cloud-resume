import os
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table('cloud-resume')
#table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))

#get views from db
def get_views():
    logging.info("Getting views...")
    response = table.get_item(Key={'id':'0'})
    return response['Item']['views']

def update_views(views):
    logging.info("Updating views...")
    response = table.update_item(
        Key={'id':'0'},
        UpdateExpression='SET #v = :val',
        ExpressionAttributeNames={'#v': 'views'},
        ExpressionAttributeValues={':val': views}
    )

def lambda_handler(event, context):
    views = get_views()
    views = int(views) + 1
    update_views(views)
    
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': 
        {"Content-Type": "application/json",},
        'body': get_views()
        }
   