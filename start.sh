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

# 创建必要的目录
mkdir -p logs
mkdir -p temp

# 打印标题
echo -e "${BLUE}================================================"
echo "            Snap-Solver 智能启动器"
echo -e "================================================${NC}"
echo ""

# 检查是否为 root 用户
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}[ERROR] 需要 root 权限！${NC}"
        echo "请使用 sudo 运行此脚本"
        echo ""
        exit 1
    fi
    echo -e "${GREEN}[√] root 权限检查通过${NC}"
    echo ""
}

# 检查并安装 Node.js
check_nodejs() {
    echo -e "${BLUE}[*] 检查 Node.js 环境...${NC}"
    if ! command -v node &> /dev/null; then
        echo -e "${YELLOW}[!] 未检测到 Node.js，准备安装...${NC}"
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if ! command -v brew &> /dev/null; then
                echo -e "${YELLOW}[!] 安装 Homebrew...${NC}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install node
        else
            # Linux
            if command -v apt &> /dev/null; then
                # Debian/Ubuntu
                curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
                sudo apt-get install -y nodejs
            elif command -v dnf &> /dev/null; then
                # Fedora
                sudo dnf install -y nodejs
            elif command -v yum &> /dev/null; then
                # CentOS
                curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
                sudo yum install -y nodejs
            else
                echo -e "${RED}[ERROR] 无法确定包管理器，请手动安装 Node.js${NC}"
                exit 1
            fi
        fi
        
        if ! command -v node &> /dev/null; then
            echo -e "${RED}[ERROR] Node.js 安装失败！${NC}"
            exit 1
        fi
    fi
    echo -e "${GREEN}[√] Node.js 已安装${NC}"
    echo ""
}

# 检查并安装 Python
check_python() {
    echo -e "${BLUE}[*] 检查 Python 环境...${NC}"
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}[!] 未检测到 Python，准备安装...${NC}"
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            brew install python3
        else
            # Linux
            if command -v apt &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip
            elif command -v dnf &> /dev/null; then
                sudo dnf install -y python3 python3-pip
            elif command -v yum &> /dev/null; then
                sudo yum install -y python3 python3-pip
            else
                echo -e "${RED}[ERROR] 无法确定包管理器，请手动安装 Python${NC}"
                exit 1
            fi
        fi
        
        if ! command -v python3 &> /dev/null; then
            echo -e "${RED}[ERROR] Python 安装失败！${NC}"
            exit 1
        fi
    fi
    echo -e "${GREEN}[√] Python 已安装${NC}"
    echo ""
}

# 安装依赖
install_dependencies() {
    echo -e "${BLUE}[*] 安装必要依赖...${NC}"
    
    # npm 依赖
    echo -e "${BLUE}[*] 安装 Node.js 依赖...${NC}"
    npm install >> logs/npm_install.log 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Node.js 依赖安装失败！${NC}"
        echo "详情请查看 logs/npm_install.log"
        exit 1
    fi
    echo -e "${GREEN}[√] Node.js 依赖安装完成${NC}"
    
    # Python 依赖
    echo -e "${BLUE}[*] 安装 Python 依赖...${NC}"
    python3 -m pip install keyboard Pillow requests >> logs/pip_install.log 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Python 依赖安装失败！${NC}"
        echo "详情请查看 logs/pip_install.log"
        exit 1
    fi
    echo -e "${GREEN}[√] Python 依赖安装完成${NC}"
    echo ""
}

# 检查并创建配置文件
check_config() {
    if [ ! -f ".env" ]; then
        echo -e "${BLUE}[*] 创建配置文件...${NC}"
        cat > .env << EOF
HOST=0.0.0.0
PORT=3000
OPENAI_API_KEY=your_api_key_here
EOF
        echo -e "${YELLOW}[!] 请设置你的 OpenAI API 密钥${NC}"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            open -t .env
        else
            xdg-open .env 2>/dev/null || nano .env || vim .env
        fi
    fi
}

# 获取本机 IP
get_local_ip() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1)
    else
        # Linux
        LOCAL_IP=$(hostname -I | awk '{print $1}')
    fi
}

# 清理临时文件
cleanup() {
    rm -rf temp
}

# 主程序
main() {
    check_root
    check_nodejs
    check_python
    install_dependencies
    check_config
    get_local_ip
    cleanup
    
    # 启动服务
    echo -e "${BLUE}================================================"
    echo "                  启动服务"
    echo -e "================================================${NC}"
    echo ""
    echo -e "${GREEN}[*] 服务访问地址:${NC}"
    echo "    本地访问: http://localhost:3000"
    echo "    局域网访问: http://$LOCAL_IP:3000"
    echo ""
    echo -e "${GREEN}[*] 快捷键说明:${NC}"
    echo "    截图: Alt + Ctrl + S"
    echo "    退出截图: ESC"
    echo ""
    echo -e "${BLUE}[*] 正在启动服务...${NC}"
    echo ""
    
    # 启动服务
    npm start
    
    echo ""
    echo -e "${YELLOW}[!] 服务已停止运行${NC}"
}

# 运行主程序
main