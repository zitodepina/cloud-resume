#Cloudfront distribution
resource "aws_cloudfront_distribution" "cf_distribution" {
  
  enabled = true
  
  origin {
    origin_id                = local.s3_origin_id
    domain_name              = aws_s3_bucket.s3bucket.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id

    connection_attempts = 3
    connection_timeout = 10
   }


  default_root_object = "index.html"

  aliases = [
    var.domain_name
  ]

  default_cache_behavior {
    
    target_origin_id = local.s3_origin_id
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "https-only"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }


  viewer_certificate {
    cloudfront_default_certificate = false
    ssl_support_method  = "sni-only"
    //acm_certificate_arn = "arn:aws:acm:us-east-1:478586629041:certificate/db0f9148-bff4-4849-9516-35fe56a7ab56"
    acm_certificate_arn = aws_acm_certificate.ssl_cert.arn
    minimum_protocol_version = "TLSv1.2_2021"
  }

  price_class = "PriceClass_All"
  
}

locals {
  s3_origin_id = "${var.bucket_name}-origin"
}

resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = aws_s3_bucket.s3bucket.bucket
  description                       = "Origin Access Control for S3 Bucket"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

#Create Route53 Alias Record
resource "aws_route53_record" "www_a" {
  zone_id = var.route53_zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.cf_distribution.domain_name
    zone_id                = "Z2FDTNDATAQYW2" # CloudFront's zone ID
    evaluate_target_health = false
  }
}