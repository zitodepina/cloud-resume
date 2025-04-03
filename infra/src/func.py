import os
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Get Table Resource
def get_table_resource():
    logging.info("Getting Table Ressource...")
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv("REGION"))
    return dynamodb.Table(os.getenv("DYNAMODB_TABLE"))


#get views from db
def get_views(table):
    logging.info("Getting views...")
    response = table.get_item(Key={'id':os.getenv("ID")})
    if 'Item' in response:
        return response['Item']['views']
    else:
        logging.info("No Views Counter in DynamoDB Table. Creating...")
        updateTableItems(table)
        response = table.get_item(Key={'id':os.getenv("ID")})
        return response['Item']['views']

#Update table Items
def updateTableItems(table):
    logging.info("Updating Tabe Items...")
     # Add some items to the table
    item = {
        'id': os.getenv("ID"),
        'views': 0
        }
    table.put_item(Item=item)

#
def update_views(views, table):
    logging.info("Updating views...")
    response = table.update_item(
        Key={'id':os.getenv("ID")},
        UpdateExpression='SET #v = :val',
        ExpressionAttributeNames={'#v': 'views'},
        ExpressionAttributeValues={':val': views}
    )

def lambda_handler(event, context):
    table = get_table_resource()
    views = get_views(table)
    views = views + 1
    update_views(views, table)
    
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin' : '*'},
        'body': get_views(table)
        }
        