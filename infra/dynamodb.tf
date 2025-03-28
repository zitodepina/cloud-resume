# DynamoDB Table
resource "aws_dynamodb_table" "views_count_ddb" {
  name         = var.database
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  #range_key    = "views"
  
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

# DynamoDB Table Item
resource "aws_dynamodb_table_item" "views_count_ddb_items" {
  table_name = aws_dynamodb_table.views_count_ddb.name
  hash_key   = aws_dynamodb_table.views_count_ddb.hash_key
  #range_key   = aws_dynamodb_table.views_count_ddb.range_key

  item = <<ITEM
  {
    "id": {"S": "${var.id}"},
    "views": {"N": "1"}
  }
  ITEM
}