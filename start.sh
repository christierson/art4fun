#!/bin/bash

cd "$(dirname "$(realpath "$0")")"

docker compose up -d

# Wait for port 3000 to be ready (up to 30 seconds)
echo "⏳ Waiting for frontend to start..."
for i in {1..30}; do
    if curl -s http://localhost:5173 >/dev/null; then
        echo "✅ Frontend is ready!"
        break
    fi
    sleep 1
done

# Open browser
xdg-open http://localhost:5173