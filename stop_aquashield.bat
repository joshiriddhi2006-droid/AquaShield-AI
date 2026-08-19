@echo off
echo Stopping AquaShield services...
taskkill /FI "WINDOWTITLE eq AquaShield AI*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq AquaShield Authority*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq AquaShield Citizen Portal*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq AquaShield GIS*" /T /F >nul 2>&1
echo Done.
