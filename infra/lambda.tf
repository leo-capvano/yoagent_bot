module "lambda_yoagent_bot_be" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "yoagent_bot_be"
  description   = "My awesome lambda function for yoagent_bot telegram bot"
  handler       = "yoagent_bot.lambda_handler"
  runtime       = "python3.12"

  source_path                = "../bot/yoagent_bot.py"
  create_lambda_function_url = false

  cloudwatch_logs_retention_in_days = 1

  environment_variables = {
    TELEGRAM_BOT_TOKEN = file("../.bot_token")
    BOT_WEBHOOK_SECRET_TOKEN = file("../.bot_webhook_secret_token")
    BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY = "X-Telegram-Bot-Api-Secret-Token"
  }
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
    BOT_WEBHOOK_SECRET_TOKEN = file("../.bot_webhook_secret_token")
    BOT_WEBHOOK_SECRET_TOKEN_HEADER_KEY = "X-Telegram-Bot-Api-Secret-Token"
  }
}