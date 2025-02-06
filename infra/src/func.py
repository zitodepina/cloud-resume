import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'cloud-resume'

def get_table_resource(TABLE_NAME):
    logging.info("Getting Table Ressource...")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    return dynamodb.Table(TABLE_NAME)


def get_views(table):
    logging.info("Getting views...")
    response = table.get_item(Key={
        'id':'0'
    })
    return response['Item']['views']

def update_views(views, table):
    logging.info("Updating views...")
    response = table.update_item(
        Key={'id':'0'},
        UpdateExpression='SET #v = :val',
        ExpressionAttributeNames={'#v': 'views'},
        ExpressionAttributeValues={':val': views}
    )

def lambda_handler(TABLE_NAME, context):
    table = get_table_resource(TABLE_NAME)
    views = get_views(table)
    views = int(views) + 1
    update_views(views, table)
    return views
