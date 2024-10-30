@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0"
title Snap-Solver 一键启动工具
color 0A

echo =================================================
echo              Snap-Solver 一键启动工具
echo =================================================
echo.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] 请以管理员权限运行此脚本
    pause
    exit /b 1
)

if not exist "logs" mkdir "logs"

echo [*] 检查依赖...
call npm install >>logs\npm_install.log 2>&1
pip install keyboard Pillow requests >>logs\pip_install.log 2>&1

if not exist ".env" (
    (
        echo HOST=0.0.0.0
        echo PORT=3000
        echo OPENAI_API_KEY=your_api_key_here
    ) > .env
    notepad .env
)

echo [*] 启动服务...
npm start
pause