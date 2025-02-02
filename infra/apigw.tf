resource "aws_api_gateway_rest_api" "yoagent_bot_apigw" {
  name        = "yoagent_bot_apigw"
  description = "My awesome HTTP API Gateway for yoagent_bot telegram bot"
  api_key_source = "AUTHORIZER"
}

resource "aws_api_gateway_resource" "yoagent_resource" {
  rest_api_id = aws_api_gateway_rest_api.yoagent_bot_apigw.id
  parent_id   = aws_api_gateway_rest_api.yoagent_bot_apigw.root_resource_id
  path_part   = "yoagent"
}

resource "aws_api_gateway_method" "yoagent_method" {
  rest_api_id   = aws_api_gateway_rest_api.yoagent_bot_apigw.id
  resource_id   = aws_api_gateway_resource.yoagent_resource.id
  http_method   = "POST"
  authorization = "CUSTOM"
  authorizer_id = aws_api_gateway_authorizer.yoagent_lambda_authorizer.id
  api_key_required = true
}

resource "aws_api_gateway_method_settings" "example" {
  rest_api_id = aws_api_gateway_rest_api.yoagent_bot_apigw.id
  stage_name  = aws_api_gateway_stage.yoagent_stage1.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled         = true
    logging_level          = "INFO"
    data_trace_enabled     = true
    throttling_burst_limit = 2
    throttling_rate_limit  = 2
  }
}

resource "aws_api_gateway_integration" "yoagent_lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.yoagent_bot_apigw.id
  resource_id = aws_api_gateway_method.yoagent_method.resource_id
  http_method = aws_api_gateway_method.yoagent_method.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = module.lambda_yoagent_bot_be.lambda_function_invoke_arn
}

resource "aws_api_gateway_deployment" "yoagent_deployment" {
  depends_on = [
    aws_api_gateway_integration.yoagent_lambda_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.yoagent_bot_apigw.id
}

resource "aws_api_gateway_stage" "yoagent_stage1" {
  deployment_id = aws_api_gateway_deployment.yoagent_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.yoagent_bot_apigw.id
  stage_name    = "yoagent_stage1"

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.apigw_cw_log_group.arn
    format = jsonencode({
      requestId      = "$context.requestId",
      ip             = "$context.identity.sourceIp",
      caller         = "$context.identity.caller",
      user           = "$context.identity.user",
      requestTime    = "$context.requestTime",
      httpMethod     = "$context.httpMethod",
      resourcePath   = "$context.resourcePath",
      status         = "$context.status",
      protocol       = "$context.protocol",
      responseLength = "$context.responseLength"
    })
  }
}

# monitoring

resource "aws_api_gateway_account" "main" {
  cloudwatch_role_arn = aws_iam_role.main.arn
}

resource "aws_iam_role" "main" {
  name = "api-gateway-logs-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_cloudwatch_log_group" "apigw_cw_log_group" {
  name              = "API-Gateway-Execution-Logs_${aws_api_gateway_rest_api.yoagent_bot_apigw.id}/yoagent_stage1"
  retention_in_days = 1
}

# usage plan

resource "aws_api_gateway_usage_plan" "yoagent_stage1_usage_plan" {
  name         = "yoagent_stage1_usage_plan"
  description  = "Usage plan for stage 1 of yoagent_bot"
  product_code = "yoagent_bot"

  api_stages {
    api_id = aws_api_gateway_rest_api.yoagent_bot_apigw.id
    stage  = aws_api_gateway_stage.yoagent_stage1.stage_name
  }

  quota_settings {
    # max 100 requests per day
    limit  = 100
    period = "DAY"
  }

  throttle_settings {
    burst_limit = 2 # num of concurrent requests
    rate_limit = 2 # num of requests per seconds
  }
}

resource "aws_api_gateway_usage_plan_key" "main" {
  key_id        = aws_api_gateway_api_key.telegram_api_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.yoagent_stage1_usage_plan.id
}

resource "aws_api_gateway_api_key" "telegram_api_key" {
  name = "telegram_api_key"
  value = file("../.bot_webhook_secret_token")
}

# authorizer

resource "aws_api_gateway_authorizer" "yoagent_lambda_authorizer" {
  name                   = "yoagent_lambda_authorizer"
  rest_api_id            = aws_api_gateway_rest_api.yoagent_bot_apigw.id
  authorizer_uri         = module.lambda_yoagent_apigw_authorizer.lambda_function_invoke_arn
  authorizer_credentials = aws_iam_role.authorizer_credentials.arn
  type = "REQUEST"
  identity_source = "method.request.header.X-Telegram-Bot-Api-Secret-Token"
}

resource "aws_iam_role" "authorizer_credentials" {
  name               = "api_gateway_auth_invocation"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.authorizer_credentials_assume_role.json
}

data "aws_iam_policy_document" "authorizer_credentials_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["apigateway.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role_policy" "invocation_policy" {
  name   = "invocation_policy"
  role   = aws_iam_role.authorizer_credentials.id
  policy = data.aws_iam_policy_document.invocation_policy.json
}

data "aws_iam_policy_document" "invocation_policy" {
  statement {
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = [module.lambda_yoagent_apigw_authorizer.lambda_function_arn]
  }
}

# policies

resource "aws_api_gateway_rest_api_policy" "yoagent_resource_policy" {
  rest_api_id = aws_api_gateway_rest_api.yoagent_bot_apigw.id
  policy      = data.aws_iam_policy_document.allow_only_from_telegram_subnets.json
}

data "aws_iam_policy_document" "allow_only_from_telegram_subnets" {
  statement {
    effect = "Allow"
    principals {
      type = "*"
      identifiers = ["*"]
    }
    actions = ["execute-api:Invoke"]
    resources = ["execute-api:/*/POST/yoagent"]
  }
  statement {
    effect = "Deny"
    principals {
      type = "*"
      identifiers = ["*"]
    }
    actions = ["execute-api:Invoke"]
    resources = ["execute-api:/*/POST/yoagent"]
    condition {
      test     = "NotIpAddress"
      variable = "aws:SourceIp"
      values = [
        "149.154.160.0/20",
        "91.108.4.0/22"
      ]
    }
  }
}
