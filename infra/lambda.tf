locals {
  lambda_yoagent_bot_be_zip_file_name = "yoagent_bot_be.zip"
}

provider "archive" {}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "../src/bot/"
  output_path = local.lambda_yoagent_bot_be_zip_file_name
}

module "lambda_yoagent_bot_be" {
  source = "terraform-aws-modules/lambda/aws"
  function_name = "yoagent_bot_be"
  description   = "My awesome lambda function for yoagent_bot telegram bot"
  handler       = "yoagent_bot.lambda_handler"
  runtime       = "python3.12"
  timeout = var.lambda_yoagent_bot_be_timeout
  create_lambda_function_url = false
  create_package         = false
  local_existing_package = local.lambda_yoagent_bot_be_zip_file_name
  cloudwatch_logs_retention_in_days = 1

  layers = [
    "arn:aws:lambda:eu-west-1:015030872274:layer:AWS-Parameters-and-Secrets-Lambda-Extension:12",
    aws_lambda_layer_version.bot_layer.arn
  ]

  environment_variables = {
    TELEGRAM_BOT_TOKEN = file(var.telegram_bot_token_file)
    BOT_WEBHOOK_SECRET_TOKEN = file(var.telegram_bot_webhook_token_file)
    BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY = var.telegram_bot_webhook_secret_token_header_key
    AUTHORIZATION_SECRET = file(var.authorization_secret_file)
    USERS_TABLE_NAME                    = var.users_table_name
  }
}

resource "aws_lambda_layer_version" "bot_layer" {
  filename   = "layer/bot_layer.zip"
  layer_name = "bot_layer"
  compatible_runtimes = ["python3.12"]
  description = "Layer containing Bot dependencies (eg langchain and langgraph)"
}

module "lambda_yoagent_apigw_authorizer" {
  source = "terraform-aws-modules/lambda/aws"
  function_name = "yoagent_apigw_authorizer"
  description   = "My awesome lambda function for api gw authorizer"
  handler       = "authorizer.lambda_handler"
  runtime       = "python3.12"
  source_path                = "./authorizer.py"
  create_lambda_function_url = false
  cloudwatch_logs_retention_in_days = 1

  environment_variables = {
    BOT_WEBHOOK_SECRET_TOKEN = file(var.telegram_bot_webhook_token_file)
    BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY = var.telegram_bot_webhook_secret_token_header_key
    AUTHORIZATION_SECRET = file(var.authorization_secret_file)
  }
}