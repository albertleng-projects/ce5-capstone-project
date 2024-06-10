#!/bin/bash
# TODO: Add environment variable for account-id

ENVIRONMENT=$(grep 'environment:' ./helm/values.yaml | awk '{print $2}')
VERSION=$(grep 'version:' ./helm/values.yaml | awk '{print $2}')
ACCOUNT_ID=$(grep 'account_id:' ./helm/values.yaml | awk '{print $2}')

export ENVIRONMENT
export VERSION
export ACCOUNT_ID

echo "export ENVIRONMENT=${ENVIRONMENT}"
echo "export VERSION=${VERSION}"
echo "export ACCOUNT_ID=${ACCOUNT_ID}"

# Build and push Docker images
sudo docker build -t chatbot-"$ENVIRONMENT":"$VERSION" ./chatbot
sudo docker build -t sentiment-analysis-api-"$ENVIRONMENT":"$VERSION" ./api

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin "$ACCOUNT_ID".dkr.ecr.us-east-1.amazonaws.com

docker tag chatbot-"$ENVIRONMENT":"$VERSION" "$ACCOUNT_ID".dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-chatbot-"$ENVIRONMENT":"$VERSION"
docker tag sentiment-analysis-api-"$ENVIRONMENT":"$VERSION" "$ACCOUNT_ID".dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-api-"$ENVIRONMENT":"$VERSION"

docker push "$ACCOUNT_ID".dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-chatbot-"$ENVIRONMENT":"$VERSION"
docker push "$ACCOUNT_ID".dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-api-"$ENVIRONMENT":"$VERSION"
