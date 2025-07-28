#!/bin/bash
# AWS ECS Fargate Deployment Script for Radio Sahoo
# Run this after creating ECR repository manually

set -e

# Configuration
AWS_REGION="ap-southeast-2"
AWS_ACCOUNT_ID="896820529994"
REPOSITORY_NAME="radio-sahoo"
CLUSTER_NAME="radio-sahoo-cluster"
SERVICE_NAME="radio-sahoo-service"
TASK_FAMILY="radio-sahoo-task"

# ECR Repository URI (update after creating repo)
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}"

echo "🚀 Radio Sahoo AWS ECS Fargate Deployment"
echo "========================================="

# Step 1: Login to ECR
echo "📝 Step 1: Logging into ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URI}

# Step 2: Build Docker image
echo "🔨 Step 2: Building Docker image..."
docker build -t ${REPOSITORY_NAME}:latest .

# Step 3: Tag image for ECR
echo "🏷️  Step 3: Tagging image for ECR..."
docker tag ${REPOSITORY_NAME}:latest ${ECR_URI}:latest

# Step 4: Push image to ECR
echo "📤 Step 4: Pushing image to ECR..."
docker push ${ECR_URI}:latest

# Step 5: Create ECS cluster (if not exists)
echo "🏗️  Step 5: Creating ECS cluster..."
aws ecs create-cluster --cluster-name ${CLUSTER_NAME} --region ${AWS_REGION} || echo "Cluster may already exist"

# Step 6: Register task definition
echo "📋 Step 6: Registering ECS task definition..."
aws ecs register-task-definition --cli-input-json file://aws-task-definition.json --region ${AWS_REGION}

# Step 7: Create or update ECS service
echo "⚙️  Step 7: Creating ECS service..."
aws ecs create-service \
  --cluster ${CLUSTER_NAME} \
  --service-name ${SERVICE_NAME} \
  --task-definition ${TASK_FAMILY}:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-255aab6d,subnet-59dd1a3f,subnet-5391e70b],securityGroups=[sg-ffe07db6],assignPublicIp=ENABLED}" \
  --region ${AWS_REGION} || echo "Service may already exist - updating instead"

echo "✅ Deployment script completed!"
echo "📱 Check AWS Console ECS service for deployment status"
echo "🌐 Service URL will be available after load balancer setup"