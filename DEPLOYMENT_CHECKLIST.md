# Deployment Checklist - Step by Step

## ✅ Pre-Deployment Checklist

### Step 1: Google Cloud Account Setup (5 minutes)

- [ ] **Create Google Cloud Account**
  - Go to: https://cloud.google.com/
  - Sign up (free trial with $300 credit)
  - Verify email if needed

- [ ] **Create a Project**
  - Go to: https://console.cloud.google.com/
  - Click "Select a project" → "New Project"
  - Project name: `kerala-crowd-detection` (or your choice)
  - Note your **Project ID** (e.g., `kerala-crowd-detection-123456`)

- [ ] **Enable Billing**
  - Go to: Billing in Google Cloud Console
  - Link a payment method
  - ⚠️ Won't charge unless you exceed free tier

### Step 2: Install Google Cloud SDK (10 minutes)

**Windows:**
1. Download installer: https://cloud.google.com/sdk/docs/install#windows
2. Run the installer
3. Restart PowerShell/terminal
4. Verify: `gcloud version`

**Or use PowerShell:**
```powershell
# Download installer
$url = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
$output = "$env:TEMP\GoogleCloudSDKInstaller.exe"
Invoke-WebRequest -Uri $url -OutFile $output

# Run installer
Start-Process $output -Wait
```

### Step 3: Login and Configure (2 minutes)

```powershell
# Login to Google Cloud
gcloud auth login

# This will open a browser - sign in with your Google account

# Set your project (replace YOUR_PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID

# Verify
gcloud config get-value project
```

### Step 4: Enable Required APIs (1 minute)

```powershell
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 5: Deploy! (5-10 minutes)

**Option A: Using deployment script (Easiest)**
```powershell
.\deploy.ps1
```

**Option B: Manual deployment**
```powershell
# Set your project ID
$PROJECT_ID = "your-project-id"

# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/kerala-crowd-detection

gcloud run deploy kerala-crowd-detection `
  --image gcr.io/$PROJECT_ID/kerala-crowd-detection `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 2Gi `
  --cpu 2 `
  --timeout 300 `
  --max-instances 10
```

### Step 6: Set Environment Variables (2 minutes)

```powershell
# No required env vars - optional: gcloud run services update kerala-crowd-detection --update-env-vars KEY=value --region us-central1
```

### Step 7: Get Your URL (1 minute)

```powershell
gcloud run services describe kerala-crowd-detection `
  --region us-central1 `
  --format 'value(status.url)'
```

You'll get a URL like: `https://kerala-crowd-detection-xxxxx-uc.a.run.app`

### Step 8: Test Your Deployment

1. Open the URL in your browser
2. Test city query: "Should I visit Kochi?" or "Is Munnar crowded?"
3. Verify crowd data and live YOLO detection displays

## 🎯 Quick Command Reference

```powershell
# Check if gcloud is installed
gcloud version

# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Check current project
gcloud config get-value project

# Deploy (using script)
.\deploy.ps1

# Or deploy manually
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection
gcloud run deploy kerala-crowd-detection --image gcr.io/YOUR_PROJECT_ID/kerala-crowd-detection --platform managed --region us-central1 --allow-unauthenticated --memory 2Gi --cpu 2

# Set environment variable (optional)
gcloud run services update kerala-crowd-detection --update-env-vars KEY=value --region us-central1

# Get service URL
gcloud run services describe kerala-crowd-detection --region us-central1 --format 'value(status.url)'

# View logs
gcloud run services logs read kerala-crowd-detection --region us-central1
```

## ⚠️ Troubleshooting

**"gcloud: command not found"**
- Install Google Cloud SDK
- Restart terminal/PowerShell
- Check PATH environment variable

**"Project not found"**
- Verify project exists in console
- Check project ID is correct
- List projects: `gcloud projects list`

**"Permission denied"**
- Make sure billing is enabled
- Check you're logged in: `gcloud auth list`
- Verify project permissions

**"Build failed"**
- Check Dockerfile is correct
- Verify all files are present
- View build logs: `gcloud builds list`

**"Service not responding"**
- Check logs: `gcloud run services logs read kerala-crowd-detection --region us-central1`
- Verify environment variables
- Check memory is 2Gi minimum

## 📊 Estimated Timeline

- **Setup**: 15-20 minutes
- **Deployment**: 5-10 minutes
- **Testing**: 5 minutes
- **Total**: ~30 minutes

## 💰 Cost Estimate

- **Free tier**: 2 million requests/month
- **Low usage** (10K requests): ~$5-10/month
- **Medium usage** (100K requests): ~$20-30/month

## ✅ Success Criteria

You'll know deployment is successful when:
- [ ] Service URL is accessible
- [ ] Frontend loads correctly
- [ ] API endpoints respond
- [ ] City crowd queries work
- [ ] Typing animation appears
- [ ] City queries work

## 🚀 After Deployment

Once deployed, we'll:
1. Test the deployment
2. Set up MCP integration
3. Configure any additional features

Ready to start? Begin with Step 1!



