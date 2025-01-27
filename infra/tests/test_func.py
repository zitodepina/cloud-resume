import importlib
import json
import os
import sys
from unittest import mock

import boto3
import pytest
from moto import mock_dynamodb

import func

@pytest.fixture

def dynamo_table():

    with mock_dynamodb():

        dynamo = boto3.resource('dynamodb')

        table = dynamo.create_table(

            TableName='visitor_count',

            KeySchema=[

                {'AttributeName': 'id', 'KeyType': 'HASH'}

            ],

            AttributeDefinitions=[

                {'AttributeName': 'id', 'AttributeType': 'S'}

            ]

        )

        yield table

def test_update_visitor_count_success(dynamo_table):

    # Create a test visitor count in DynamoDB
    dynamo_table.put_item(Item={'id': 'visitor_count', 'count': {'N': '0'}})

    # Call the Lambda function
    #response = func.lambda_handler({'httpMethod': 'GET'})
    response = func.lambda_handler({}, {})

    # Assert that the count is incremented
    assert response['statusCode'] == 200
    assert response['body'] == '{"count": 1}'
