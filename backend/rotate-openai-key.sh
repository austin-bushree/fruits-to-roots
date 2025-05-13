#!/bin/bash

# Exit on error
set -e

PROJECT_ID="fruits-to-roots"
REGION="us-west2"
SERVICE_NAME="fruits-backend"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
SECRET_NAME="OPENAI_API_KEY"

echo "🔐 Enter your new OpenAI API key (it will not be shown):"
read -s NEW_KEY

# Save to temp file and upload to Secret Manager
echo -n "$NEW_KEY" > .tmp_openai_key.txt

echo "🔁 Uploading new secret version to Secret Manager..."
gcloud secrets versions add "$SECRET_NAME" \
  --data-file=.tmp_openai_key.txt

rm .tmp_openai_key.txt

echo "🚀 Re-deploying Cloud Run to apply latest secret version..."
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-secrets=OPENAI_API_KEY=OPENAI_API_KEY:latest

echo "✅ Secret rotated and service redeployed!"
