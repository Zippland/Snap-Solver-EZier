# 📚 Snap-Solver

> 一键识题，自动解答 —— 你的智能解题助手

Snap-Solver 是一个用于笔试、测评的智能题目解答工具，只需**按下快捷键**，即可**在附近设备上**自动识别题目并给出详细解答。

目前支持使用 GPT-4o 或 Claude 3.5 来识图解题。

## ✨ 特色功能

- 🎯 **一键截图**：使用快捷键（可自定义）即可远程监控电脑屏幕
- 🌐 **局域网共享**：一处部署，多处使用，同一网络下**所有设备**都是监控设备
- 🔍 **智能识图**：使用 llm 图片接口识别文字，可对识别结果进行编辑修改
- 🤖 **AI 解答**：混合使用 GPT-4o 或 Claude-3.5-Sonnet(new) 来深度解析题目
- 🔐 **代理支持**：内置代理，支持国内用户通过代理访问 API
- 💻 **跨平台支持**：Windows、MacOS、Linux、ios、Android全平台可用

## 📋 使用前准备

1. **API Key**: 
   - 选择一个或两个 AI 服务并获取对应的 API Key：
     - OpenAI API Key：访问 [OpenAI 官网](https://openai.com) 获取
     - Claude API Key：访问 [Anthropic 官网](https://anthropic.com) 获取

2. **运行环境**:
   - [Node.js](https://nodejs.org/) 20.x 或更高版本
   - [Python](https://www.python.org/downloads/) 3.x 版本
   - （可选）代理软件，如 Clash、v2ray 等

## 🚀 快速开始

### Windows 用户

1. 下载项目后，右键 `run.bat`，选择"以管理员身份运行"
2. 首次运行会自动安装所需依赖
3. 根据提示填写你选择的 AI 服务的 API Key
4. 等待服务启动完成

### MacOS/Linux 用户

```bash
# 添加执行权限
chmod +x start.sh

# 运行启动脚本
sudo ./start.sh
```

## 💡 使用说明

### 1. 访问服务

- **本机访问**：打开浏览器，访问 http://localhost:3000
- **局域网访问**：其他设备使用 http://[服务器IP]:3000
  > 💡 服务器 IP 会在启动时显示在控制台中

### 2. 截图解题

1. 按下 `Alt + Ctrl + S` 组合键
2. 拖动鼠标选择题目区域
3. 松开鼠标完成截图
4. 选择以下方式之一：
   - **使用图片解题**：直接用图片内容解答
   - **分析文本再解题**：先识别文字，可以编辑后再解答

## ⚙️ 高级配置

### 配置文件说明 (.env)

```env
# 基础配置
HOST=0.0.0.0           # 服务监听地址
PORT=3000              # 服务端口号

# API Key 配置（选择一个或两个）
OPENAI_API_KEY=your_openai_key_here    # 如果使用 GPT-4o
CLAUDE_API_KEY=your_claude_key_here     # 如果使用 Claude

# AI选择 (必选其一)
EXTRACTION_AI=openai   # 文字识别用哪个AI (openai/claude)
SOLVING_AI=openai      # 解题用哪个AI (openai/claude)

# 代理设置
USE_PROXY=false        # 是否启用代理
PROXY_HOST=127.0.0.1   # 代理服务器地址
PROXY_PORT=4780        # 代理服务器端口
PROXY_PROTOCOL=http    # 代理协议(http/https)
```

### AI 模型说明

选用哪个 AI 服务，就需要配置对应的 API Key：
- **OpenAI**: 使用 gpt-4o-2024-08-06 模型
- **Claude**: 使用 claude-3-5-sonnet-20241022 模型

### 自定义快捷键

修改 `snap.py` 中的快捷键设置：
```python
# 默认是 alt+ctrl+s
keyboard.add_hotkey('alt+ctrl+s', take_screenshot)
```

## 🌐 代理配置

### 常见代理软件配置

#### 1. Clash
```env
USE_PROXY=true
PROXY_HOST=127.0.0.1
PROXY_PORT=7890        # Clash 默认 HTTP 代理端口
PROXY_PROTOCOL=http
```

#### 2. v2ray
```env
USE_PROXY=true
PROXY_HOST=127.0.0.1
PROXY_PORT=10809       # v2ray 默认 HTTP 代理端口
PROXY_PROTOCOL=http
```

### 代理故障排查

1. **检查代理状态**:
   - 确认代理软件是否正常运行
   - 验证代理端口是否正确
   - 测试代理连接：
     ```bash
     curl -x http://127.0.0.1:你的代理端口 https://api.openai.com/v1/chat/completions -v
     # 或
     curl -x http://127.0.0.1:你的代理端口 https://api.anthropic.com/v1/messages -v
     ```

2. **常见错误处理**:
   - 连接超时：检查代理服务是否正常运行
   - 证书错误：确认 HTTPS 代理配置是否正确
   - 认证失败：检查 API Key 是否正确

## 🔧 常见问题

### 1. 截图功能无响应？

- **Windows**: 
  - 确保以管理员权限运行
  - 检查任务管理器中是否有 Python 进程

- **MacOS/Linux**: 
  - 检查是否授予了屏幕录制权限
  - 尝试重新运行 `sudo ./start.sh`

### 2. 服务无法访问？

1. 检查防火墙设置
2. 确认使用的端口（默认3000）未被占用
3. 验证其他设备是否在同一局域网内

### 3. API 调用失败？

1. 检查选用的 AI 服务的 API Key 是否正确设置
2. 确认 EXTRACTION_AI/SOLVING_AI 设置与你拥有的 API Key 匹配
3. 检查代理配置是否正确
4. 尝试更换代理或直连测试

## 🔐 安全建议

1. 避免将 API Key 分享给他人
2. 定期更新系统和依赖包
3. 建议只在可信任的局域网中使用
4. 使用代理时注意数据安全性

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📞 获取帮助

如果遇到问题：
1. 查看上述常见问题解答
2. 提交 Issue 描述你的问题

## 📜 开源协议

本项目采用 [MIT](LICENSE) 协议。

---

💝 如果这个项目对你有帮助，请给个 Star！感谢支持！