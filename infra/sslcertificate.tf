// Create SSL certificate
resource "aws_acm_certificate" "ssl_cert" {
  domain_name       = var.domain_name
  validation_method = "DNS"

  tags = {
    Environment = var.environment
  }

  lifecycle {
    create_before_destroy = true
  }
}

#Cert Validation
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for d in aws_acm_certificate.ssl_cert.domain_validation_options : d.domain_name => {
      name   = d.resource_record_name
      record = d.resource_record_value
      type   = d.resource_record_type
    }
  }
  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = var.route53_zone_id
}




