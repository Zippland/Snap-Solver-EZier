import tkinter as tk
from tkinter import ttk, messagebox
import pystray
from PIL import Image
import json
import subprocess
import os
import sys
import threading
from pathlib import Path
import socket
import urllib.request
import time

class SnapSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Snap-Solver 配置工具")
        self.root.geometry("600x750")
        
        # 初始化托盘图标
        self.create_tray_icon()
        
        # 绑定窗口关闭事件
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        
        # 设置样式
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态显示区域
        self.status_frame = ttk.LabelFrame(main_frame, text="状态", padding=10)
        self.status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(self.status_frame, text="准备就绪")
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.url_label = ttk.Label(self.status_frame, text="")
        self.url_label.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # 配置区域
        config_frame = ttk.LabelFrame(main_frame, text="配置", padding=10)
        config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 基础设置
        ttk.Label(config_frame, text="基础设置", style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,10), sticky=tk.W)
        
        ttk.Label(config_frame, text="监听地址:").grid(row=1, column=0, sticky=tk.W)
        self.host_var = tk.StringVar(value="0.0.0.0")
        ttk.Entry(config_frame, textvariable=self.host_var).grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(config_frame, text="端口:").grid(row=2, column=0, sticky=tk.W)
        self.port_var = tk.StringVar(value="3000")
        ttk.Entry(config_frame, textvariable=self.port_var).grid(row=2, column=1, sticky=(tk.W, tk.E))
        
        # API Keys
        ttk.Label(config_frame, text="API设置", style='Title.TLabel').grid(row=3, column=0, columnspan=2, pady=(10,10), sticky=tk.W)
        
        ttk.Label(config_frame, text="OpenAI API Key:").grid(row=4, column=0, sticky=tk.W)
        self.openai_key_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.openai_key_var, show="*").grid(row=4, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(config_frame, text="Claude API Key:").grid(row=5, column=0, sticky=tk.W)
        self.claude_key_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.claude_key_var, show="*").grid(row=5, column=1, sticky=(tk.W, tk.E))
        
        # AI 选择
        ttk.Label(config_frame, text="AI选择", style='Title.TLabel').grid(row=6, column=0, columnspan=2, pady=(10,10), sticky=tk.W)
        
        ttk.Label(config_frame, text="文字识别 AI:").grid(row=7, column=0, sticky=tk.W)
        self.extraction_ai_var = tk.StringVar(value="openai")
        ttk.Combobox(config_frame, textvariable=self.extraction_ai_var, values=["openai", "claude"], 
                    state="readonly").grid(row=7, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(config_frame, text="解题 AI:").grid(row=8, column=0, sticky=tk.W)
        self.solving_ai_var = tk.StringVar(value="openai")
        ttk.Combobox(config_frame, textvariable=self.solving_ai_var, values=["openai", "claude"], 
                    state="readonly").grid(row=8, column=1, sticky=(tk.W, tk.E))
        
        # 提示词设置
        ttk.Label(config_frame, text="解题提示设置", style='Title.TLabel').grid(row=14, column=0, columnspan=2, pady=(10,10), sticky=tk.W)

        ttk.Label(config_frame, text="默认解题提示:").grid(row=15, column=0, sticky=tk.W)
        self.solving_prompt_var = tk.StringVar(value="请详细分析这道题目并给出完整的解答思路和步骤。如果是选择题，请分析每个选项并说明选择的理由。")
        prompt_entry = ttk.Entry(config_frame, textvariable=self.solving_prompt_var, width=50)
        prompt_entry.grid(row=15, column=1, sticky=(tk.W, tk.E))
    
        # 代理设置
        ttk.Label(config_frame, text="代理设置", style='Title.TLabel').grid(row=9, column=0, columnspan=2, pady=(10,10), sticky=tk.W)
        
        self.use_proxy_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(config_frame, text="启用代理", variable=self.use_proxy_var).grid(row=10, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Label(config_frame, text="代理协议:").grid(row=11, column=0, sticky=tk.W)
        self.proxy_protocol_var = tk.StringVar(value="http")
        ttk.Combobox(config_frame, textvariable=self.proxy_protocol_var, values=["http", "https"], 
                    state="readonly").grid(row=11, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(config_frame, text="代理地址:").grid(row=12, column=0, sticky=tk.W)
        self.proxy_host_var = tk.StringVar(value="127.0.0.1")
        ttk.Entry(config_frame, textvariable=self.proxy_host_var).grid(row=12, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(config_frame, text="代理端口:").grid(row=13, column=0, sticky=tk.W)
        self.proxy_port_var = tk.StringVar(value="4780")
        ttk.Entry(config_frame, textvariable=self.proxy_port_var).grid(row=13, column=1, sticky=(tk.W, tk.E))
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        self.save_btn = ttk.Button(button_frame, text="保存配置", command=self.save_config)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.install_btn = ttk.Button(button_frame, text="安装依赖", command=self.install_dependencies)
        self.install_btn.pack(side=tk.LEFT, padx=5)
        
        self.start_btn = ttk.Button(button_frame, text="启动服务", command=self.start_service)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="停止服务", command=self.stop_service, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # 设置列权重
        main_frame.columnconfigure(0, weight=1)
        config_frame.columnconfigure(1, weight=1)
        
        # 加载现有配置
        self.load_config()

    def create_tray_icon(self):
        """创建系统托盘图标"""
        # 创建一个简单的图标（16x16 的纯色图标）
        image = Image.new('RGB', (16, 16), color='purple')
        menu = pystray.Menu(
            pystray.MenuItem("显示窗口", self.show_window),
            pystray.MenuItem("退出程序", self.quit_application)
        )
        self.icon = pystray.Icon("snap-solver", image, "Snap-Solver", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def show_window(self, icon=None, item=None):
        """显示窗口"""
        self.root.deiconify()  # 显示窗口
        self.root.state('normal')
        self.root.focus_force()  # 给窗口焦点

    def on_closing(self):
        """处理窗口关闭事件"""
        self.root.withdraw()  # 隐藏窗口而不是关闭
        if not hasattr(self, 'minimize_hint_shown'):
            messagebox.showinfo("提示", "程序已最小化到系统托盘，可以在托盘图标右键菜单中退出程序。")
            self.minimize_hint_shown = True

    def quit_application(self, icon=None, item=None):
        """完全退出应用程序"""
        # 停止服务
        self.stop_service()
        # 移除托盘图标
        if hasattr(self, 'icon'):
            self.icon.stop()
        # 销毁窗口
        self.root.destroy()
        # 强制退出程序
        os._exit(0)

    def get_python_exe(self):
        """获取pythonw.exe的路径"""
        if sys.platform == 'win32':
            python_path = os.path.dirname(sys.executable)
            pythonw = os.path.join(python_path, 'pythonw.exe')
            return pythonw if os.path.exists(pythonw) else sys.executable
        return sys.executable
    
    def get_node_path(self):
        """获取 node.exe 的路径"""
        if sys.platform == 'win32':
            program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
            program_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
            possible_paths = [
                os.path.join(program_files, 'nodejs', 'node.exe'),
                os.path.join(program_files_x86, 'nodejs', 'node.exe'),
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
        return 'node'  # 非 Windows 系统直接返回 'node'
    
    def set_status(self, message, error=False):
        """更新状态显示"""
        self.status_label.config(text=message)
        if error:
            messagebox.showerror("错误", message)

    def get_local_ip(self):
        """获取本机局域网IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists('.env'):
                with open('.env', 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            try:
                                key, value = line.strip().split('=', 1)
                                if key == 'HOST':
                                    self.host_var.set(value)
                                elif key == 'PORT':
                                    self.port_var.set(value)
                                elif key == 'OPENAI_API_KEY':
                                    self.openai_key_var.set(value)
                                elif key == 'CLAUDE_API_KEY':
                                    self.claude_key_var.set(value)
                                elif key == 'EXTRACTION_AI':
                                    self.extraction_ai_var.set(value.lower())
                                elif key == 'SOLVING_AI':
                                    self.solving_ai_var.set(value.lower())
                                elif key == 'USE_PROXY':
                                    self.use_proxy_var.set(value.lower() == 'true')
                                elif key == 'PROXY_HOST':
                                    self.proxy_host_var.set(value)
                                elif key == 'PROXY_PORT':
                                    self.proxy_port_var.set(value)
                                elif key == 'PROXY_PROTOCOL':
                                    self.proxy_protocol_var.set(value.lower())
                                elif key == 'SOLVING_PROMPT':
                                    # 如果配置文件中存在提示词，则加载它
                                    # 否则保持默认提示词
                                    if value.strip():
                                        self.solving_prompt_var.set(value)
                            except ValueError:
                                # 如果某一行的格式不正确，跳过该行并继续
                                print(f"Warning: Skipping invalid config line: {line.strip()}")
                                continue
                
                self.set_status("配置加载完成")
            else:
                # 如果配置文件不存在，设置默认值
                self.host_var.set("0.0.0.0")
                self.port_var.set("3000")
                self.extraction_ai_var.set("openai")
                self.solving_ai_var.set("openai")
                self.use_proxy_var.set(False)
                self.proxy_host_var.set("127.0.0.1")
                self.proxy_port_var.set("4780")
                self.proxy_protocol_var.set("http")
                self.solving_prompt_var.set("请详细分析这道题目并给出完整的解答思路和步骤。如果是选择题，请分析每个选项并说明选择的理由。")
                
                self.set_status("使用默认配置")
        except Exception as e:
            self.set_status(f"加载配置失败: {str(e)}", True)
            # 出错时也设置默认值
            self.host_var.set("0.0.0.0")
            self.port_var.set("3000")
            self.extraction_ai_var.set("openai")
            self.solving_ai_var.set("openai")
            self.use_proxy_var.set(False)
            self.proxy_host_var.set("127.0.0.1")
            self.proxy_port_var.set("4780")
            self.proxy_protocol_var.set("http")
            self.solving_prompt_var.set("请详细分析这道题目并给出完整的解答思路和步骤。如果是选择题，请分析每个选项并说明选择的理由。")


    def save_config(self):
        try:
            config_content = f"""# 基础配置
    HOST={self.host_var.get()}
    PORT={self.port_var.get()}

    # API Key 配置
    OPENAI_API_KEY={self.openai_key_var.get()}
    CLAUDE_API_KEY={self.claude_key_var.get()}

    # AI选择
    EXTRACTION_AI={self.extraction_ai_var.get()}
    SOLVING_AI={self.solving_ai_var.get()}

    # 解题提示设置
    SOLVING_PROMPT={self.solving_prompt_var.get()}

    # 代理设置
    USE_PROXY={str(self.use_proxy_var.get()).lower()}
    PROXY_HOST={self.proxy_host_var.get()}
    PROXY_PORT={self.proxy_port_var.get()}
    PROXY_PROTOCOL={self.proxy_protocol_var.get()}"""

            with open('.env', 'w', encoding='utf-8') as f:
                f.write(config_content)
            
            self.set_status("配置已保存")
        except Exception as e:
            self.set_status(f"保存配置失败: {str(e)}", True)

    def check_nodejs(self):
        """检查是否安装了 Node.js"""
        try:
            subprocess.run(['node', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def install_nodejs(self):
        """安装 Node.js"""
        try:
            self.set_status("正在安装 Node.js...")
            if not os.path.exists('temp'):
                os.makedirs('temp')
            
            installer_path = os.path.join('temp', 'node_installer.msi')
            urllib.request.urlretrieve(
                'https://nodejs.org/dist/v18.17.0/node-v18.17.0-x64.msi',
                installer_path
            )
            
            subprocess.run(['msiexec', '/i', installer_path, '/qn', '/norestart'], check=True)
            time.sleep(10)
            
            return self.check_nodejs()
                
        except Exception as e:
            self.set_status(f"Node.js 安装失败: {str(e)}", True)
            return False
        finally:
            if os.path.exists('temp'):
                import shutil
                shutil.rmtree('temp', ignore_errors=True)

    def install_dependencies(self):
        """安装依赖"""
        def run_install():
            try:
                # 禁用按钮
                self.install_btn.state(['disabled'])
                self.save_btn.state(['disabled'])
                self.start_btn.state(['disabled'])
                
                # 配置启动信息来隐藏窗口
                startupinfo = None
                if sys.platform == 'win32':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE

                # 检查并安装 Node.js
                if not self.check_nodejs():
                    self.set_status("正在安装 Node.js...")
                    if not self.install_nodejs():
                        raise Exception("Node.js 安装失败")

                # 设置环境变量，包括代理
                env = os.environ.copy()
                if sys.platform == 'win32':
                    # 添加可能的 npm 路径
                    program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
                    program_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
                    possible_paths = [
                        os.path.join(program_files, 'nodejs'),
                        os.path.join(program_files_x86, 'nodejs'),
                        os.path.join(os.environ.get('APPDATA', ''), 'npm'),
                    ]
                    env['PATH'] = ';'.join(possible_paths + [env.get('PATH', '')])

                # 如果启用了代理，设置npm代理
                if self.use_proxy_var.get():
                    proxy_protocol = self.proxy_protocol_var.get()
                    proxy_host = self.proxy_host_var.get()
                    proxy_port = self.proxy_port_var.get()
                    proxy_url = f"{proxy_protocol}://{proxy_host}:{proxy_port}"
                    self.set_status(f"使用代理: {proxy_url}")
                    env['HTTP_PROXY'] = proxy_url
                    env['HTTPS_PROXY'] = proxy_url
                    # 对于某些特殊情况，也可能需要设置这些
                    env['http_proxy'] = proxy_url
                    env['https_proxy'] = proxy_url

                # 安装 Node.js 依赖
                self.set_status("正在安装 Node.js 依赖...")
                npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
                process = subprocess.run([npm_cmd, 'install'], 
                                      check=True,
                                      startupinfo=startupinfo,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      env=env,
                                      creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)

                # 修改 Python 依赖安装部分，添加 pystray
                self.set_status("正在安装 Python 依赖...")
                python_exe = self.get_python_exe()
                process = subprocess.run(
                    [python_exe, '-m', 'pip', 'install', 'keyboard', 'Pillow', 'requests', 'pystray'],
                    check=True,
                    startupinfo=startupinfo,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )

                self.set_status("依赖安装完成")
                messagebox.showinfo("成功", "所有依赖安装完成！")
                
            except Exception as e:
                self.set_status(f"安装依赖失败: {str(e)}", True)
            finally:
                self.install_btn.state(['!disabled'])
                self.save_btn.state(['!disabled'])
                self.start_btn.state(['!disabled'])

        threading.Thread(target=run_install, daemon=True).start()

    def start_service(self):
        """启动服务"""
        def run_service():
            try:
                # 禁用按钮
                self.start_btn.state(['disabled'])
                self.install_btn.state(['disabled'])
                self.save_btn.state(['disabled'])
                self.stop_btn.state(['!disabled'])
                
                self.set_status("正在启动服务...")
                
                # 配置启动信息来隐藏窗口
                startupinfo = None
                if sys.platform == 'win32':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE

                # 启动 Python 截图服务
                python_exe = self.get_python_exe()
                self.python_process = subprocess.Popen(
                    [python_exe, 'snap.py'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                    text=True
                )
                
                # 启动 Node.js 服务
                if sys.platform == 'win32':
                    node_exe = self.get_node_path()
                    self.node_process = subprocess.Popen(
                        [node_exe, 'scripts/start.js'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        startupinfo=startupinfo,
                        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                        text=True,
                        env=os.environ.copy()  # 继承环境变量
                    )
                else:
                    # 非 Windows 系统仍使用 npm
                    self.node_process = subprocess.Popen(
                        ['npm', 'start'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                
                # 等待服务启动
                time.sleep(2)
                
                # 更新状态和访问地址
                local_ip = self.get_local_ip()
                port = self.port_var.get()
                
                self.set_status("服务已启动")
                self.url_label.config(text=f"""本地访问: http://localhost:{port}
局域网访问: http://{local_ip}:{port}
快捷键: Alt + Ctrl + S 进行截图""")
                
                # 监控错误输出
                self.monitor_errors()
                
            except Exception as e:
                self.set_status(f"启动服务失败: {str(e)}", True)
                self.stop_service()

        threading.Thread(target=run_service, daemon=True).start()


    def monitor_errors(self):
        """监控服务错误输出"""
        def monitor():
            while True:
                if hasattr(self, 'python_process'):
                    error = self.python_process.stderr.readline()
                    if error:
                        self.set_status(f"截图服务错误: {error.strip()}", True)
                
                if hasattr(self, 'node_process'):
                    error = self.node_process.stderr.readline()
                    if error:
                        self.set_status(f"Node.js服务错误: {error.strip()}", True)
                
                # 检查进程是否还在运行
                if (not hasattr(self, 'python_process') or self.python_process.poll() is not None) and \
                   (not hasattr(self, 'node_process') or self.node_process.poll() is not None):
                    break
                
                time.sleep(0.1)
            
        threading.Thread(target=monitor, daemon=True).start()

    def stop_service(self):
        """停止服务"""
        try:
            self.set_status("正在停止服务...")
            
            # 停止 Python 进程
            if hasattr(self, 'python_process'):
                self.python_process.terminate()
                self.python_process.wait(timeout=5)
                delattr(self, 'python_process')
            
            # 停止 Node.js 进程
            if hasattr(self, 'node_process'):
                self.node_process.terminate()
                self.node_process.wait(timeout=5)
                delattr(self, 'node_process')
            
            self.set_status("服务已停止")
            self.url_label.config(text="")
            
        except Exception as e:
            self.set_status(f"停止服务时出错: {str(e)}", True)
        finally:
            # 恢复按钮状态
            self.start_btn.state(['!disabled'])
            self.install_btn.state(['!disabled'])
            self.save_btn.state(['!disabled'])
            self.stop_btn.state(['disabled'])

def main():
    root = tk.Tk()
    app = SnapSolverGUI(root)
    
    def check_pip_dependencies():
        try:
            import pystray
        except ImportError:
            # 如果没有安装 pystray，先安装它
            messagebox.showinfo("初始化", "首次运行需要安装一些必要组件，请稍候...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pystray'], 
                         creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            messagebox.showinfo("初始化", "组件安装完成，程序将重新启动...")
            python = sys.executable
            os.execl(python, python, *sys.argv)
    
    # 检查依赖
    check_pip_dependencies()
    
    # 运行主程序
    root.mainloop()

if __name__ == "__main__":
    main()