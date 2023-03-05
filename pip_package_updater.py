# FILE: pip.package_updater.py
# AUTHOR: Otas02CZ
# DATE: 2023
# LICENSE: MIT
# INFO: Simple python script to update all installed pip packages

from subprocess import run, call, PIPE
import os

print("Tool for updating installed pip packages - v0.1")
match os.name:
    case "nt":
        result: str = str(run("pip freeze", stdout=PIPE).stdout)[2:-2]
        packages: list[str] = [package_version[:package_version.index("=")] for package_version in result.split("\\r\\n")]
        call(f"python.exe -m pip install --upgrade {' '.join(packages)}")
    case "posix":
        result: str = str(run(["python3", "-m","pip", "freeze"], stdout=PIPE).stdout)[2:-2]
        packages: list[str] = [package_version[:package_version.index("=")] for package_version in result.split("\\n")]
        command: list[str] = ["python3", "-m", "pip", "install", "--upgrade"] + packages
        call(command)
