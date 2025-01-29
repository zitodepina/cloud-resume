import boto3
import pytest
import moto

import sys
sys.path.insert (0, 'infra/src')

from func import lambda_handler

TABLE_NAME = "data"

'''
@pytest.fixture
def dynamo_table():

    with moto.mock_dynamodb():

        dynamo = boto3.resource('dynamodb', region_name="us-east-1")

        table = dynamo.create_table(

            TableName=TABLE_NAME,
            KeySchema=[

                {'AttributeName': 'id', 'KeyType': 'HASH'}

            ],

            AttributeDefinitions=[

                {'AttributeName': 'id', 'AttributeType': 'S'}

            ]

        )
        yield TABLE_NAME


@pytest.fixture
def data_table_with_transactions(dynamo_table):
    """Creates transactions"""

    table = boto3.resource("dynamodb").Table(dynamo_table)
    views = 1

    response = table.update_item(
        Key={'id':'0'},
        UpdateExpression='SET #v = :val',
        ExpressionAttributeNames={'#v': 'views'},
        ExpressionAttributeValues={':val': views}
    )


def test_update_visitor_count_success(data_table_with_transactions):

    # Create a test visitor count in DynamoDB
   # dynamo_table.put_item(Item={'id': 'visitor_count', 'count': {'N': '0'}})

    # Call the Lambda function
    #response = func.lambda_handler({'httpMethod': 'GET'})
    response = lambda_handler({}, {})

    # Assert that the count is incremented
    assert response['statusCode'] == 200
    assert response['body'] == '{"count": 1}'
    '''

@moto.mock_dynamodb
def test_lambda_handler():

    table_name = 'test_counter'
    dynamodb = boto3.resource('dynamodb', 'us-east-1')

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'user_id','AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    response = lambda_handler({}, {})

    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'stat': {'S': 'view-count'}
        }
    )
    
    item = response['view-count']
