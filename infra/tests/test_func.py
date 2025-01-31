import importlib
import boto3
import pytest
from unittest import mock
from moto import mock_dynamodb

import sys
sys.path.insert (0, 'infra/src')

#from func import lambda_handler

TABLE_NAME = "data"

@mock_dynamodb
def test_lambda_handler_existing_entries():
    """Testing visitors updating when there are entries available in dynamodb table."""
    app_module = importlib.import_module("src.func")
    table = table = app_module.dynamodb.create_table(
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

    app_module.dynamodb_table.put_item(
        Item={"key": "0", "views": 1},
    )

    response = app_module.handler({}, {})

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

@mock_dynamodb
def test_lambda_handler_empty_table():
    """Testing visitors updating when there are no entries in dynamodb table."""
    app_module = importlib.import_module("src.func")
    table = table = app_module.dynamodb.create_table(
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

    response = app_module.handler({}, {})

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