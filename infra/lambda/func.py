import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)



#dynamodb = boto3.resource('dynamodb')
#table = dynamodb.Table('cloud-resume')

def get_table_resource():
    logging.info("Getting Table Ressource...")
    dynamodb_resource = boto3.resource("dynamodb")
    table_name = os.environ[ENV_TABLE_NAME]
    return dynamodb_resource.Table(table_name)


def get_views():
    table = get_table_resource()

    logging.info("Getting views...")
    response = table.get_item(Key={
        'id':'0'
    })
    views = response['Item']['views']
    return views

def update_views(views):
    logging.info("Updating views...")
    views +1
    response = table.put_item(Item={
            'id':'0',
            'views': views
    })
    return views


def lambda_handler(event, context):
    views = get_views()
    update_views(views)

    '''
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
    '''