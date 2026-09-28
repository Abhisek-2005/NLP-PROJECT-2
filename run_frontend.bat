@echo off
title Resume-Job Description Matcher Frontend
cd /d "%~dp0\frontend"

echo ========================================================
echo Starting Vite + React + Tailwind CSS Dashboard...
echo ========================================================

set "PATH=%LOCALAPPDATA%\Programs\node-lts;%LOCALAPPDATA%\Programs\node-lts\node_modules\npm\bin;C:\Users\abhis\anaconda3;C:\Users\abhis\anaconda3\Scripts;%PATH%"

npm run dev -- --host 127.0.0.1
pause
