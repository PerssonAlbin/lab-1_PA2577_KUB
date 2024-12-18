#!/bin/bash

# Ensure script exits on error
set -e

echo "Stopping..."

# Navigate to the project root directory
cd ../../

# Switch back to the default Docker environment
eval $(minikube docker-env -u)

# Delete Kubernetes resources
echo "Deleting Kubernetes resources..."
kubectl delete -f deployment/manifests/deployments -n bslab --ignore-not-found
kubectl delete -f deployment/manifests/services -n bslab --ignore-not-found

# Stop Minikube
minikube stop -p bslab

echo "Stopped successfully!"
