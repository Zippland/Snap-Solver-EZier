# Snap-Solver

Snap-Solver-Local 是一个基于 OpenAI API 的本地题目解答工具，支持截图识别和自动解答功能。它可以部署在局域网中，让多个设备都能方便地使用这个服务。

如果想部署在互联网(Heroku)，请访问项目：[Snap-Solver-Web](https://github.com/zippland/snap-solver-web)
(产生此需求的可能原因：比如在国内想使用GPT-4o/Claude-3.5 Sonnet)

## 功能特点

- 📸 快捷截图：使用快捷键快速截取屏幕上的题目
- 🔍 文字识别：自动提取图片中的文字内容
- 🤖 智能解答：使用 GPT-4o 模型进行题目分析和解答
- 🌐 局域网访问：支持在同一局域网内的多设备访问
- 💻 跨平台支持：支持 Windows、Linux 和 macOS

## 系统要求

- Node.js 14.0 或更高版本
- Python 3.x
- OpenAI API 密钥

## 安装步骤

1. 克隆项目并安装依赖：
```bash
git clone https://github.com/zippland/snap-solver-local.git
cd snap-solver-local
npm install
```

2. 安装 Python 依赖：
```bash
pip install keyboard Pillow requests
```

3. 创建配置文件：
```bash
# 创建 .env 文件
cp .env.example .env

# 编辑 .env 文件，填入你的配置
HOST=0.0.0.0
PORT=3000
OPENAI_API_KEY=your_api_key_here
```

## 启动服务

### Windows
```bash
# 直接运行
start.bat

# 或使用 npm
npm start
```

### Linux/Mac
```bash
# 添加执行权限
chmod +x start.sh

# 运行服务
./start.sh

# 或使用 npm
npm start
```

## 使用方法

1. 启动服务后，在浏览器访问：
   - 本机访问：http://localhost:3000
   - 局域网访问：http://[服务器IP]:3000

2. 使用截图功能：
   - Windows/Linux：按下 `Alt + Ctrl + S` 进行截图
   - 截图后自动上传并识别

3. 解题流程：
   - 上传图片后可以选择区域
   - 点击"提取文本"获取题目内容
   - 点击"解答题目"获取答案

## 快捷键

- `Alt + Ctrl + S`: 截取屏幕
- `ESC`: 退出截图程序

## 配置说明

在 `.env` 文件中可以配置以下参数：
```env
# 服务器监听地址 (0.0.0.0 表示所有网卡)
HOST=0.0.0.0

# 服务器端口
PORT=3000

# OpenAI API 密钥
OPENAI_API_KEY=your_api_key_here

# 可选：允许访问的 IP 地址列表（用逗号分隔）
ALLOWED_IPS=192.168.1.100,192.168.1.101
```

## 开发模式

使用开发模式运行服务（支持热重载）：
```bash
npm run dev
```

## 安全建议

1. 设置允许访问的 IP 范围
2. 定期更新依赖包
3. 使用强密码保护 API 密钥
4. 监控服务器日志

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 发起 Pull Request

## 许可证

MIT License

## 支持与反馈

如有问题或建议，请提交 Issue 