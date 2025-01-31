import importlib
import os
import boto3
import pytest
import json
import moto
from unittest import mock

#from moto import mock_aws

import sys
sys.path.insert (0, 'infra/src')

#from func import lambda_handler

TABLE_NAME = "data"


@pytest.fixture()
def aws_credentials():
    """Mocked AWS Credentials for moto library."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@moto.mock_dynamodb
def test_lambda_handler_existing_entries(aws_credentials):
    """Testing visitors updating when there are entries available in dynamodb table."""
    app_module = importlib.import_module("src.func")
    table = app_module.dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "key", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {
                "AttributeName": "key",
                "AttributeType": "S",
            },
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )
    table.wait_until_exists()

    app_module.dynamodb.put_item(
        Item={"key": "0", "views": 1},
    )

    response = app_module.lambda_handler({}, {})

    assert response["statusCode"] == 200
    assert response["body"] == json.dumps({"visits": 2})
    '''
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Headers"] == "Content-Type, Origin"
    assert response["headers"]["Access-Control-Allow-Origin"] == "http://localhost"
    assert response["headers"]["Access-Control-Allow-Methods"] == "OPTIONS,POST,GET"
    '''

    dynamodb_response = app_module.table.get_item(
        Key={"keyw": "0"}
    )

    assert int(dynamodb_response["Item"]["views"]) == 2

@moto.mock_dynamodb
def test_lambda_handler_empty_table(aws_credentials):
    """Testing visitors updating when there are no entries in dynamodb table."""
    app_module = importlib.import_module("src.func")
    table = app_module.dynamodb.create_table(
         TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "key", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {
                "AttributeName": "key",
                "AttributeType": "S",
            },
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )
    table.wait_until_exists()

    response = app_module.lambda_handler({}, {})

    assert response["statusCode"] == 200
    assert response["body"] == json.dumps({"visits": 1})
    '''
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Headers"] == "Content-Type, Origin"
    assert response["headers"]["Access-Control-Allow-Origin"] == "http://localhost"
    assert response["headers"]["Access-Control-Allow-Methods"] == "OPTIONS,POST,GET"
    '''

    dynamodb_response = app_module.table.get_item(
        Key={"CounterName": "visitorsCounter"}
    )

    assert int(dynamodb_response["Item"]["visits"]) == 1