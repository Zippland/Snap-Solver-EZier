import os
import sys
import requests
import tempfile
import zipfile
import platform
import subprocess
import shutil
from pathlib import Path

class NodePackager:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir)
        self.temp_dir = Path(tempfile.mkdtemp())
        self.node_version = '20.11.1'  # LTS version
        
    def get_download_url(self):
        """Get the appropriate Node.js download URL based on platform"""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if system == 'windows':
            arch = 'x64' if machine.endswith('64') else 'x86'
            return f'https://nodejs.org/dist/v{self.node_version}/node-v{self.node_version}-win-{arch}.zip'
        elif system == 'darwin':
            arch = 'arm64' if machine == 'arm64' else 'x64'
            return f'https://nodejs.org/dist/v{self.node_version}/node-v{self.node_version}-darwin-{arch}.tar.gz'
        else:  # Linux
            arch = 'arm64' if machine == 'aarch64' else 'x64'
            return f'https://nodejs.org/dist/v{self.node_version}/node-v{self.node_version}-linux-{arch}.tar.xz'

    def download_node(self):
        """Download Node.js binary"""
        url = self.get_download_url()
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        download_path = self.temp_dir / os.path.basename(url)
        with open(download_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return download_path

    def extract_node(self, archive_path):
        """Extract Node.js archive"""
        extract_dir = self.temp_dir / 'node'
        
        if archive_path.suffix == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        else:
            if archive_path.suffix == '.xz':
                import tarfile
                import lzma
                with lzma.open(archive_path) as f:
                    with tarfile.open(fileobj=f) as tar:
                        tar.extractall(extract_dir)
            else:  # .tar.gz
                import tarfile
                with tarfile.open(archive_path, 'r:gz') as tar:
                    tar.extractall(extract_dir)
                    
        return extract_dir

    def copy_node_files(self, extracted_dir):
        """Copy necessary Node.js files to target directory"""
        # Find the node directory (it's usually nested one level)
        node_dir = next(extracted_dir.glob('node-*'))
        
        # Create node directory in target
        node_target = self.target_dir / 'node'
        node_target.mkdir(parents=True, exist_ok=True)
        
        # Copy necessary files
        if platform.system().lower() == 'windows':
            shutil.copy2(node_dir / 'node.exe', node_target)
            shutil.copy2(node_dir / 'npm.cmd', node_target)
            shutil.copytree(node_dir / 'node_modules', node_target / 'node_modules', dirs_exist_ok=True)
        else:
            shutil.copy2(node_dir / 'bin' / 'node', node_target)
            shutil.copy2(node_dir / 'bin' / 'npm', node_target)
            shutil.copytree(node_dir / 'lib', node_target / 'lib', dirs_exist_ok=True)

    def cleanup(self):
        """Clean up temporary files"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def package(self):
        """Package Node.js for distribution"""
        try:
            print("Downloading Node.js...")
            archive_path = self.download_node()
            
            print("Extracting Node.js...")
            extracted_dir = self.extract_node(archive_path)
            
            print("Copying Node.js files...")
            self.copy_node_files(extracted_dir)
            
            print("Node.js packaging completed successfully!")
            return True
            
        except Exception as e:
            print(f"Error packaging Node.js: {str(e)}")
            return False
            
        finally:
            self.cleanup()

def main():
    if len(sys.argv) != 2:
        print("Usage: python node_packager.py <target_directory>")
        sys.exit(1)
        
    packager = NodePackager(sys.argv[1])
    success = packager.package()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()