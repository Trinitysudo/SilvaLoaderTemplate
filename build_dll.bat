@echo off
echo Silva Loader - DLL Build Script
echo ================================

:: Check for Visual Studio
where cl >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Visual Studio C++ compiler not found!
    echo.
    echo Please run this from "Developer Command Prompt for VS" or "x64 Native Tools Command Prompt"
    echo.
    echo Alternatively, install Visual Studio 2019/2022 with C++ tools:
    echo https://visualstudio.microsoft.com/downloads/
    pause
    exit /b 1
)

echo Building TestDLL.dll...
echo.

:: Compile the DLL
cl /LD /O2 TestDLL.cpp user32.lib /Fe:TestDLL.dll

if %errorlevel% equ 0 (
    echo.
    echo ================================
    echo SUCCESS! TestDLL.dll compiled
    echo ================================
    echo.
    echo File location: %CD%\TestDLL.dll
    echo.
    echo You can now use this DLL with Silva Loader
    echo Test it by injecting into notepad.exe
    echo.
    
    :: Clean up build artifacts
    del TestDLL.obj TestDLL.exp TestDLL.lib 2>nul
) else (
    echo.
    echo ================================
    echo ERROR: Build failed!
    echo ================================
)

pause
