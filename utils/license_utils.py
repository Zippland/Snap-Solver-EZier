import hashlib
import platform
import subprocess
import json
from datetime import datetime, timedelta
import base64
from cryptography.fernet import Fernet
import winreg
import os

class LicenseUtils:
    def __init__(self, secret_key=None):
        # 使用固定的密钥
        self._secret_key = b'cJ-JE8cG-NAHbYfFszoxnCl0sy6cIZXZUiJKqYPNs5w='
        self._cipher_suite = Fernet(self._secret_key)
        
    def get_machine_code(self):
        """获取机器的唯一标识码"""
        try:
            # 获取CPU信息
            def get_cpu_info():
                if platform.system() == "Windows":
                    try:
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                           r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                        cpu_id = winreg.QueryValueEx(key, "ProcessorNameString")[0]
                        winreg.CloseKey(key)
                        return cpu_id
                    except:
                        return platform.processor()
                else:
                    return platform.processor()

            # 获取主板序列号（仅Windows）
            def get_motherboard_serial():
                if platform.system() == "Windows":
                    try:
                        result = subprocess.check_output(
                            'wmic baseboard get serialnumber', 
                            shell=True
                        ).decode()
                        return result.split('\n')[1].strip()
                    except:
                        return ""
                return ""

            # 获取硬盘序列号
            def get_disk_serial():
                if platform.system() == "Windows":
                    try:
                        result = subprocess.check_output(
                            'wmic diskdrive get serialnumber', 
                            shell=True
                        ).decode()
                        return result.split('\n')[1].strip()
                    except:
                        return ""
                else:
                    try:
                        result = subprocess.check_output(
                            'system_profiler SPHardwareDataType | grep "Serial Number"',
                            shell=True
                        ).decode()
                        return result.strip()
                    except:
                        return ""

            # 组合硬件信息
            hardware_info = {
                'cpu': get_cpu_info(),
                'motherboard': get_motherboard_serial(),
                'disk': get_disk_serial(),
                'platform': platform.platform(),
                'node': platform.node()
            }

            # 生成机器码
            machine_str = json.dumps(hardware_info, sort_keys=True)
            machine_hash = hashlib.sha256(machine_str.encode()).hexdigest()
            return machine_hash
        except Exception as e:
            print(f"Error getting machine code: {str(e)}")
            return None

    def generate_license_key(self, machine_code, valid_days=365):
        """生成许可证密钥"""
        try:
            # 创建许可证数据
            license_data = {
                'machine_code': machine_code,
                'creation_date': datetime.now().isoformat(),
                'expiration_date': (datetime.now() + timedelta(days=valid_days)).isoformat(),
                'version': '1.0'
            }

            # 序列化并加密
            json_data = json.dumps(license_data)
            encrypted_data = self._cipher_suite.encrypt(json_data.encode())
            
            # 转换为可读的字符串
            license_key = base64.urlsafe_b64encode(encrypted_data).decode()
            return license_key
        except Exception as e:
            print(f"Error generating license key: {str(e)}")
            return None

    def verify_license_key(self, license_key):
        """验证许可证密钥"""
        try:
            # 解码并解密
            encrypted_data = base64.urlsafe_b64decode(license_key.strip())
            decrypted_data = self._cipher_suite.decrypt(encrypted_data)
            license_data = json.loads(decrypted_data)

            # 验证机器码
            current_machine_code = self.get_machine_code()
            if current_machine_code is None:
                return False, "无法获取机器码"
                
            if license_data['machine_code'] != current_machine_code:
                return False, "无效的机器码，该许可证不适用于此设备"

            # 验证有效期
            expiration_date = datetime.fromisoformat(license_data['expiration_date'])
            if datetime.now() > expiration_date:
                return False, "许可证已过期"

            return True, "许可证有效"
        except Exception as e:
            print(f"License verification error: {str(e)}")
            return False, f"无效的许可证密钥: {str(e)}"

    def save_license(self, license_key):
        """保存许可证到本地"""
        try:
            # 先验证许可证
            is_valid, message = self.verify_license_key(license_key)
            if not is_valid:
                print(f"Attempting to save invalid license: {message}")
                return False

            # 获取用户主目录
            home_dir = os.path.expanduser("~")
            license_path = os.path.join(home_dir, '.snap_solver_license')
            
            with open(license_path, 'w') as f:
                f.write(license_key.strip())
            return True
        except Exception as e:
            print(f"Error saving license: {str(e)}")
            return False

    def load_license(self):
        """从本地加载许可证"""
        try:
            # 获取用户主目录
            home_dir = os.path.expanduser("~")
            license_path = os.path.join(home_dir, '.snap_solver_license')
            
            if os.path.exists(license_path):
                with open(license_path, 'r') as f:
                    license_key = f.read().strip()
                    # 加载时验证许可证
                    is_valid, _ = self.verify_license_key(license_key)
                    if is_valid:
                        return license_key
                    else:
                        print("Loaded license is invalid")
                        return None
            return None
        except Exception as e:
            print(f"Error loading license: {str(e)}")
            return None