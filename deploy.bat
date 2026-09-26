@echo off
echo ========================================================
echo   SHREE KRIPA MIDWAY RESTAURANT - QR & STANDEE DEPLOYER
echo ========================================================
echo.
echo [1/3] Generating 300 DPI Standees & QR Codes...
python generate_qr.py
echo.
echo [2/3] Staging and Committing Changes...
git add .
git commit -m "update"
echo.
echo [3/3] Pushing to GitHub Pages (main)...
git push
echo.
echo [DONE] Live changes deployed successfully!
pause
