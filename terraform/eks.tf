# TODOs:
# 1. Rename `aws_vpc` and their tags
# 2. Rename `aws_subnet` and their tags
# 3. Rename `aws_subnets` and their tags

resource "aws_vpc" "my_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "my_vpc"
  }
}

resource "aws_subnet" "subnet_1" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "subnet_1"
  }
}

resource "aws_subnet" "subnet_2" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "subnet_2"
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.13.0"

  cluster_name    = "${var.prefix}eks-cluster"
  cluster_version = "1.29"
  subnet_ids = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id]
  vpc_id = aws_vpc.my_vpc.id

  #   TODO: Refer to https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest
  eks_managed_node_groups = {
    eks_nodes = {
      desired_capacity = 2
      max_capacity     = 10
      min_capacity     = 1

      instance_type = "t2.micro"
      #       TODO: Create a key pair for group 6, naming `ce5-group6-key`
      key_name = "simple-instance-1-key"
    }
  }

  #   TODO: Add tags to the EKS cluster and other resources
  #   tags = {
  #     Environment = "dev"
  #     Terraform   = "true"
  #   }
}