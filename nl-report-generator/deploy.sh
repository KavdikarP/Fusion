#!/bin/bash
set -e

#export CLOUDRUN_SERVICE_IMAGE_NAME=asia-south1-docker.pkg.dev/$PROJECT_ID/$CLOUDRUN_SERVICE_NAME/$CLOUDRUN_SERVICE_NAME:latest
export REGION=us-central1
export DB_USER=report_user
export DB_PASS=test123
export DB_HOST=35.244.42.223
export DB_NAME=reporting_db
export BUCKET_NAME=cxo-prism

# Variables
export PROJECT_ID=deft-clarity-461011-c7
export CLOUDRUN_SERVICE_NAME=cxo-prism
#export CLOUDRUN_SERVICE_IMAGE_NAME=us-central1-docker.pkg.dev/$PROJECT_ID/$CLOUDRUN_SERVICE_NAME/$CLOUDRUN_SERVICE_NAME:latest

# Build Docker image and push to Google Container Registry
gcloud builds submit . \
  --tag gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --logging=CLOUD_LOGGING_ONLY

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  #--set-env-vars BUCKET_NAME=your-gcs-bucket,PROJECT_ID=$PROJECT_ID,REGION=$REGION,DB_USER=postgres,DB_PASS=your-db-password,DB_HOST=your-cloudsql-public-ip,DB_NAME=cxo_prism

echo "Deployment completed. Access your service via the Cloud Run console."


