import os

import boto3
import moto
import pytest

import sys
sys.path.insert (0, 'infra/src')

from func import lambda_handler

TABLE_NAME = "data"

@pytest.fixture()
def aws_credentials():
    """Mocked AWS Credentials for moto library."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture
def dynamo_table():
    with moto.mock_dynamodb():
        dynamo = boto3.resource('dynamodb', region_name="us-east-1")
        table = dynamo.create_table(
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "views", "AttributeType": "N"}
            ],
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
                {"AttributeName": "views", "KeyType": "RANGE"}
            ],
            BillingMode="PAY_PER_REQUEST"
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