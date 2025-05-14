#VARIABLES

#variables for AWS access key and secret key
variable "aws_access_key" {}
variable "aws_secret_key" {}

#variable for region
variable "region" {
    description = "AWS Region where resources will be deployed"
    type        = string
}

#the environment
variable "environment" {
    description = "AWS Environment"
    type        = string
}

#variable for database to use
variable "database" {
    description = "AWS Database to use"
    type        = string
}
#variable for s3 bucket to use
variable "bucket_name" {
    description = "AWS S3 Bucket Name"
    type        = string
}

#domain name
variable "domain_name" {
    description = "Domain Name"
    type        = string
}

#cloudfront zone Id
variable "CloudFront_zone_id"{
    description = "set value for cloudfront distribution https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-aliastarget.html"
    type        = string
}
    

#alias
variable "domain_alias"{
    description = "Alias Name"
    type        = string
}