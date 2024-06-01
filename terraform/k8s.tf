terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "~> 1.9"
    }
  }
}

provider "kubernetes" {
  host             = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  token            = module.eks.cluster_iam_role_arn
  load_config_file = false
}

resource "kubernetes_deployment" "chatbot" {
  metadata {
    name = "chatbot"
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        App = "chatbot"
      }
    }

    template {
      metadata {
        labels = {
          App = "chatbot"
        }
      }

      spec {
        container {
          image = "your-account-id.dkr.ecr.region.amazonaws.com/chatbot-app:latest"
          name  = "chatbot"
        }
      }
    }
  }
}

resource "kubernetes_deployment" "sentiment_analysis" {
  metadata {
    name = "sentiment-analysis"
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        App = "sentiment-analysis"
      }
    }

    template {
      metadata {
        labels = {
          App = "sentiment-analysis"
        }
      }

      spec {
        container {
          image = "your-account-id.dkr.ecr.region.amazonaws.com/sentiment-analysis-api:latest"
          name  = "sentiment-analysis"
        }
      }
    }
  }
}