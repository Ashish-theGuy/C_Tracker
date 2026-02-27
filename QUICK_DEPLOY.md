# Quick Deployment to Google Cloud Run

## Prerequisites Checklist

- [ ] Google Cloud account with billing enabled
- [ ] Google Cloud SDK installed (`gcloud`)
- [ ] Project created in Google Cloud Console
- [ ] Project configured

## 3-Step Deployment

### Step 1: Setup (One-time)

```bash
# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com
```

### Step 2: Deploy

**Option A: Using deploy script (Linux/Mac)**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Option B: Manual deployment**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection

gcloud run deploy kerala-crowd-detection \
  --image gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300
```

### Step 3: Get Your URL

```bash
gcloud run services describe kerala-crowd-detection \
  --region us-central1 \
  --format 'value(status.url)'
```

## Cost Estimate

- **Free tier**: 2 million requests/month
- **Low usage** (10K requests): ~$5-10/month
- **Medium usage** (100K requests): ~$20-30/month

## Important Notes

1. **Videos**: Currently stored in container (ephemeral)
   - Consider Cloud Storage for production

2. **Data**: JSON files are lost on restart
   - Consider Cloud Firestore for persistence

3. **Cold starts**: First request may take 5-10 seconds
   - Set min instances to 1 to avoid

4. **Memory**: Needs at least 2Gi for YOLO model

## Troubleshooting

**Build fails?**
```bash
gcloud builds list
gcloud builds log BUILD_ID
```

**Service not working?**
```bash
gcloud run services logs read kerala-crowd-detection --region us-central1
```

## Next Steps

- [ ] Set up Cloud Storage for videos
- [ ] Use Cloud Firestore for data
- [ ] Configure custom domain (optional)
- [ ] Set up monitoring



