# lambda function creation
resource "aws_lambda_function" "myfunc" {
  filename         = data.archive_file.zip_the_python_code.output_path
  source_code_hash = data.archive_file.zip_the_python_code.output_base64sha256
  function_name    = "myfunc"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "func.lambda_handler"
  runtime          = "python3.12"

  environment {
    variables = {
      DYNAMODB_TABLE = var.database
      REGION = var.region
    }
  }
}

# create lambda iam role
resource "aws_iam_role" "iam_for_lambda" {
name = "iam_for_lambda"

assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
# create lambda iam role policy
resource "aws_iam_policy" "iam_policy_for_resume_project" {

  name        = "aws_iam_policy_for_terraform_resume_project_policy"
  path        = "/"
  description = "AWS IAM Policy for managing the resume project role"
    policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Resource" : "arn:aws:logs:*:*:*",
          "Effect" : "Allow"
        },
        {
          "Effect" : "Allow",
          "Action" : [
            "dynamodb:*"
          ],
          "Resource" : "arn:aws:dynamodb:*:*:table/cloud-resume"
        },
      ]
  })
}
# iam role policy attachment to lambda role
resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
  role = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.iam_policy_for_resume_project.arn
  
}

# Archive the lambda function python code 
data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_file = "${path.module}/src/func.py"
  output_path = "${path.module}/src/func.zip"
}

resource "aws_lambda_function_url" "url1" {
  function_name      = aws_lambda_function.myfunc.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    allow_headers     = ["date", "keep-alive"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }
}

/*
# Create an S3 bucket
resource "aws_s3_bucket" "example_bucket" {
  bucket = "cloud-resume-adp" 
  
  tags = {
    Name  = "My resume bucket"
  }
}
*/

# DynamoDB Table
resource "aws_dynamodb_table" "views_count_ddb" {
  name         = var.database
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  range_key    = "views"
  
  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "views"
    type = "N"
  }

  tags = {
    Name = var.database
  }
}

# DynamoDB Table Item
resource "aws_dynamodb_table_item" "views_count_ddb_items" {
  table_name = aws_dynamodb_table.views_count_ddb.name
  hash_key   = aws_dynamodb_table.views_count_ddb.hash_key
  range_key   = aws_dynamodb_table.views_count_ddb.range_key

  item = <<ITEM
  {
    "id": {"S": "${var.id}"},
    "views": {"N": "1"}
  }
  ITEM
}



#API gateway entry
resource "aws_api_gateway_rest_api" "resume_project_gateway" {
  name = "resumeprojectgateway"
  description = "Proxy to handle requests to our API"
  
}

# RESOURCES
resource "aws_api_gateway_resource" "views_gateway_resource" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  parent_id   = aws_api_gateway_rest_api.resume_project_gateway.root_resource_id
  path_part   = "visitor"
}

# METHODS

resource "aws_api_gateway_method" "views_gateway_method" {
  rest_api_id   = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id   = aws_api_gateway_resource.views_gateway_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "views_gateway_options_method" {
  rest_api_id   = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id   = aws_api_gateway_resource.views_gateway_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# RESPONSES

resource "aws_api_gateway_method_response" "views_gateway_response_200" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id = aws_api_gateway_method.views_gateway_method.resource_id
  http_method = aws_api_gateway_method.views_gateway_method.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }
  depends_on = [aws_api_gateway_method.views_gateway_options_method]
}

resource "aws_api_gateway_method_response" "options_200" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id = aws_api_gateway_method.views_gateway_options_method.resource_id
  http_method = aws_api_gateway_method.views_gateway_options_method.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
  depends_on = [aws_api_gateway_method.views_gateway_options_method]
}


# INTEGRATIONS

resource "aws_api_gateway_integration" "integration" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id = aws_api_gateway_resource.views_gateway_resource.id
  http_method = aws_api_gateway_method.views_gateway_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.myfunc.invoke_arn
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.myfunc.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.resume_project_gateway.execution_arn}/*/*"
}

resource "aws_api_gateway_integration" "options_integration" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id = aws_api_gateway_method.views_gateway_options_method.resource_id
  http_method = aws_api_gateway_method.views_gateway_options_method.http_method
  type        = "MOCK"
  depends_on  = [aws_api_gateway_method.views_gateway_options_method]
}


# INTEGRATION RESPONSES

resource "aws_api_gateway_integration_response" "options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id = aws_api_gateway_method.views_gateway_options_method.resource_id
  http_method = aws_api_gateway_method.views_gateway_options_method.http_method
  status_code = aws_api_gateway_method_response.options_200.status_code
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
  depends_on = [aws_api_gateway_method_response.options_200]
}



# DEPLOYMENTS
resource "aws_api_gateway_deployment" "resume_project_gateway_deployment" {
  depends_on = [
    aws_api_gateway_integration.integration
  ]
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
}

# STAGE
resource "aws_api_gateway_stage" "resume_project_gateway_stage" {
  deployment_id = aws_api_gateway_deployment.resume_project_gateway_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.resume_project_gateway.id
  stage_name    = "prod"
}

resource "aws_api_gateway_method_settings" "resume_project_gateway_method_settings" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  stage_name  = aws_api_gateway_stage.resume_project_gateway_stage.stage_name
  method_path = "*/*"
  
  settings {
    metrics_enabled = true
  }
}




