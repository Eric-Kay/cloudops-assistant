terraform {
  backend "s3" {
    bucket       = "cloudops-assistant-tfstate-603108265570"
    key          = "cloudops-assistant/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
