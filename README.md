# Snap-Solver 使用指南

Snap-Solver 是一个题目解答工具，可以通过自动识别电脑上的题目并自动解答。

## 安装步骤（小白版）

### 1. 安装必要软件

1. 安装 Node.js
   - 访问 https://nodejs.org/
   - 下载并安装 "LTS" 版本
   - 安装时全部默认选项即可

2. 安装 Python
   - 访问 https://www.python.org/downloads/
   - 下载并安装最新版 Python
   - 安装时勾选 "Add Python to PATH"

### 2. 下载本项目
- 点击页面顶部绿色的 "Code" 按钮
- 选择 "Download ZIP"
- 解压下载的文件到任意位置

### 3. 配置项目
1. 打开解压后的文件夹
2. 创建一个名为 `.env` 的文件（注意包含小数点）
3. 在文件中粘贴以下内容（替换 API 密钥）：
```
HOST=0.0.0.0
PORT=3000
OPENAI_API_KEY=你的OpenAI密钥
```

### 4. 安装依赖
1. 在项目文件夹中按住 Shift + 鼠标右键
2. 选择"在此处打开 PowerShell 窗口"
3. 输入以下命令：
```
npm install
pip install keyboard Pillow requests
```

## 使用方法

### 启动服务
- 双击 `start-all.bat`
- 会打开三个窗口，这是正常的
- 记住显示的网址，比如 `http://192.168.1.100:3000`

### 使用功能
1. 打开浏览器，输入显示的网址
2. 按 `Alt + Ctrl + S` 进行截图
3. 在网页上处理截图并获取答案

### 快捷键
- `Alt + Ctrl + S`: 截图
- `ESC`: 退出截图功能

### 关闭服务
- 关闭所有命令行窗口即可

## 常见问题

1. 如果提示 "npm 不是内部或外部命令"
   - 重新安装 Node.js
   - 重启电脑

2. 如果提示 "python 不是内部或外部命令"
   - 重新安装 Python
   - 确保安装时勾选了 "Add Python to PATH"

3. 如果其他设备访问不了
   - 检查防火墙设置
   - 确保在同一个网络内

## 需要帮助？
遇到问题请提交 Issue 或联系作者。