@echo off
echo ========================================
echo Firebase Deployment Script
echo ========================================
echo.

echo 🔧 Installing dependencies...
call npm install

echo.
echo 📊 Exporting data from analysis...
cd ..
python dashboard/export_scripts/export_dashboard_data.py
cd dashboard

echo.
echo 🏗️ Building for production...
call npm run build

echo.
echo 🔥 Deploying to Firebase...
echo.
echo If this is your first time, you'll need to:
echo 1. Install Firebase CLI: npm install -g firebase-tools
echo 2. Login: firebase login
echo 3. Initialize project: firebase init hosting
echo.
echo Press any key to continue with deployment...
pause

call firebase deploy --only hosting

echo.
echo ✅ Deployment complete!
echo Your dashboard should be available at the Firebase URL above
echo.
pause