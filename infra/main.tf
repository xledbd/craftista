resource "aws_s3_bucket" "backend" {
  bucket_prefix = "terraform-backend"

  tags = {
    "Name" = "Terraform backend"
  }
}

resource "aws_s3_bucket_versioning" "backend" {
  bucket = aws_s3_bucket.backend.id

  versioning_configuration {
    status = "Enabled"
  }
}