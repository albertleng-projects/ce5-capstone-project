#!/bin/bash

# TODOs:
# 1. Replace the account id with environment variable
# 2. Replace the region with environment variable

# Build the Docker images
sudo docker build -t chatbot-app ./chatbot
sudo docker build -t sentiment-analysis-api ./api

# Authenticate Docker to the ECR registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 255945442255.dkr.ecr.us-east-1.amazonaws.com

# Tag the Docker images
docker tag chatbot-app:latest 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr:chatbot-app-latest
docker tag sentiment-analysis-api:latest 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr:sentiment-analysis-api-latest

# Push the Docker images
docker push 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr:chatbot-app-latest
docker push 255945442255.dkr.ecr.us-east-1.amazonaws.com/ce5-group6-ecr:sentiment-analysis-api-latest