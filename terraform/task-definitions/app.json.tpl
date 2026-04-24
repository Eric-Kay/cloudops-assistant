[
  {
    "name": "${project_name}",
    "image": "${image}",
    "essential": true,
    "portMappings": [
      {
        "containerPort": ${container_port},
        "hostPort": ${container_port},
        "protocol": "tcp"
      }
    ],
    "environment": [
      {
        "name": "AWS_REGION",
        "value": "${aws_region}"
      },
      {
        "name": "BEDROCK_MODEL_ID",
        "value": "${bedrock_model_id}"
      },
      {
        "name": "APP_USERNAME",
        "value": "${app_username}"
      },
      {
        "name": "S3_BUCKET_NAME",
        "value": "${s3_bucket_name}"
      }
    ],
    "secrets": [
      {
        "name": "JWT_SECRET",
        "valueFrom": "${jwt_secret_arn}"
      },
      {
        "name": "APP_PASSWORD",
        "valueFrom": "${app_password_arn}"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${log_group}",
        "awslogs-region": "${aws_region}",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }
]