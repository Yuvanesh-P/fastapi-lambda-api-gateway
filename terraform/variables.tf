variable "aws_region" {
  description = "AWS deployment region"
  type        = string
  default     = "ap-south-1"
}

variable "lambda_function_name" {
  description = "Existing Lambda function name"
  type        = string
  default     = "fastapi-lambda-api"
}

variable "lambda_role_name" {
  description = "Existing Lambda execution role"
  type        = string
  default     = "fastapi-lambda-execution-role"
}

variable "api_name" {
  description = "Existing API Gateway HTTP API name"
  type        = string
  default     = "fastapi-http-api"
}