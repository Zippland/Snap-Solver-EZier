import subprocess
import sys
import os

def check_and_install_dependencies():
    try:
        # 检查 pystray 是否已安装
        try:
            import pystray
            print("pystray already installed.")
            return True
        except ImportError:
            print("Installing pystray...")
            
            # 使用 subprocess.CREATE_NO_WINDOW 标志来隐藏控制台窗口
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'pystray'],
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                check=True
            )
            print("pystray installation completed.")
            return True
            
    except Exception as e:
        print(f"Error installing dependencies: {str(e)}")
        return False

if __name__ == "__main__":
    if check_and_install_dependencies():
        # 安装完成后，启动 config_gui.py
        python_exe = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe') \
            if sys.platform == 'win32' else sys.executable
            
        subprocess.run(
            [python_exe, 'config_gui.py'],
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )