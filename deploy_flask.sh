#!/usr/bin/env bash
set -e

echo "📦 Building Flask Docker image..."
cd /home/ec2-user/ml-server
docker build -t wehago_flask:latest .

echo "🛑 Stopping old container (if any)..."
docker stop wehago_flask 2>/dev/null || true
docker rm   wehago_flask 2>/dev/null || true

echo "🚀 Starting new Flask container..."
docker run -d \
  --name wehago_flask \
  --restart unless-stopped \
  -p 5000:5000 \
  wehago_flask:latest

echo "✅ Flask deployed on port 5000"
