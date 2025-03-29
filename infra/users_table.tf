resource "aws_dynamodb_table" "users_table" {
  name         = var.users_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "username"

  attribute {
    name = "username"
    type = "S"
  }

}

# add an admin user
resource "aws_dynamodb_table_item" "default_user" {
  table_name = aws_dynamodb_table.users_table.name
  hash_key   = "username"

  item = jsonencode({
    username = { "S" = var.default_admin_user }
    role     = { "S" : "admin" }
  })
}

