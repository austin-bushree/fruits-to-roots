#!/bin/bash

# Exit on error
set -e

PROJECT_ID="fruits-to-roots"
REGION="us-west2"
SERVICE_NAME="fruits-backend"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🔨 Building Docker image..."
gcloud builds submit --tag "$IMAGE"

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-secrets=OPENAI_API_KEY=OPENAI_API_KEY:latest

echo "✅ Deployment complete!"