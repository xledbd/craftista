import {
  to = aws_s3_bucket.catalogue-db-init
  id = "craftista-catalogue-db"
}

resource "aws_s3_bucket" "catalogue-db-init" {
  bucket = "craftista-catalogue-db"
}

resource "aws_dynamodb_table" "catalogue-dev" {
  name           = "craftista-catalogue-dev"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  import_table {
    input_compression_type = "NONE"
    input_format           = "CSV"

    s3_bucket_source {
      bucket     = aws_s3_bucket.catalogue-db-init.id
      key_prefix = "init/"
    }
  }

  tags = {
    "Name"        = "craftista-catalogue-dev"
    "Environment" = "dev"
  }
}