# FILE: pip.package_updater.py
# AUTHOR: Otas02CZ
# DATE: 2023
# LICENSE: MIT
# INFO: Simple python script to update all installed pip packages

import argparse
import os
import sys
import subprocess
import re
from typing import List, Optional, Tuple


def get_pip_command() -> List[str]:
    """Returns the appropriate pip command based on the system"""
    if os.name == "nt":  # Windows
        return ["python", "-m", "pip"]
    else:  # POSIX systems (Linux, macOS)
        return ["python3", "-m", "pip"]


def get_installed_packages(pip_cmd: List[str], exclude: List[str]) -> List[str]:
    """Get all installed packages excluding those in the exclude list"""
    try:
        result = subprocess.run(pip_cmd + ["freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        packages = []
        for line in result.stdout.splitlines():
            # Skip editable packages or git/url based packages
            if line.startswith("-e ") or "git+" in line or "http://" in line or "https://" in line:
                continue

            # Extract package name (everything before == or >=)
            match = re.match(r'^([A-Za-z0-9_\-\.]+)', line)
            if match and match.group(1).lower() not in [pkg.lower() for pkg in exclude]:
                packages.append(match.group(1))

        return packages
    except subprocess.CalledProcessError as e:
        print(f"Error getting installed packages: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)


def update_pip(pip_cmd: List[str]) -> None:
    """Update pip itself"""
    print("Updating pip itself...")
    try:
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], check=True)
        print("Pip successfully updated.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update pip: {e}")


def update_packages(pip_cmd: List[str], packages: List[str], one_by_one: bool = False) -> None:
    """Update packages either all at once or one by one"""
    if not packages:
        print("No packages to update.")
        return

    print(f"Updating {len(packages)} packages...")

    if one_by_one:
        successful = []
        failed = []

        for i, package in enumerate(packages, 1):
            print(f"[{i}/{len(packages)}] Updating {package}...")
            try:
                subprocess.run(pip_cmd + ["install", "--upgrade", package], check=True)
                successful.append(package)
            except subprocess.CalledProcessError:
                print(f"Failed to update {package}")
                failed.append(package)

        print(f"\nUpdate summary: {len(successful)} successful, {len(failed)} failed")
        if failed:
            print("Failed packages:")
            for package in failed:
                print(f"  - {package}")
    else:
        # Update all packages at once
        try:
            subprocess.run(pip_cmd + ["install", "--upgrade"] + packages, check=True)
            print("All packages successfully updated.")
        except subprocess.CalledProcessError as e:
            print(f"Error during package update: {e}")
            print("Try using the --one-by-one option to identify problematic packages.")


def main():
    parser = argparse.ArgumentParser(description="Update all installed pip packages")
    parser.add_argument("--version", action="version", version="pip_package_updater v0.2")
    parser.add_argument("--skip-pip-update", action="store_true", help="Skip updating pip itself")
    parser.add_argument("--one-by-one", action="store_true",
                       help="Update packages one by one (slower but better error reporting)")
    parser.add_argument("--exclude", type=str, nargs="+", default=[],
                       help="Packages to exclude from updating")
    parser.add_argument("--only", type=str, nargs="+", default=[],
                       help="Only update these specific packages")

    args = parser.parse_args()

    # Get the appropriate pip command for this system
    pip_cmd = get_pip_command()

    # Update pip itself first, unless skipped
    if not args.skip_pip_update:
        update_pip(pip_cmd)

    # Get all installed packages
    all_packages = get_installed_packages(pip_cmd, args.exclude)

    # Filter to only requested packages if specified
    packages_to_update = [pkg for pkg in all_packages if not args.only or pkg.lower() in
                         [only_pkg.lower() for only_pkg in args.only]]

    if not packages_to_update:
        print("No packages to update.")
        return

    # Update the packages
    update_packages(pip_cmd, packages_to_update, args.one_by_one)


if __name__ == "__main__":
    main()
