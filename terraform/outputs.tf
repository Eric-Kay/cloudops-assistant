output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "uploads_bucket_name" {
  value = aws_s3_bucket.uploads.bucket
}

output "alb_dns_name" {
  value = aws_lb.app.dns_name
}

output "app_url" {
  value = "http://${aws_lb.app.dns_name}"
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.this.name
}

output "ecs_service_name" {
  value = aws_ecs_service.app.name
}

output "jwt_secret_arn" {
  value = aws_secretsmanager_secret.jwt_secret.arn
}

output "app_password_secret_arn" {
  value = aws_secretsmanager_secret.app_password.arn
}