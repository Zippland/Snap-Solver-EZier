@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0"
title Snap-Solver 启动器

:: 检查参数
if "%1"=="--gui" (
    goto run_gui
) else if "%1"=="--service" (
    goto run_service
) else (
    goto run_gui
)

:run_gui
:: 运行配置界面
python config_gui.py
goto :eof

:run_service
:: 从配置工具中启动服务时使用
echo ================================================
echo                  启动服务
echo ================================================
echo.
echo [*] 正在启动服务...
echo.

npm start

echo.
echo [!] 服务已停止运行
pause