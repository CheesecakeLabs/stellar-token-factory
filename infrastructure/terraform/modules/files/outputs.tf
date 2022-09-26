output "app_bucket_public" {
  value = aws_s3_bucket.app_bucket_public.bucket
}

output "app_bucket_private" {
  value = aws_s3_bucket.app_bucket_private.bucket
}
