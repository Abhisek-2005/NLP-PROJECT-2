@echo off
title Resume-Job Description Matcher Backend
cd /d "%~dp0"

echo ========================================================
echo Starting FastAPI NLP Resume Matcher Backend Server...
echo ========================================================

set "PATH=%LOCALAPPDATA%\Programs\node-lts;%LOCALAPPDATA%\Programs\node-lts\node_modules\npm\bin;C:\Users\abhis\anaconda3;C:\Users\abhis\anaconda3\Scripts;%PATH%"

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001 --reload
pause
