#!/bin/bash

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查命令行参数
if [ "$1" == "--gui" ]; then
    python3 config_gui.py
    exit 0
elif [ "$1" == "--service" ]; then
    # 从配置工具中启动服务时使用
    echo -e "${BLUE}================================================"
    echo "                  启动服务"
    echo -e "================================================${NC}"
    echo ""
    echo -e "${BLUE}[*] 正在启动服务...${NC}"
    echo ""
    
    # 启动服务
    npm start
    
    echo ""
    echo -e "${YELLOW}[!] 服务已停止运行${NC}"
    exit 0
fi

# 默认运行配置界面
python3 config_gui.py