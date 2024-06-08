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


module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.30.3"

  cluster_name    = local.cluster_name
  cluster_version = "1.30"
  subnet_ids = [
    "subnet-0aa24ba6afc315287", "subnet-0df58e4c0dd0fab5f",
    "subnet-0334d23b810a18cb0"
  ]

  vpc_id = "vpc-0b1601b5d13b56128"

  eks_managed_node_groups = {
    ce5-group6-node_group = {
      desired_capacity = 1
      max_capacity     = 5
      min_capacity     = 1

      instance_type = "t3.medium"
    }
  }
}