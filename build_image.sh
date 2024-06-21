#!/bin/bash

export AWS_PROFILE=varicon-prakash-dev
export ECR_REGION=us-east-2
export ECR_IMAGE=$1
export BUILD_NUMBER=latest
echo "ECR IMAGE: $ECR_IMAGE"

aws ecr get-login-password --region $ECR_REGION | docker login --username AWS --password-stdin ${ECR_IMAGE}
docker build -t $ECR_IMAGE:$BUILD_NUMBER .
docker push $ECR_IMAGE:$BUILD_NUMBER
