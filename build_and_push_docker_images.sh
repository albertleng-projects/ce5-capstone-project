#!/bin/bash
# TODO: Add environment variable for account-id

ENVIRONMENT=$(grep 'environment:' ./helm/values.yaml | awk '{print $2}')
VERSION=$(grep 'version:' ./helm/values.yaml | awk '{print $2}')

export ENVIRONMENT
export VERSION

echo "export ENVIRONMENT=${ENVIRONMENT}"
echo "export VERSION=${VERSION}"

# Build and push Docker images
sudo docker build -t chatbot-"$ENVIRONMENT":"$VERSION" ./chatbot
sudo docker build -t sentiment-analysis-api-"$ENVIRONMENT":"$VERSION" ./api

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 255945442255.dkr.ecr.us-east-1.amazonaws.com

docker tag chatbot-"$ENVIRONMENT":"$VERSION" 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-chatbot-"$ENVIRONMENT":"$VERSION"
docker tag sentiment-analysis-api-"$ENVIRONMENT":"$VERSION" 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-api-"$ENVIRONMENT":"$VERSION"

docker push 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-chatbot-"$ENVIRONMENT":"$VERSION"
docker push 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-api-"$ENVIRONMENT":"$VERSION"
