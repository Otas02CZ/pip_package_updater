# Pip Package Updater

A simple yet powerful Python script to update all your installed pip packages at once.

## Features

- Automatically detects and uses the correct Python/pip command for your system
- Updates pip itself before updating other packages
- Handles package parsing with proper error messages
- Provides progress information during updates
- Command-line options for more control:
  - Update packages one by one for better error reporting
  - Exclude specific packages from updates
  - Only update specific packages
  - Skip updating pip itself

## Requirements

- Python 3.6 or later

## Usage

Basic usage (updates all packages):
```bash
python pip_package_updater.py
```

With options:
```bash
# Update packages one by one (slower but shows which ones failed)
python pip_package_updater.py --one-by-one

# Skip updating pip itself
python pip_package_updater.py --skip-pip-update

# Exclude specific packages
python pip_package_updater.py --exclude package1 package2

# Only update specific packages
python pip_package_updater.py --only package1 package2
```

## License

MIT
