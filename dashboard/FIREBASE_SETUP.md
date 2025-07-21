# Firebase Hosting Setup Guide

This guide will help you deploy your thesis dashboard to Firebase Hosting.

## Prerequisites

1. **Node.js** (v16 or higher)
2. **npm** or **yarn**
3. **Google account** for Firebase

## Step 1: Install Firebase CLI

```bash
npm install -g firebase-tools
```

## Step 2: Login to Firebase

```bash
firebase login
```

This will open your browser to authenticate with your Google account.

## Step 3: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter project name: `thesis-dashboard-2024` (or your preferred name)
4. Follow the setup wizard (you can disable Google Analytics if not needed)
5. Note your **Project ID** - you'll need it for the next step

## Step 4: Update Project Configuration

Edit `.firebaserc` and replace the project ID:

```json
{
  "projects": {
    "default": "YOUR_PROJECT_ID_HERE"
  }
}
```

## Step 5: Initialize Firebase (First Time Only)

```bash
firebase init hosting
```

When prompted:
- Choose "Use an existing project"
- Select your project
- Public directory: `dist`
- Configure as single-page app: `Yes`
- Don't overwrite index.html: `No`

## Step 6: Deploy

### Option A: Use the deployment script
```bash
deploy.bat
```

### Option B: Manual deployment
```bash
# Install dependencies
npm install

# Export data (from project root)
cd ..
python dashboard/export_scripts/export_dashboard_data.py
cd dashboard

# Build and deploy
npm run build
firebase deploy --only hosting
```

## Step 7: Access Your Dashboard

After successful deployment, Firebase will provide a URL like:
```
https://your-project-id.web.app
```

## Custom Domain (Optional)

1. In Firebase Console, go to Hosting
2. Click "Add custom domain"
3. Follow the DNS configuration instructions

## Environment Variables (If Needed)

If you need environment variables, create a `.env` file:

```env
VITE_API_URL=your_api_url
VITE_FIREBASE_CONFIG=your_firebase_config
```

## Troubleshooting

### Common Issues:

1. **"Project not found"**
   - Make sure you're logged in: `firebase login`
   - Check your project ID in `.firebaserc`

2. **"Build failed"**
   - Check for missing dependencies: `npm install`
   - Verify all imports are correct

3. **"Deploy failed"**
   - Ensure you have proper permissions in Firebase project
   - Check Firebase CLI version: `firebase --version`

### Useful Commands:

```bash
# Check Firebase status
firebase projects:list

# View deployment history
firebase hosting:channel:list

# Rollback to previous version
firebase hosting:clone live:previous-version live:current-version

# Clear cache
firebase hosting:clear
```

## Performance Optimization

The dashboard is already optimized with:
- ✅ Code splitting with Vite
- ✅ Gzip compression
- ✅ Cache headers for static assets
- ✅ Single-page app routing
- ✅ Optimized bundle size

## Monitoring

After deployment, you can monitor:
- **Performance**: Firebase Console → Performance
- **Analytics**: Firebase Console → Analytics (if enabled)
- **Errors**: Firebase Console → Crashlytics (if enabled)

## Security

The dashboard is a static site, so security considerations are minimal:
- ✅ No server-side code
- ✅ All data is public (as intended for thesis presentation)
- ✅ No sensitive information exposed

## Cost

Firebase Hosting is **free** for:
- 10GB storage
- 10GB/month data transfer
- Custom domain support

Perfect for thesis presentations and academic projects!