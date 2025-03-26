# Give API GW Permission to invoke lambda
resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_yoagent_bot_be.lambda_function_arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.yoagent_bot_rest_api.execution_arn}/*/*"
}

resource "aws_iam_role" "lambda" {
  name               = "allow_lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# IAM policy used by lambda bot to access SecretsManager and retrieve LLM API Key
resource "aws_iam_policy" "secrets_manager_access" {
  name        = "SecretsManagerAccessPolicy"
  description = "Allows Lambda to access AWS Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = aws_secretsmanager_secret.llm_api_key_secret.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_secrets_manager" {
  policy_arn = aws_iam_policy.secrets_manager_access.arn
  role       = module.lambda_yoagent_bot_be.lambda_role_name
}
