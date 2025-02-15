variable "yoagent_rest_api_max_request_per_day" {
  default = 100
  type = number
  description = "The maximum number of requests per day for the API"
}

variable "cloudwatch_log_group_retention_in_days" {
  default = 1
  type = number
  description = "Retention in days of cloudwatch log group"
}

variable "telegram_ip_whitelist" {
  default = ["149.154.160.0/20", "91.108.4.0/22"]
  type = list(string)
  description = "Telegram IPs to whitelist"
}

variable "lambda_authorizer_identity_source" {
  default = "method.request.header.X-Telegram-Bot-Api-Secret-Token"
  type = string
  description = "The identity source of the lambda authorizer"
}

variable "telegram_bot_webhook_secret_token_header_key" {
  default = "X-Telegram-Bot-Api-Secret-Token"
  type = string
  description = "The name of the header that contains the webhook token"
}

variable "telegram_bot_webhook_token_file" {
  default = "../.bot_webhook_secret_token"
  type = string
  description = "The file containing the telegram webhook secret token"
}

variable "telegram_bot_token_file" {
  default = "../.bot_token"
  type = string
  description = "The file containing the telegram secret token"
}

variable "authorization_secret_file" {
  default = "../.authorization_secret"
  type = string
  description = "The file containing the secret sent by the authorizer"
}

