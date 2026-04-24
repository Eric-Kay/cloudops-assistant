aws_region       = "us-east-1"
project_name     = "cloudops-assistant"
app_image        = "603108265570.dkr.ecr.us-east-1.amazonaws.com/cloudops-assistant:v2"
bedrock_model_id = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
app_username     = "admin"

vpc_id = "vpc-08fcfd0487e79fd90"

public_subnet_ids = [
  "subnet-096ad404115c60073",
  "subnet-080cbb322b43a125b"
]
