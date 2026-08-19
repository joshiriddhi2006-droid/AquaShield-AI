@echo off
title AquaShield - Complete System Launcher

echo.
echo ============================================================
echo              AQUASHIELD AI - STARTING
echo ============================================================
echo.

set "ROOT=%~dp0"

echo Project folder:
echo %ROOT%
echo.

REM ============================================================
REM START AI SERVICE - PORT 8000
REM ============================================================

echo [1/4] Starting AquaShield AI Service on port 8000...

start "AquaShield AI - Port 8000" cmd /k "cd /d "%ROOT%ai_module" && python -m uvicorn api_service:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul


REM ============================================================
REM START AUTHORITY DASHBOARD - PORT 5000
REM ============================================================

echo [2/4] Starting Authority Dashboard on port 5000...

start "AquaShield Authority - Port 5000" cmd /k "cd /d "%ROOT%authority_dashboard" && python aquashield_ai.py"

timeout /t 3 /nobreak >nul


REM ============================================================
REM START GIS ROUTE PLANNER - PORT 8501
REM ============================================================

echo [3/4] Starting GIS Route Planner on port 8501...

start "AquaShield GIS - Port 8501" cmd /k "cd /d "%ROOT%gis_module" && python -m streamlit run app.py --server.port 8501"

timeout /t 5 /nobreak >nul


REM ============================================================
REM START FRONTEND - PORT 5500
REM ============================================================

echo [4/4] Starting AquaShield Frontend on port 5500...

start "AquaShield Frontend - Port 5500" cmd /k "cd /d "%ROOT%frontend" && python -m http.server 5500"

timeout /t 3 /nobreak >nul


REM ============================================================
REM OPEN MAIN AQUASHIELD PAGE
REM ============================================================

echo.
echo ============================================================
echo              AQUASHIELD IS STARTING
echo ============================================================
echo.
echo AI Service:
echo http://127.0.0.1:8000
echo.
echo Authority Dashboard:
echo http://127.0.0.1:5000
echo.
echo GIS Route Planner:
echo http://127.0.0.1:8501
echo.
echo Main AquaShield:
echo http://127.0.0.1:5500/index.html
echo.
echo ============================================================
echo.

timeout /t 5 /nobreak >nul

start "" "http://127.0.0.1:5500/index.html"

echo AquaShield launched successfully.
echo.
echo DO NOT CLOSE the four server windows while using AquaShield.
echo.
pause