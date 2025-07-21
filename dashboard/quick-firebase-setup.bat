@echo off
echo ========================================
echo Quick Firebase Setup
echo ========================================
echo.

echo 🔧 Installing Firebase CLI globally...
call npm install -g firebase-tools

echo.
echo 🔐 Please login to Firebase...
call firebase login

echo.
echo 📋 Next steps:
echo 1. Go to https://console.firebase.google.com/
echo 2. Create a new project (name it: thesis-dashboard-2024)
echo 3. Copy the Project ID
echo 4. Edit .firebaserc and replace the project ID
echo 5. Run: firebase init hosting
echo 6. Run: deploy.bat
echo.
echo Press any key to continue...
pause