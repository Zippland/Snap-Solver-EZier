// start-all.bat
@echo off
chcp 65001
cls
echo ======================================
echo         启动 Snap-Solver 服务
echo ======================================
echo.

:: 获取本机IP地址
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /r "IPv4.*[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*"') do (
    set ip=%%a
    set ip=!ip:~1!
)

:: 启动 Node.js 服务
echo [1/2] 启动 Web 服务...
start "" node scripts/start.js

:: 等待几秒确保服务启动
timeout /t 3 /nobreak > nul

:: 启动 Python 截图服务
echo [2/2] 启动截图服务...
start "" python snap.py

:: 清理屏幕并显示访问信息
cls
echo ======================================
echo Snap-Solver 服务已启动！
echo ======================================
echo.
echo 快捷键说明：
echo - Alt + Ctrl + S: 截图
echo - ESC: 退出截图程序
echo.
echo 访问地址：
echo - 本地访问：http://localhost:3000
echo - 局域网访问：http://%ip%:3000
echo.
echo 提示：按任意键关闭本窗口不会停止服务
echo 如需停止服务，请关闭另外两个命令行窗口
echo ======================================

pause > nul