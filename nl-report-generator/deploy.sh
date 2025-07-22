#!/bin/bash

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
export CLOUDRUN_SERVICE_IMAGE_NAME=us-central1-docker.pkg.dev/$PROJECT_ID/$CLOUDRUN_SERVICE_NAME/$CLOUDRUN_SERVICE_NAME:latest

# Setup
gcloud config set project $PROJECT_ID
gcloud auth application-default set-quota-project $PROJECT_ID

# Build image
gcloud builds submit . --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy image
gcloud run deploy $CLOUDRUN_SERVICE_NAME \
    --image $CLOUDRUN_SERVICE_IMAGE_NAME \
    --region us-central1 \
    --port 8501 --allow-unauthenticated
    --set-env-vars BUCKET_NAME=$BUCKET_NAME,PROJECT_ID=$PROJECT_ID,REGION=$REGION,DB_USER=$DB_USER,DB_PASS=$DB_PASS,DB_HOST=$DB_HOST,DB_NAME=$DB_NAME

echo "Deployment completed. Access your service via the Cloud Run console."





