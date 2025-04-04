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

# Archive the lambda function python code 
data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_file = "${path.module}/src/func.py"
  output_path = "${path.module}/src/func.zip"
}

#Provide Lambda function URL resource
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
