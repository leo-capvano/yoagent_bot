resource "aws_s3_bucket" "lambda_layers" {
  bucket = "yoagent-lambda-layers-bucket"
}

resource "aws_s3_object" "requirements_layer_s3_obj" {
  bucket = aws_s3_bucket.lambda_layers.bucket
  key    = "layers/requirements_layer.zip"
  source = "layer/requirements_layer.zip"
  etag = filemd5("layer/requirements_layer.zip")
}
