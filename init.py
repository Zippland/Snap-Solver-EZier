# init.py
import subprocess
import sys
import os

def check_and_install_dependencies():
    try:
        # 检查必要的依赖包
        required_packages = ['pystray', 'cryptography', 'pyperclip']
        for package in required_packages:
            try:
                __import__(package)
                print(f"{package} 已安装.")
            except ImportError:
                print(f"正在安装 {package}...")
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', package],
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                    check=True
                )
                print(f"{package} 安装完成.")
        return True
            
    except Exception as e:
        print(f"检查依赖时出错: {str(e)}")
        return False

def validate_license():
    """验证许可证"""
    python_exe = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe') \
        if sys.platform == 'win32' else sys.executable

    # 运行许可证验证并等待完成
    result = subprocess.run(
        [python_exe, 'license_validator.py'],
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
    )
    
    # 只有当验证成功（返回值为0）时才返回True
    return result.returncode == 0

def run_config_gui():
    """运行配置界面"""
    python_exe = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe') \
        if sys.platform == 'win32' else sys.executable
        
    subprocess.run(
        [python_exe, 'config_gui.py'],
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
    )

if __name__ == "__main__":
    try:
        print("检查依赖...")
        if not check_and_install_dependencies():
            print("依赖检查失败")
            sys.exit(1)

        print("验证许可证...")
        if not validate_license():
            print("许可证验证失败")
            sys.exit(1)

        print("启动配置界面...")
        run_config_gui()
            
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        sys.exit(1)