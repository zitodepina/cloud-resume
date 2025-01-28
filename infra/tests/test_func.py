import boto3
import pytest
import moto

import sys
sys.path.insert (0, 'infra/src')

from func import lambda_handler

TABLE_NAME = "data"


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



@pytest.fixture
def test_update_visitor_count_success(data_table_with_transactions):

   views = 1 
    # Create a test visitor count in DynamoDB
   response = table.update_item(
        Key={'id':'0'},
        UpdateExpression='SET #v = :val',
        ExpressionAttributeNames={'#v': 'views'},
        ExpressionAttributeValues={':val': views}
    )

    # Call the Lambda function
    #response = func.lambda_handler({'httpMethod': 'GET'})
    response = lambda_handler({}, {})

    # Assert that the count is incremented
    assert response['statusCode'] == 200
    assert response['body'] == '{"count": 1}'
