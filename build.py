import os
import sys
import shutil
import subprocess
import json
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('build.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class SnapSolverBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.dist_dir = self.root_dir / 'dist'
        self.build_dir = self.root_dir / 'build'
        self.temp_dir = self.root_dir / 'temp'
        self.node_modules_dir = self.root_dir / 'node_modules'

    def clean_directories(self):
        """Clean up previous build artifacts"""
        logging.info("Cleaning previous build artifacts...")
        for directory in [self.dist_dir, self.build_dir, self.temp_dir]:
            if directory.exists():
                shutil.rmtree(directory)
            directory.mkdir(parents=True, exist_ok=True)

    def install_python_dependencies(self):
        """Install required Python packages"""
        logging.info("Installing Python dependencies...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install',
            'pyinstaller',
            'pillow',
            'keyboard',
            'requests',
            'pystray',
            'cryptography',
            'pyperclip'
        ], check=True)

    def install_node_dependencies(self):
        """Install Node.js dependencies"""
        logging.info("Installing Node.js dependencies...")
        subprocess.run(['npm', 'install'], check=True)

    def create_version_file(self):
        """Create version.txt with build information"""
        version_info = {
            'version': '1.0.0',
            'build_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'python_version': sys.version,
        }
        
        with open(self.dist_dir / 'version.txt', 'w') as f:
            json.dump(version_info, f, indent=2)

    def bundle_frontend(self):
        """Bundle frontend assets"""
        logging.info("Bundling frontend assets...")
        # Copy public directory
        shutil.copytree(
            self.root_dir / 'public',
            self.dist_dir / 'public',
            dirs_exist_ok=True
        )

    def create_pyinstaller_spec(self):
        """Create PyInstaller spec file"""
        spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['init.py'],
    pathex=['{self.root_dir}'],
    binaries=[],
    datas=[
        ('assets/*', 'assets'),
        ('utils/*', 'utils'),
        ('public/*', 'public'),
        ('node_modules/*', 'node_modules'),
        ('.env.example', '.'),
        ('package.json', '.'),
        ('config.js', '.'),
        ('app.js', '.'),
        ('services/*', 'services'),
        ('controllers/*', 'controllers'),
        ('middleware/*', 'middleware'),
        ('routes/*', 'routes'),
        ('scripts/*', 'scripts')
    ],
    hiddenimports=[
        'PIL',
        'keyboard',
        'requests',
        'pystray',
        'cryptography',
        'pyperclip'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Snap-Solver',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/app_icon.ico'
)
'''
        with open('snap-solver.spec', 'w') as f:
            f.write(spec_content)

    def build_executable(self):
        """Build the final executable"""
        logging.info("Building executable...")
        subprocess.run([
            'pyinstaller',
            '--clean',
            '--noconfirm',
            'snap-solver.spec'
        ], check=True)

    def package_node(self):
        """Package Node.js runtime"""
        logging.info("Packaging Node.js runtime...")
        # Download and extract Node.js binary
        # This would need to be implemented based on the platform
        pass

    def build(self):
        """Main build process"""
        try:
            logging.info("Starting build process...")
            
            # Clean up
            self.clean_directories()
            
            # Install dependencies
            self.install_python_dependencies()
            self.install_node_dependencies()
            
            # Create version file
            self.create_version_file()
            
            # Bundle frontend
            self.bundle_frontend()
            
            # Package Node.js
            self.package_node()
            
            # Create and run PyInstaller spec
            self.create_pyinstaller_spec()
            self.build_executable()
            
            logging.info("Build completed successfully!")
            return True
            
        except Exception as e:
            logging.error(f"Build failed: {str(e)}")
            return False

def main():
    builder = SnapSolverBuilder()
    success = builder.build()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()