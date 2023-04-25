# FILE: pip.package_updater.py
# AUTHOR: Otas02CZ
# DATE: 2023
# LICENSE: MIT
# INFO: Simple python script to update all installed pip packages

import sys
import subprocess

# Determine the operating system
if sys.platform.startswith("win"):
    newline = "\r\n"
else:
    newline = "\n"

print("Tool for updating installed pip packages - v0.1")

# List outdated packages
output = subprocess.check_output(["pip", "list", "--outdated"]).decode()

# Extract package names
packages = [line.split()[0] for line in output.split(newline)[2:-1]]

# Update packages
subprocess.check_call(["pip", "install", "--upgrade"] + packages)