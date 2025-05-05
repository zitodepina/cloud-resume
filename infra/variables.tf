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

###TO DELETE############
#route53 zone Id
variable "route53_zone_id"{
    default = "Z0748855167ZVE7XK6EQX"
}


#cloudfront zone Id
variable "CloudFront_zone_id"{
    default = "Z2FDTNDATAQYW2" // set value for cloudfront distribution https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-aliastarget.html
}

#alias
variable "domain_alias"{
     default = "adepina.com"
}