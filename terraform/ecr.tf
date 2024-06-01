# ecr.tf
resource "aws_ecr_repository" "chatbot" {
  name = "${var.prefix}chatbot-app"
}

resource "aws_ecr_repository" "sentiment_analysis" {
  name = "${var.prefix}sentiment-analysis-api"
}