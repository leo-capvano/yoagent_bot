resource "aws_dynamodb_table" "users_table" {
  name         = var.users_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

}

# add an admin user
resource "aws_dynamodb_table_item" "default_user" {
  table_name = aws_dynamodb_table.users_table.name
  hash_key   = aws_dynamodb_table.users_table.hash_key

  item = jsonencode({
    user_id = { "S" = var.default_admin_user }
    role     = { "S" : "admin" }
  })
}

