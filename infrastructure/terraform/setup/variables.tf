variable "aws_profile" {
  description = "AWS profile (./aws/credentials) used to authenticate requests"
  default     = "ckl-stellar-tf"
}
variable "region" {
  description = "Region to deploy resources"
  default     = "us-east-2"
}
variable "project_name" {
  description = "Project name used to build resources"
  default     = "stellar-tf"
}
