terraform {
  backend "s3" {
    bucket       = "terraform-backend20250311100019716100000001"
    key          = "terraform.tfstate"
    region       = "eu-central-1"
    use_lockfile = true
  }
}