@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0"
title Snap-Solver 智能启动器
color 0A

:: 创建临时目录
if not exist "temp" mkdir temp
if not exist "logs" mkdir logs

echo ================================================
echo            Snap-Solver 智能启动器
echo ================================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] 需要管理员权限！
    echo 请右键选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)
echo [√] 管理员权限检查通过
echo.

:: 检查并安装 Node.js
echo [*] 检查 Node.js 环境...
node -v >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] 未检测到 Node.js，准备安装...
    
    :: 下载 Node.js
    echo [*] 下载 Node.js 安装包...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://nodejs.org/dist/v18.17.0/node-v18.17.0-x64.msi' -OutFile 'temp\node_installer.msi'}"
    
    if !errorLevel! neq 0 (
        echo [ERROR] Node.js 下载失败！
        echo 请手动安装 Node.js: https://nodejs.org/
        pause
        exit /b 1
    )
    
    :: 安装 Node.js
    echo [*] 正在安装 Node.js...
    msiexec /i "temp\node_installer.msi" /qn /norestart
    
    :: 等待安装完成
    timeout /t 10 /nobreak >nul
    
    :: 检查安装结果
    node -v >nul 2>&1
    if !errorLevel! neq 0 (
        echo [ERROR] Node.js 安装失败！
        echo 请手动安装 Node.js: https://nodejs.org/
        pause
        exit /b 1
    )
    echo [√] Node.js 安装成功
) else (
    echo [√] Node.js 已安装
)
echo.

:: 检查并安装 Python
echo [*] 检查 Python 环境...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] 未检测到 Python，准备安装...
    
    :: 下载 Python
    echo [*] 下载 Python 安装包...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe' -OutFile 'temp\python_installer.exe'}"
    
    if !errorLevel! neq 0 (
        echo [ERROR] Python 下载失败！
        echo 请手动安装 Python: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    :: 安装 Python
    echo [*] 正在安装 Python...
    temp\python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    :: 等待安装完成
    timeout /t 10 /nobreak >nul
    
    :: 检查安装结果
    python --version >nul 2>&1
    if !errorLevel! neq 0 (
        echo [ERROR] Python 安装失败！
        echo 请手动安装 Python: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    echo [√] Python 安装成功
) else (
    echo [√] Python 已安装
)
echo.

:: 检查并安装依赖
echo [*] 安装必要依赖...
echo.

:: npm 依赖
echo [*] 安装 Node.js 依赖...
call npm install >>logs\npm_install.log 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Node.js 依赖安装失败！
    echo 详情请查看 logs\npm_install.log
    pause
    exit /b 1
)
echo [√] Node.js 依赖安装完成
echo.

:: Python 依赖
echo [*] 安装 Python 依赖...
pip install keyboard Pillow requests >>logs\pip_install.log 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python 依赖安装失败！
    echo 详情请查看 logs\pip_install.log
    pause
    exit /b 1
)
echo [√] Python 依赖安装完成
echo.

:: 检查并创建 .env 文件
if not exist ".env" (
    echo [*] 创建配置文件...
    (
        echo HOST=0.0.0.0
        echo PORT=3000
        echo OPENAI_API_KEY=your_api_key_here
    ) > .env
    
    echo [!] 请在打开的记事本中设置你的 OpenAI API 密钥
    echo [!] 设置完成后保存并关闭记事本窗口
    timeout /t 3 >nul
    notepad .env
)

:: 配置防火墙规则
echo [*] 配置防火墙规则...
netsh advfirewall firewall show rule name="Snap-Solver" >nul 2>&1
if %errorLevel% == 1 (
    netsh advfirewall firewall add rule name="Snap-Solver" dir=in action=allow protocol=TCP localport=3000 >nul 2>&1
    echo [√] 防火墙规则已添加
) else (
    echo [√] 防火墙规则已存在
)
echo.

:: 获取本机IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /r /c:"IPv4.*[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*"') do (
    set IP=%%a
    set IP=!IP:~1!
    goto :found_ip
)
:found_ip

:: 清理临时文件
if exist "temp" rd /s /q "temp"

:: 启动服务
echo ================================================
echo                  启动服务
echo ================================================
echo.
echo [*] 服务访问地址:
echo     本地访问: http://localhost:3000
echo     局域网访问: http://%IP%:3000
echo.
echo [*] 快捷键说明:
echo     截图: Alt + Ctrl + S
echo     退出截图: ESC
echo.
echo [*] 正在启动服务...
echo.

:: 启动服务
npm start

echo.
echo [!] 服务已停止运行
pause