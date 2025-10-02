#!/bin/bash
set -e

echo "🔨 Starting full build..."

# Ensure you're in the project root
cd "$(dirname "$0")"

# Step 1: Build frontend using Docker
echo "📦 Building frontend..."
docker compose run --rm frontend-build

# Step 2: Build backend executable using Docker
echo "🐍 Building backend binary..."
docker compose run --rm backend-build

# Step 3: Ensure executable permission (esp. on Linux)
chmod +x backend/dist/main

# Step 4: Run Electron builder
echo "⚡ Running Electron builder..."
npm run build:electron

echo "✅ Build complete! Check the dist/ folder for your installer."