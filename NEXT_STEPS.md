# Next Steps to Deploy Your Application

## Step-by-Step Deployment Guide

### Step 1: Prepare Google Cloud (5 minutes)

1. **Create Google Cloud Account** (if you don't have one)
   - Go to: https://cloud.google.com/
   - Sign up (free trial with $300 credit)

2. **Create a Project**
   - Go to: https://console.cloud.google.com/
   - Click "Create Project"
   - Name it: `kerala-crowd-detection` (or your choice)
   - Note your Project ID

3. **Enable Billing**
   - Go to Billing in console
   - Link a payment method (won't charge unless you exceed free tier)

### Step 2: Install Google Cloud SDK (10 minutes)

**Windows:**
```powershell
# Download and install from:
# https://cloud.google.com/sdk/docs/install

# Or use PowerShell:
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

**Linux/Mac:**
```bash
# Download script
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### Step 3: Login and Setup (2 minutes)

```bash
# Login to Google Cloud
gcloud auth login

# Set your project (replace YOUR_PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID

# Verify
gcloud config get-value project
```

### Step 4: Deploy! (5-10 minutes)

**Windows:**
```powershell
# Run the deployment script
.\deploy.ps1

# Or manually:
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection
gcloud run deploy kerala-crowd-detection --image gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection --platform managed --region us-central1 --allow-unauthenticated --memory 2Gi --cpu 2
```

**Linux/Mac:**
```bash
# Make script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### Step 5: Configure Environment Variables (Optional)

```bash
# No required env vars - optional: gcloud run services update kerala-crowd-detection --update-env-vars KEY=value --region us-central1
```

### Step 6: Get Your URL (1 minute)

```bash
# Get the service URL
gcloud run services describe kerala-crowd-detection \
  --region us-central1 \
  --format 'value(status.url)'
```

You'll get a URL like: `https://kerala-crowd-detection-xxxxx-uc.a.run.app`

### Step 7: Test Your Deployment

1. Open the URL in your browser
2. Test city queries: "Should I visit Kochi?" or "Is Munnar crowded?"

## Quick Checklist

- [ ] Google Cloud account created
- [ ] Project created
- [ ] Billing enabled
- [ ] Google Cloud SDK installed
- [ ] Logged in with `gcloud auth login`
- [ ] Project set with `gcloud config set project`
- [ ] Deployment script run (or manual deployment)
- [ ] Application tested
- [ ] Service URL obtained
- [ ] Application tested

## Troubleshooting

**"Project not found"**
- Make sure you created the project in Google Cloud Console
- Verify with: `gcloud projects list`

**"Permission denied"**
- Make sure billing is enabled
- Check you're logged in: `gcloud auth list`

**"Build failed"**
- Check Dockerfile is correct
- Verify all files are in place
- Check logs: `gcloud builds list`

**"Service not responding"**
- Check service logs: `gcloud run services logs read kerala-crowd-detection --region us-central1`
- Verify environment variables are set
- Check memory is set to at least 2Gi

## What Happens After Deployment?

1. **First Request**: May take 5-10 seconds (cold start)
2. **Subsequent Requests**: Fast (< 1 second)
3. **Scaling**: Automatically scales based on traffic
4. **Costs**: Only pay for what you use

## Optional: Improve Deployment

1. **Set Minimum Instances** (avoid cold starts)
   ```bash
   gcloud run services update kerala-crowd-detection \
     --min-instances 1 \
     --region us-central1
   ```

2. **Use Cloud Storage for Videos**
   - Upload videos to Cloud Storage bucket
   - Update code to read from bucket

3. **Use Cloud Firestore for Data**
   - Replace JSON files with Firestore
   - Persistent data storage

4. **Custom Domain** (optional)
   - Map your domain to Cloud Run service
   - Configure in Cloud Run settings

## Need Help?

- Check `DEPLOYMENT_GUIDE.md` for detailed info
- Google Cloud Run Docs: https://cloud.google.com/run/docs
- Cloud Run Pricing: https://cloud.google.com/run/pricing



