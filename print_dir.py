import os
import sys

def print_directory_structure(startpath, exclude_dirs=None, exclude_files=None):
    """
    打印目录结构
    
    :param startpath: 开始扫描的路径
    :param exclude_dirs: 要排除的目录列表
    :param exclude_files: 要排除的文件列表
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', '__pycache__', 'node_modules', 'dist', 'build']
    if exclude_files is None:
        exclude_files = ['.gitignore', '.DS_Store', '*.pyc']
        
    print(f"\n目录结构 ({startpath}):")
    print("=" * 50)
    
    # 获取第一层目录和文件
    try:
        items = os.listdir(startpath)
        files = [f for f in items if os.path.isfile(os.path.join(startpath, f))]
        dirs = [d for d in items if os.path.isdir(os.path.join(startpath, d))]
        
        # 过滤掉不需要的目录和文件
        dirs = [d for d in dirs if d not in exclude_dirs]
        files = [f for f in files if not any(
            (pattern.startswith('*') and f.endswith(pattern[1:])) or f == pattern 
            for pattern in exclude_files
        )]
        
        # 首先打印文件
        for f in sorted(files):
            print(f"├── {f}")
            
        # 然后打印目录及其内容
        for d in sorted(dirs):
            print(f"├── {d}/")
            dir_path = os.path.join(startpath, d)
            
            # 打印子目录内容
            for root, subdirs, subfiles in os.walk(dir_path):
                # 过滤掉不需要的目录
                subdirs[:] = [sd for sd in subdirs if sd not in exclude_dirs]
                
                # 计算相对于起始路径的层级
                level = root.replace(startpath, '').count(os.sep)
                indent = '│   ' * level
                
                # 过滤和打印文件
                filtered_files = [f for f in subfiles if not any(
                    (pattern.startswith('*') and f.endswith(pattern[1:])) or f == pattern 
                    for pattern in exclude_files
                )]
                
                for f in sorted(filtered_files):
                    print(f"{indent}├── {f}")
                
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    # 获取当前目录
    current_dir = os.getcwd()
    
    # 自定义要排除的目录和文件
    exclude_dirs = [
        '.git',
        '__pycache__',
        'node_modules',
        'dist',
        'build',
        'venv',
        '.idea',
        '.vscode'
    ]
    
    exclude_files = [
        '.gitignore',
        '.DS_Store',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '*.so',
        '*.dll',
        '*.dylib'
    ]
    
    # 打印目录结构
    print_directory_structure(current_dir, exclude_dirs, exclude_files)