@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 创建调试日志
set "DEBUG_LOG=%~dp0debug.log"
echo Started script at %date% %time% > "%DEBUG_LOG%"

:: 将所有输出重定向到日志文件和控制台
call :log_setup

cd /d "%~dp0"
title Snap-Solver 智能启动器
color 0A

echo ================================================
echo            Snap-Solver 智能启动器
echo ================================================
echo.

:: 捕获可能的错误
if not exist "package.json" (
    echo [ERROR] 未找到 package.json 文件！
    echo 请确保在正确的目录中运行此脚本。
    echo Current directory: %cd%
    goto error
)

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] 需要管理员权限！
    echo 请右键选择"以管理员身份运行"
    goto error
)

echo [√] 权限检查通过
echo.

:: 检查 Node.js
echo [*] 检查 Node.js 环境...
node -v > "%DEBUG_LOG%" 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Node.js 未安装！
    echo 请安装 Node.js: https://nodejs.org/
    goto error
)
echo [√] Node.js 已安装
echo.

:: 检查 Python
echo [*] 检查 Python 环境...
python --version > "%DEBUG_LOG%" 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python 未安装！
    echo 请安装 Python: https://www.python.org/downloads/
    goto error
)
echo [√] Python 已安装
echo.

:: 安装依赖
echo [*] 安装依赖...
if not exist "node_modules" (
    echo [*] 安装 Node.js 依赖...
    call npm install >> "%DEBUG_LOG%" 2>&1
    if !errorLevel! neq 0 (
        echo [ERROR] Node.js 依赖安装失败！
        goto error
    )
)

echo [*] 安装 Python 依赖...
pip install keyboard Pillow requests >> "%DEBUG_LOG%" 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python 依赖安装失败！
    goto error
)

:: 检查配置文件
if not exist ".env" (
    echo [*] 创建配置文件...
    (
        echo HOST=0.0.0.0
        echo PORT=3000
        echo OPENAI_API_KEY=your_api_key_here
    ) > .env
    echo [!] 请设置 OpenAI API 密钥
    notepad .env
)

:: 启动服务
echo.
echo [*] 正在启动服务...
npm start

goto :eof

:error
echo.
echo [!] 发生错误，请查看 debug.log 获取详细信息
echo Current directory: %cd%
echo.
type "%DEBUG_LOG%"
echo.
pause
exit /b 1

:log_setup
:: 创建日志目录
if not exist "logs" mkdir "logs"
exit /b 0

:eof
pause
exit /b 0