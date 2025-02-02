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