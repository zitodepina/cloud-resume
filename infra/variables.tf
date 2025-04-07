#VARIABLES

#variables for AWS access key and secret key
variable "aws_access_key" {}
variable "aws_secret_key" {}

#variable for region
variable "region" {
    default = "us-east-1"
}

#variable for database to use
variable "database" {
    default = "aws_cloud-resume"
}

#variable for user Id
variable "id" {
    default = "resume-adepina.com"
}

