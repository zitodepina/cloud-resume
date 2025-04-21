#VARIABLES

#variables for AWS access key and secret key
variable "aws_access_key" {}
variable "aws_secret_key" {}

#variable for region
variable "region" {
    default = "us-east-1"
}

#the environment
variable "environment" {
  default = "prod"
}

#variable for database to use
variable "database" {
    default = "aws_cloud-resume"
}
#variable for s3 bucket to use
variable "bucket_name" {
    default = "adalbertodepina-12345"
}

#domain name
variable "domain_name" {
    default = "adepina.com"
}

#route53 zone Id
variable "route53_zone_id"{
    default = "Z0748855167ZVE7XK6EQX"
}

variable "domain_alias"{
     default = "adepina.com"
}