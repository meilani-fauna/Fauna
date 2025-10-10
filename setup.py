#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: @anbuinfosec
GitHub: https://github.com/meilani-fauna/Fauna
License: MIT License
Disclaimer:
    This tool is for educational and authorized penetration testing only.  
    Do NOT use on unauthorized networks.  
    The author is not responsible for any misuse.
"""

import os
import sys
import subprocess
from colors import green, yellow, red, reset

red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
reset = "\033[0m"

RED = red
GREEN = green
YELLOW = yellow
RESET = reset

SCRIPT_NAME = 'main.py'
MODULE_NAME = 'eka'
BIN_NAME = 'eka'

def is_termux():
    return os.getenv("PREFIX", "").startswith("/data/data/com.termux/files/usr")

def print_info(msg):
    print(f"{green}[+]{reset} {msg}")

def print_warn(msg):
    print(f"{yellow}[!]{reset} {msg}")

def print_error(msg):
    print(f"{red}[-]{reset} {msg}")

def install_script():
    if not is_termux():
        print_warn("You don't appear to be running inside Termux. Paths may be incorrect.")
        sys.exit(1)

    prefix = sys.prefix
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"

    bin_path = os.path.join(prefix, 'bin', BIN_NAME)
    lib_path = os.path.join(prefix, 'lib', python_version, SCRIPT_NAME)

    launcher_code = f'''#!/data/data/com.termux/files/usr/bin/python3
import runpy
if __name__ == "__main__":
    runpy.run_path("/data/data/com.termux/files/usr/lib/python3.12/main.py", run_name="__main__")
'''

    try:
        with open(bin_path, 'w') as f:
            f.write(launcher_code)
        os.chmod(bin_path, 0o775)
        print_info(f"Launcher script installed at {bin_path}")
        files_to_copy = [
            '.flake8',
            'config.txt',
            'main.py',
            'colors.py',
            'update.py',
            'vulnwsc.txt'
        ]

        for filename in files_to_copy:
            src_path = filename
            dst_path = os.path.join(prefix, 'lib', python_version, filename)
            try:
                with open(src_path, 'r') as src, open(dst_path, 'w') as dst:
                    dst.write(src.read())
                print_info(f"Copied {filename} to {dst_path}")
            except Exception as e:
                print_warn(f"Failed to copy {filename}: {e}")

        print_info(f"Installed successfully! Run the tool with: {BIN_NAME}")
        print_info("Showing usage:\n")

        subprocess.run([bin_path, '--help'], check=False)
    except Exception as e:
        print_error(f"Installation failed: {e}")

def uninstall_script():
    prefix = sys.prefix
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"

    bin_path = os.path.join(prefix, 'bin', BIN_NAME)
    lib_path = os.path.join(prefix, 'lib', python_version, SCRIPT_NAME)

    for path in [bin_path, lib_path]:
        try:
            os.remove(path)
            print_info(f"Removed: {path}")
        except FileNotFoundError:
            print_warn(f"File not found, skipping: {path}")
        except Exception as e:
            print_error(f"Error removing {path}: {e}")

def main():
    if len(sys.argv) != 2:
        print(f"{yellow}Usage: python3 setup.py [install | uninstall]{reset}")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == 'install':
        install_script()
    elif cmd == 'uninstall':
        uninstall_script()
    else:
        print_error("Unknown command. Use 'install' or 'uninstall'.")

if __name__ == '__main__':
    main()
