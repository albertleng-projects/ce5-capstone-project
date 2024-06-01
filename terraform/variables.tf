# variables.tf
# TODO:
# 1. Define the variables that will be used in the main.tf file
# 2. Find out how to use and set the variables in the main.tf file



variable "prefix" {
  type        = string
  default     = "ce5-group6-"
  description = "Prefix for resources"
}

variable "aws_account_id" {
  type        = string
  description = "AWS Account ID"
}