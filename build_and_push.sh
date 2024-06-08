#!/bin/bash

# TODOs:
# 1. Replace the account id with environment variable
# 2. Replace the region with environment variable
# 3. Add environment and version to the Docker images, for example: chatbot-`staging`:`1.0.0` (using environment variables)

# shellcheck disable=SC2269
ENVIRONMENT=$ENVIRONMENT
VERSION=$VERSION

# Build the Docker images
sudo docker build -t chatbot-"$ENVIRONMENT":"$VERSION" ./chatbot
sudo docker build -t sentiment-analysis-api-"$ENVIRONMENT":"$VERSION" ./api

# Authenticate Docker to the ECR registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 255945442255.dkr.ecr.us-east-1.amazonaws.com

# Tag the Docker images
docker tag chatbot-"$ENVIRONMENT":"$VERSION" 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-chatbot-"$ENVIRONMENT":"$VERSION"
# shellcheck disable=SC2086
docker tag sentiment-analysis-api-"$ENVIRONMENT":"$VERSION" 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-api-$ENVIRONMENT:$VERSION

# Push the Docker images
docker push 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-chatbot-"$ENVIRONMENT":"$VERSION"
docker push 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr-api-"$ENVIRONMENT":"$VERSION"