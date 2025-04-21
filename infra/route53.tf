resource "aws_route53domains_domain" "route53-domain" {
  domain_name = var.domain_name
  auto_renew  = true

  admin_contact {
    address_line_1    = "335 Rockland Street"
    city              = "Brockton"
    contact_type      = "COMPANY"
    country_code      = "US"
    email             = "a_depina@comcast.net"
    fax               = "+1.5088023694"
    first_name        = "Adalberto"
    last_name         = "DePina"
    organization_name = "HashiCorp"
    phone_number      = "+1.5088023694"
    state             = "MA"
    zip_code          = "02301"
  }

  registrant_contact {
    address_line_1    = "335 Rockland Street"
    city              = "Brockton"
    contact_type      = "COMPANY"
    country_code      = "US"
    email             = "a_depina@comcast.net"
    fax               = "+1.5088023694"
    first_name        = "Adalberto"
    last_name         = "DePina"
    organization_name = "HashiCorp"
    phone_number      = "+1.5088023694"
    state             = "MA"
    zip_code          = "02301"
  }

  tech_contact {
    address_line_1    = "335 Rockland Street"
    city              = "Brockton"
    contact_type      = "COMPANY"
    country_code      = "US"
    email             = "a_depina@comcast.net"
    fax               = "+1.5088023694"
    first_name        = "Adalberto"
    last_name         = "DePina"
    organization_name = "HashiCorp"
    phone_number      = "+1.5088023694"
    state             = "MA"
    zip_code          = "02301"
  }

  /*lifecycle {
       prevent_destroy = true
     }
     */
}

/*
resource "aws_route53_zone" "route53_zone" {
  name = var.domain_name
}*/
