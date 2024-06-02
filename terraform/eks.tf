# TODOs:
# 1. Rename `aws_vpc` and their tags
# 2. Rename `aws_subnet` and their tags
# 3. Rename `aws_subnets` and their tags

resource "aws_vpc" "ce5-group6-vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "ce5-group6-vpc"
  }
}

resource "aws_subnet" "ce5-group6-subnet-1" {
  vpc_id            = aws_vpc.ce5-group6-vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "ce5-group6-subnet-1"
  }
}

resource "aws_subnet" "ce5-group6-subnet-2" {
  vpc_id            = aws_vpc.ce5-group6-vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "ce5-group6-subnet-2"
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.13.0"

  cluster_name    = "${var.prefix}eks-cluster"
#   TODO: Replace all instances of "1.29" with "1.30"
  cluster_version = "1.30"
  subnet_ids = [
    aws_subnet.ce5-group6-subnet-1.id, aws_subnet.ce5-group6-subnet-2.id
  ]
  vpc_id = aws_vpc.ce5-group6-vpc.id

  #   TODO: Refer to https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest
#    In the eks.tf file, the eks_managed_node_groups block defines a group of
  #    EC2 instances that will be part of the EKS cluster. These instances will
  #    serve as the worker nodes for the Kubernetes cluster.

  # TODO: add ssh access?
  eks_managed_node_groups = {
    eks_nodes = {
      desired_capacity = 2
#       TODO: max_capacity should be 10? Or lower?
      max_capacity     = 10
      min_capacity     = 1

      instance_type = "t2.micro"
      key_name = "ce5-group6-key"
    }
  }

#     TODO:
#   1. Use Environment "staging" and "main"
    tags = {
      Environment = "dev"
      Terraform   = "true"
    }
}