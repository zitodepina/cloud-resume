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
    os.environ["DYNAMODB_TABLE"] = "test-dynamodb"
    os.environ["ID"] = "adp"

@mock_aws
def test_lambda_handler_existing_entries(aws_credentials):
    """Testing visitors updating when there are entries available in dynamodb table."""
    dynamo = boto3.resource('dynamodb', region_name="us-east-1")
    
    table = dynamo.create_table(
        TableName=os.getenv("DYNAMODB_TABLE"),
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
        'id': os.getenv("ID"),
        'views': 1
        }
        
    table.put_item(Item=item)
    
    event = {'pathParameters': {'id': 'adp'}}
        
    response = lambda_handler(event, {})

    assert response["statusCode"] == 200
    #assert response["headers"]["Content-Type"] == "application/json"
    assert response["body"] == 2
