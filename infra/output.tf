output "base_url" {
  value = "${aws_api_gateway_deployment.yoagent_deployment.invoke_url}yoagent_stage1/yoagent"
}

output "yoagent_lambda_url" {
  value = module.lambda_yoagent_bot_be.lambda_function_url
}