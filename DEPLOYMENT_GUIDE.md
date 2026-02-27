# Google Cloud Run Deployment Guide

This guide covers deploying your Kerala Cities Crowd Detection application to Google Cloud Run.

## Deployment Options

### Option 1: Single Service (Recommended for MVP)
- **Backend + Frontend** in one container
- Backend serves frontend static files
- Simpler deployment, single URL
- **Cost**: Lower (one service)

### Option 2: Separate Services
- **Backend** as Cloud Run service
- **Frontend** as Cloud Storage + Cloud CDN or separate service
- More scalable, better separation
- **Cost**: Higher (two services)

### Option 3: Hybrid
- **Backend** on Cloud Run
- **Frontend** on Firebase Hosting or Netlify
- Best performance, separate scaling
- **Cost**: Medium

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **Google Cloud SDK** installed: https://cloud.google.com/sdk/docs/install
3. **Docker** installed (for local testing)
4. **Project ID** created in Google Cloud Console

## Quick Start (Option 1 - Single Service)

### Step 1: Setup Google Cloud

```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Build and Deploy

```bash
# Build the Docker image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection

# Deploy to Cloud Run
gcloud run deploy kerala-crowd-detection \
  --image gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10
```

### Step 3: Get Your URL

After deployment, you'll get a URL like:
```
https://kerala-crowd-detection-xxxxx-uc.a.run.app
```

## Environment Variables

No required environment variables. Optional env vars can be set:

```bash
gcloud run services update kerala-crowd-detection \
  --update-env-vars KEY=value \
  --region us-central1
```

## Storage Considerations

### Current Setup (JSON files)
- Data stored in `data/locations_data.json`
- Videos stored locally
- **Issue**: Cloud Run is stateless - files are lost on restart

### Solutions:

#### Option A: Cloud Storage (Recommended)
1. Upload videos to Cloud Storage bucket
2. Update code to read from Cloud Storage
3. Use Cloud Firestore or Cloud SQL for data

#### Option B: Persistent Volume (Cloud Run for Anthos)
- More complex setup
- Requires GKE cluster

#### Option C: Pre-process and embed data
- Process videos before deployment
- Embed data in container or use environment variables
- Good for demo/MVP

## Configuration Files

### Dockerfile
- Already created
- Uses Python 3.11
- Includes all dependencies
- Uses Gunicorn for production

### cloudbuild.yaml
- Automated build and deploy

## Deployment Steps

### Manual Deployment

```bash
# 1. Build image
docker build -t kerala-crowd-detection .

# 2. Test locally
docker run -p 8080:8080 -e PORT=8080 kerala-crowd-detection

# 3. Tag for GCR
docker tag kerala-crowd-detection gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection

# 4. Push to GCR
docker push gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection

# 5. Deploy to Cloud Run
gcloud run deploy kerala-crowd-detection \
  --image gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Automated Deployment (CI/CD)

```bash
# Using Cloud Build
gcloud builds submit --config cloudbuild.yaml
```

## Cost Estimation

### Cloud Run Pricing (us-central1)
- **CPU**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GiB-second
- **Requests**: $0.40 per million requests
- **Free tier**: 2 million requests/month

### Example Monthly Cost (Low traffic)
- 2 vCPU, 2GB RAM
- 10,000 requests/month
- ~$5-10/month

### Example Monthly Cost (Medium traffic)
- 2 vCPU, 2GB RAM
- 100,000 requests/month
- ~$20-30/month

## Important Notes

1. **Cold Starts**: First request may be slow (5-10s)
   - Solution: Set min instances to 1

2. **Memory**: YOLO model needs ~1-2GB RAM
   - Set memory to at least 2Gi

3. **Timeout**: Video processing can take time
   - Set timeout to 300s (max)

4. **Videos**: Large video files
   - Consider Cloud Storage
   - Or pre-process before deployment

5. **Data Persistence**: JSON files are ephemeral
   - Use Cloud Firestore or Cloud SQL

## Troubleshooting

### Build fails
```bash
# Check logs
gcloud builds list
gcloud builds log BUILD_ID
```

### Deployment fails
```bash
# Check service logs
gcloud run services logs read kerala-crowd-detection --region us-central1
```

### Container crashes
```bash
# Check container logs
gcloud run services describe kerala-crowd-detection --region us-central1
```

## Next Steps

1. **Set up Cloud Storage** for videos
2. **Use Cloud Firestore** for data persistence
3. **Enable Cloud CDN** for better performance
4. **Set up monitoring** with Cloud Monitoring
5. **Configure custom domain** (optional)

## Support

- [Cloud Run Docs](https://cloud.google.com/run/docs)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)



