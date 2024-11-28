#!/bin/bash

# Ensure script exits on error
set -e

echo "Starting..."

# Navigate to the project root directory
cd ../../

# Start Minikube with Docker driver
minikube start -p bslab --driver=docker

# Set Docker environment to use Minikube's Docker daemon
eval $(minikube -p bslab docker-env)

# Build Docker images inside Minikube's Docker daemon
echo "Building Docker images..."
docker build -t nuxt-frontend:latest ./frontend
docker build -t express-backend:latest ./backend
docker build -t transcriber-service:latest ./transcriber
docker build -t narrator-service:latest ./narrator

# Create namespace if it doesn't exist
kubectl get namespace bslab >/dev/null 2>&1 || kubectl create namespace bslab

# Apply Kubernetes manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f deployment/manifests -n bslab

echo "Started successfully!"

# kubectl get all -n bslab

minikube service frontend-service -p bslab -n bslab
