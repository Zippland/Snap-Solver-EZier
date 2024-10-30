#!/bin/bash

# start.sh
set -e

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${GREEN}=================================================${NC}"
echo -e "${GREEN}             Snap-Solver 一键启动工具${NC}"
echo -e "${GREEN}=================================================${NC}"

# 检查权限
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}[!] 请使用 sudo 运行此脚本${NC}"
    exit 1
fi

# 创建日志目录
mkdir -p logs

# 安装依赖
echo "[*] 安装依赖..."
npm install >>logs/npm_install.log 2>&1
pip3 install keyboard Pillow requests >>logs/pip_install.log 2>&1

# 检查 .env 文件
if [ ! -f ".env" ]; then
    cat > .env << EOL
HOST=0.0.0.0
PORT=3000
OPENAI_API_KEY=your_api_key_here
EOL
    echo "[!] 已创建 .env 文件，请设置 OpenAI API 密钥"
    nano .env
fi

# 设置可执行权限
chmod +x scripts/start.js

echo "[*] 启动服务..."
npm start