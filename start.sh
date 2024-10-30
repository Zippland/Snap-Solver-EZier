// start-all.sh
#!/bin/bash

echo "======================================"
echo "         启动 Snap-Solver 服务"
echo "======================================"
echo

# 获取本机IP地址
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    ip=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
else
    # Linux
    ip=$(hostname -I | awk '{print $1}')
fi

# 启动 Node.js 服务
echo "[1/2] 启动 Web 服务..."
node scripts/start.js &
NODE_PID=$!

# 等待几秒确保服务启动
sleep 3

# 启动 Python 截图服务
echo "[2/2] 启动截图服务..."
python3 snap.py &
PYTHON_PID=$!

# 清理屏幕并显示访问信息
clear
echo "======================================"
echo "Snap-Solver 服务已启动！"
echo "======================================"
echo
echo "快捷键说明："
echo "- Alt + Ctrl + S: 截图"
echo "- ESC: 退出截图程序"
echo
echo "访问地址："
echo "- 本地访问：http://localhost:3000"
echo "- 局域网访问：http://$ip:3000"
echo
echo "按 Ctrl+C 停止所有服务"
echo "======================================"

# 等待用户中断
trap "kill $NODE_PID $PYTHON_PID; exit" INT
wait