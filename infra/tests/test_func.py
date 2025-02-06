import os
import json
import boto3
import pytest

from moto import mock_aws

import sys
sys.path.insert (0, 'infra/src')

from func import lambda_handler
from func import get_views

TABLE_NAME = "test_counter"

@pytest.fixture()
def aws_credentials():
    """Mocked AWS Credentials for moto library."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@mock_aws
def test_lambda_handler_existing_entries(aws_credentials):
    """Testing visitors updating when there are entries available in dynamodb table."""
    dynamo = boto3.resource('dynamodb', region_name="us-east-1")
    
    table = dynamo.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {
                "AttributeName": "id",
                "AttributeType": "S",
            },
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    table.wait_until_exists()
    # Add some items to the table
    item = {
        'id': '0',
        'views': '1'
        }
        
    table.put_item(Item=item)

    #response = get_views(table)
    #assert int(response) == 1
        
    response = lambda_handler(TABLE_NAME, {})
    assert int(response) == 2


'''
    # Assert that the count is incremented
    assert response["statusCode"] == 200
    assert response["body"] == json.dumps({"visits": 2})
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Headers"] == "Content-Type, Origin"
    assert response["headers"]["Access-Control-Allow-Origin"] == "http://localhost"
    assert response["headers"]["Access-Control-Allow-Methods"] == "OPTIONS,POST,GET"
    


    response = table.get_item(
        Key={"id": "0"}
    )
    assert int(response["Item"]["views"]) == 2
    '''
    

    





'''
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