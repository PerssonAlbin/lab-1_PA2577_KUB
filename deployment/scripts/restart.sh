#!/bin/bash

# Ensure script exits on error
set -e

echo "Restarting..."

# Navigate to the scripts directory
cd "$(dirname "$0")"

# Stop the project
./stop.sh

# Start the project
./start.sh

echo "Restarted successfully!"
