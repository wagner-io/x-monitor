resource "aws_s3_bucket" "indexes" {
  bucket = "x-monitor-indexes"
}

resource "aws_s3_bucket_versioning" "indexes_v" {
  bucket = aws_s3_bucket.indexes.id
  versioning_configuration { status = "Enabled" }
}