#!/bin/bash

PROJECT_ID=deft-clarity-461011-c7
REGION=us-central1
SERVICE_NAME=doc-comparison-qc

gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 3600 \
  --port 8501
