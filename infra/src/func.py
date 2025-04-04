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
def get_views(table, tableId):
    logging.info("Getting views...")
    response = table.get_item(Key={'id':tableId})
    if 'Item' in response:
        return response['Item']['views']
    else:
        logging.info("No Views Counter in DynamoDB Table. Creating...")
        updateTableItems(table, tableId)
        response = table.get_item(Key={'id':tableId})
        return response['Item']['views']

#Update table Items
def updateTableItems(table, tableId):
    logging.info("Updating Tabe Items...")
     # Add some items to the table
    item = {
        'id': tableId,
        'views': 0
        }
    table.put_item(Item=item)

#
def update_views(views, table, tableId):
    logging.info("Updating views...")
    response = table.update_item(
        Key={'id':tableId},
        UpdateExpression='SET #v = :val',
        ExpressionAttributeNames={'#v': 'views'},
        ExpressionAttributeValues={':val': views}
    )

def lambda_handler(event, context):

    tableId = event['queryStringParameters']['id']

    table = get_table_resource()
    views = get_views(table, tableId)
    views = views + 1
    update_views(views, table, tableId)
    
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin' : '*'},
        'body': get_views(table, tableId)
        }
        