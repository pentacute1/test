import os
import shutil
import ctypes
import platform
from pathlib import Path

def print_ascii_art():
    art = r"""
  ____  _______     _______    _______  _______ 
 / ___||  ___\ \   / / ____|  | ____\ \/ / ____|
 \___ \| |_   \ \ / /|  _|    |  _|  \  /|  _|  
  ___) |  _|   \ V / | |___   | |___ /  \| |___ 
 |____/|_|      \_/  |_____|  |_____/_/\_\_____|
                                               
"""
    print(art)
    print("Welcome to SEV CLEANER!\n")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def clean_temp_dirs():
    temp_dirs = [
        os.environ.get('TEMP'),
        os.environ.get('TMP'),
        '/var/tmp',
        '/tmp'
    ]

    for temp_dir in temp_dirs:
        if temp_dir and os.path.isdir(temp_dir):
            print(f'Cleaning temporary directory: {temp_dir}')
            try:
                for item in Path(temp_dir).iterdir():
                    try:
                        if item.is_file() or item.is_symlink():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                    except Exception as e:
                        print(f'Could not delete {item}: {e}')
            except Exception as e:
                print(f'Error accessing {temp_dir}: {e}')

def empty_recycle_bin():
    if platform.system() == 'Windows':
        try:
            import winshell
            print('Emptying Recycle Bin...')
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        except ImportError:
            print('winshell module not found. Skipping Recycle Bin cleanup.')
        except Exception as e:
            print(f'Error emptying Recycle Bin: {e}')
    else:
        print('Recycle Bin cleanup is only supported on Windows.')

def clean_browser_cache():
    user_home = Path.home()
    browsers = {
        'Chrome': user_home / 'AppData/Local/Google/Chrome/User Data/Default/Cache',
        'Firefox': user_home / 'AppData/Local/Mozilla/Firefox/Profiles'
    }

    for browser, path in browsers.items():
        if path.exists():
            print(f'Cleaning {browser} cache at {path}')
            try:
                shutil.rmtree(path)
            except Exception as e:
                print(f'Could not clean {browser} cache: {e}')
        else:
            print(f'{browser} cache directory not found at {path}')

def remove_log_files():
    log_dirs = [
        Path('/var/log'),
        Path.home() / 'AppData/Local'  # For Windows
    ]

    for log_dir in log_dirs:
        if log_dir.exists():
            print(f'Cleaning log files in {log_dir}')
            for log_file in log_dir.rglob('*.log'):
                try:
                    log_file.unlink()
                    print(f'Deleted log file: {log_file}')
                except Exception as e:
                    print(f'Could not delete {log_file}: {e}')
        else:
            print(f'Log directory not found: {log_dir}')

if __name__ == '__main__':
    print_ascii_art()
    
    if platform.system() == 'Windows' and not is_admin():
        print('This script requires administrative privileges. Please run as administrator.')
    else:
        clean_temp_dirs()
        empty_recycle_bin()
        clean_browser_cache()
        remove_log_files()
        print('System cleaning completed.')
