# https://learnk8s.io/terraform-eks

provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "ce5-group6-tf-state-bucket"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}


resource "aws_s3_bucket_versioning" "versioning" {
  bucket = "ce5-group6-tf-state-bucket"
  versioning_configuration {
    status = "Enabled"
  }
}


data "aws_availability_zones" "available" {}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}

locals {
  cluster_name = "ce5-group6-eks-cluster"
}

provider "kubernetes" {
  host  = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token = data.aws_eks_cluster_auth.cluster.token
}

module "eks-kubeconfig" {
  source  = "hyperbadger/eks-kubeconfig/aws"
  version = "1.0.0"

  depends_on = [module.eks]
  cluster_id = module.eks.cluster_id
}

resource "local_file" "kubeconfig" {
  content  = module.eks-kubeconfig.kubeconfig
  filename = "kubeconfig_${local.cluster_name}"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.1"

  name = "ce5-group6-vpc"
  cidr = "172.16.0.0/16"
  azs  = data.aws_availability_zones.available.names

  #   https://github.com/hashicorp/terraform-provider-aws/issues/23488
  #   TODO: Fix
  #   module.vpc.aws_subnet.public[0]: Still destroying... [id=subnet-0ea022eb6028a9427, 20m0s elapsed]
  #module.vpc.aws_internet_gateway.this[0]: Still destroying... [id=igw-0c7d70ca564a8f6d7, 20m0s elapsed]
  #╷
  #│ Error: deleting EC2 Subnet (subnet-0ea022eb6028a9427): DependencyViolation: The subnet 'subnet-0ea022eb6028a9427' has dependencies and cannot be deleted.
  #│       status code: 400, request id: 799c4c09-d035-4342-98e9-d7cbe44b2d1f
  #│
  #│
  #╵
  #╷
  #│ Error: deleting EC2 Subnet (subnet-04e04164ef5963f1e): DependencyViolation: The subnet 'subnet-04e04164ef5963f1e' has dependencies and cannot be deleted.
  #│       status code: 400, request id: 60c53453-c38a-4348-8ee8-ed4b6679fac4
  #│
  #│
  #╵
  #╷
  #│ Error: deleting EC2 Internet Gateway (igw-0c7d70ca564a8f6d7): detaching EC2 Internet Gateway (igw-0c7d70ca564a8f6d7) from VPC (vpc-053c9eaae00d398dc): DependencyViolation: Network vpc-053c9eaae00d398dc has some mapped public address(es). Please unmap those public address(es) before detaching the gateway.
  #│       status code: 400, request id: c640edeb-4b6a-4635-909c-c930cf1645cf
  #│
  #│
  #╵

  private_subnets = ["172.16.1.0/24", "172.16.2.0/24", "172.16.3.0/24"]
  public_subnets = ["172.16.4.0/24", "172.16.5.0/24", "172.16.6.0/24"]
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.30.3"

  cluster_name    = local.cluster_name
  cluster_version = "1.30"
  subnet_ids      = module.vpc.private_subnets

  vpc_id = module.vpc.vpc_id

  eks_managed_node_groups = {
    ce5-group6-node_group = {
      desired_capacity = 1
      max_capacity     = 5
      min_capacity     = 1

      instance_type = "t3.medium"
      #       TODO: Use bastion host instead
      #       public_ip     = true
    }
  }
}