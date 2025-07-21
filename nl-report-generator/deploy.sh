#!/bin/bash

# Exit on error
set -e

PROJECT_ID=deft-clarity-461011-c7
REGION=asia-south1
SERVICE_NAME=cxo-prism
DB_USER=report_user
DB_PASS=test123
DB_HOST=35.244.42.223
DB_NAME=reporting_db

# Build Docker image and push to Google Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars BUCKET_NAME=your-gcs-bucket,PROJECT_ID=$PROJECT_ID,REGION=$REGION,DB_USER=$DB_USER,DB_PASS=$DB_PASS,DB_HOST=$DB_HOST,DB_NAME=$DB_NAME

echo "Deployment completed. Access your service via the Cloud Run console."
