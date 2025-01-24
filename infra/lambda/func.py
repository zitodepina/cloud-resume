import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_table_resource():
    logging.info("Getting Table Ressource...")
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table('cloud-resume')


def get_views(table):
    #table = get_table_resource()
    logging.info("Getting views...")
    response = table.get_item(Key={
        'id':'0'
    })
    return response['Item']['views']

def update_views(views):
    logging.info("Updating views...")
    table = get_table_resource()
    response = table.put_item(Item={
            'id':'0',
            'views': views
    })

def add_views(views):
    logging.info("Adding views...")
    views = views + 1
    return views

def lambda_handler(event, context):
    table = get_table_resource()
    views = get_views(table)
    views = add_views(views)
    update_views(views)
    return views