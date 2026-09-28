@echo off
title Launch Resume-Job Matcher Full Stack Project
cd /d "%~dp0"

echo ===================================================================
echo  Starting Resume-Job Description Matching Full-Stack Application
echo ===================================================================
echo.
echo Launching Backend (FastAPI on http://127.0.0.1:8001)...
start "Resume Matcher - Backend (FastAPI)" cmd /c "%~dp0run_backend.bat"

timeout /t 3 /nobreak >nul

echo Launching Frontend (Vite on http://127.0.0.1:5173)...
start "Resume Matcher - Frontend (Vite React)" cmd /c "%~dp0run_frontend.bat"

echo.
echo ===================================================================
echo Application successfully launched!
echo - Frontend Dashboard: http://127.0.0.1:5173
echo - Backend API Docs:   http://127.0.0.1:8001/docs
echo ===================================================================
timeout /t 5
