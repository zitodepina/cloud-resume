# Create an S3 bucket
resource "aws_s3_bucket" "s3bucket" {
  bucket = var.bucket_name
  
  tags = {
    Name  = var.bucket_name
  }
}

#Attach a policy to an S3 bucket resource
resource "aws_s3_bucket_policy" "bucket-policy" {
  bucket = aws_s3_bucket.s3bucket.id

  policy = jsonencode(
   {
    "Version": "2008-10-17",
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
             "Resource": "arn:aws:s3:::${aws_s3_bucket.s3bucket.bucket}/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::478586629041:distribution/${aws_cloudfront_distribution.cf_distribution.id}"
                }
            }
        }
    ]
}
)
}