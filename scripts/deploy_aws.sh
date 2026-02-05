#!/bin/bash

set -e

echo "Deploying Sales Analytics Pipeline to AWS..."

AWS_REGION="${AWS_REGION:-us-east-1}"
CLUSTER_NAME="sales-analytics-cluster"
SERVICE_NAME="sales-analytics-service"

echo "Building Docker images..."
docker build -t sales-api:latest -f docker/Dockerfile.api .
docker build -t sales-producer:latest -f docker/Dockerfile.producer .
docker build -t sales-dashboard:latest -f docker/Dockerfile.dashboard .

ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

echo "Logging into ECR..."
aws ecr get-login-password --region ${AWS_REGION} | \
    docker login --username AWS --password-stdin ${ECR_REGISTRY}

echo "Tagging images..."
docker tag sales-api:latest ${ECR_REGISTRY}/sales-api:latest
docker tag sales-producer:latest ${ECR_REGISTRY}/sales-producer:latest
docker tag sales-dashboard:latest ${ECR_REGISTRY}/sales-dashboard:latest

echo "Pushing images to ECR..."
docker push ${ECR_REGISTRY}/sales-api:latest
docker push ${ECR_REGISTRY}/sales-producer:latest
docker push ${ECR_REGISTRY}/sales-dashboard:latest

echo "Creating ECS cluster..."
aws ecs create-cluster --cluster-name ${CLUSTER_NAME} --region ${AWS_REGION} || true

echo "Setting up RDS PostgreSQL..."
aws rds create-db-instance \
    --db-instance-identifier sales-analytics-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username postgres \
    --master-user-password ${DB_PASSWORD} \
    --allocated-storage 20 \
    --region ${AWS_REGION} || true

echo "Setting up ElastiCache Redis..."
aws elasticache create-cache-cluster \
    --cache-cluster-id sales-analytics-cache \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1 \
    --region ${AWS_REGION} || true

echo "Setting up MSK Kafka..."
aws kafka create-cluster \
    --cluster-name sales-analytics-kafka \
    --broker-node-group-info file://kafka-config.json \
    --kafka-version 2.8.1 \
    --number-of-broker-nodes 2 \
    --region ${AWS_REGION} || true

echo "Registering ECS task definitions..."
aws ecs register-task-definition \
    --cli-input-json file://ecs-task-definition.json \
    --region ${AWS_REGION}

echo "Creating ECS service..."
aws ecs create-service \
    --cluster ${CLUSTER_NAME} \
    --service-name ${SERVICE_NAME} \
    --task-definition sales-analytics-task \
    --desired-count 1 \
    --launch-type FARGATE \
    --region ${AWS_REGION} || true

echo "Deployment complete!"
echo ""
echo "Resources created:"
echo "- ECS Cluster: ${CLUSTER_NAME}"
echo "- RDS Database: sales-analytics-db"
echo "- ElastiCache: sales-analytics-cache"
echo "- MSK Kafka: sales-analytics-kafka"