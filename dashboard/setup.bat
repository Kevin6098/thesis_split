@echo off
echo ========================================
echo Japanese Restaurant Reviews Dashboard
echo ========================================
echo.

echo 📦 Installing dependencies...
call npm install

echo.
echo 📊 Exporting data from analysis...
cd ..
python dashboard/export_scripts/export_dashboard_data.py
cd dashboard

echo.
echo 🚀 Starting development server...
echo Dashboard will be available at http://localhost:5173
echo.
echo Press Ctrl+C to stop the server
call npm run dev

pause