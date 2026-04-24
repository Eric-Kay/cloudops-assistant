variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "cloudops-assistant"
}

variable "container_port" {
  type    = number
  default = 8000
}

variable "container_cpu" {
  type    = number
  default = 256
}

variable "container_memory" {
  type    = number
  default = 512
}

variable "desired_count" {
  type    = number
  default = 1
}

variable "app_image" {
  type        = string
  description = "Full ECR image URI"
}

variable "bedrock_model_id" {
  type    = string
  default = "anthropic.claude-3-haiku-20240307-v1:0"
}

variable "app_username" {
  type    = string
  default = "admin"
}

variable "vpc_id" {
  type = string
}

variable "public_subnet_ids" {
  type = list(string)
}

variable "jwt_secret_name" {
  type    = string
  default = "cloudops-assistant/jwt"
}

variable "app_password_secret_name" {
  type    = string
  default = "cloudops-assistant/app-password"
}

variable "ui_image" {
  type        = string
  description = "Full ECR image URI for Streamlit UI"
}

variable "ui_container_port" {
  type    = number
  default = 8501
}