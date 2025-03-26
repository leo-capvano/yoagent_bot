resource "aws_secretsmanager_secret" "llm_api_key_secret" {
  name = "llm_api_key/${var.llm_api_key_admin_username_secret_name}"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "secret_version" {
  secret_id               = aws_secretsmanager_secret.llm_api_key_secret.id
  secret_string = file(var.file_path_containing_llm_api_key)
}
