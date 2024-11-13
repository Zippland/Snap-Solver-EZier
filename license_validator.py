import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from utils.license_utils import LicenseUtils

class LicenseValidatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Snap-Solver 许可证验证")
        self.root.geometry("500x400")
        
        # 初始化许可证工具
        self.license_utils = LicenseUtils()
        
        # 设置样式
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 10))
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        ttk.Label(self.main_frame, text="Snap-Solver 许可证验证", 
                 style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        
        # 机器码显示
        ttk.Label(self.main_frame, text="您的机器码：", 
                 style='Info.TLabel').grid(row=1, column=0, sticky=tk.W, pady=(0,5))
        
        self.machine_code = self.license_utils.get_machine_code()
        machine_code_frame = ttk.Frame(self.main_frame)
        machine_code_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0,20))
        
        self.machine_code_var = tk.StringVar(value=self.machine_code)
        machine_code_entry = ttk.Entry(machine_code_frame, 
                                     textvariable=self.machine_code_var, 
                                     state='readonly',
                                     width=50)
        machine_code_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        copy_btn = ttk.Button(machine_code_frame, 
                             text="复制",
                             command=self.copy_machine_code)
        copy_btn.pack(side=tk.RIGHT, padx=(5,0))
        
        # 许可证密钥输入
        ttk.Label(self.main_frame, text="请输入许可证密钥：", 
                 style='Info.TLabel').grid(row=3, column=0, sticky=tk.W, pady=(0,5))
        
        self.license_key_var = tk.StringVar()
        self.license_entry = ttk.Entry(self.main_frame, 
                                     textvariable=self.license_key_var,
                                     width=50)
        self.license_entry.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0,20))
        
        # 验证按钮
        self.verify_btn = ttk.Button(self.main_frame, 
                                   text="验证许可证",
                                   command=self.verify_license)
        self.verify_btn.grid(row=5, column=0, columnspan=2, pady=(0,20))
        
        # 许可证状态显示
        self.status_frame = ttk.LabelFrame(self.main_frame, text="许可证状态", padding=10)
        self.status_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0,20))
        
        self.status_label = ttk.Label(self.status_frame, 
                                    text="等待验证...",
                                    style='Info.TLabel')
        self.status_label.pack(expand=True, fill=tk.X)
        
        # 设置列权重
        self.main_frame.columnconfigure(0, weight=1)
        
        # 检查已保存的许可证
        self.check_saved_license()
        
        # 绑定回车键
        self.license_entry.bind('<Return>', lambda e: self.verify_license())
        
        # 设置窗口在屏幕中央
        self.center_window()

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """窗口关闭事件处理"""
        self.root.destroy()
        sys.exit(1)  # 非正常退出返回1
        
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def copy_machine_code(self):
        """复制机器码到剪贴板"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.machine_code)
        messagebox.showinfo("成功", "机器码已复制到剪贴板")
        
    def verify_license(self):
        """验证许可证"""
        license_key = self.license_key_var.get().strip()
        if not license_key:
            messagebox.showerror("错误", "请输入许可证密钥")
            return
            
        is_valid, message = self.license_utils.verify_license_key(license_key)
        
        if is_valid:
            self.status_label.config(text="许可证有效", foreground="green")
            # 保存有效的许可证
            self.license_utils.save_license(license_key)
            # 验证成功，正常退出
            self.root.destroy()
            sys.exit(0)  # 成功验证后返回0
        else:
            self.status_label.config(text=f"许可证无效: {message}", foreground="red")
            messagebox.showerror("验证失败", message)
            
    def check_saved_license(self):
        """检查是否有已保存的许可证"""
        saved_license = self.license_utils.load_license()
        if saved_license:
            self.license_key_var.set(saved_license)
            # 自动验证已保存的许可证
            self.verify_license()

def main():
    root = tk.Tk()
    app = LicenseValidatorGUI(root)
    root.mainloop()
    # 如果程序正常结束但没有验证成功，返回1
    sys.exit(1)

if __name__ == "__main__":
    main()