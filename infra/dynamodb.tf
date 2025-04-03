# DynamoDB Table
resource "aws_dynamodb_table" "views_count_ddb" {
  name         = var.database
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
 
  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "views"
    type = "N"
  }

   global_secondary_index {
    name               = "ViewCountIndex"
    hash_key           = "views"
    projection_type    = "ALL"
  }

  tags = {
    Name = var.database
  }
}


