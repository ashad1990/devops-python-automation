# Python Commands Cheat Sheet

Quick reference for Python, pip, and virtual environment commands used in DevOps automation.

## Table of Contents

- [Python CLI](#python-cli)
- [pip Commands](#pip-commands)
- [Virtual Environment Commands](#virtual-environment-commands)
- [Running Python Code](#running-python-code)
- [Package Management](#package-management)
- [Common DevOps Snippets](#common-devops-snippets)

---

## Python CLI

### Version & Help
```bash
# Check Python version
python --version
python3 --version

# Get help
python --help
python -h

# Interactive shell
python
python3

# Check where Python is installed
which python
which python3

# Show Python path
python -c "import sys; print(sys.executable)"
```

### Execute Code
```bash
# Execute string
python -c "print('Hello')"

# Execute module as script
python -m module_name

# Run with unbuffered output (for Docker/logs)
python -u script.py

# Enable debug mode
python -d script.py

# Verbose import tracing
python -v script.py
```

---

## pip Commands

### Installation
```bash
# Install package
pip install package_name

# Install specific version
pip install package_name==1.2.3

# Install minimum version
pip install 'package_name>=1.2.3'

# Install from requirements file
pip install -r requirements.txt

# Install in editable mode (for development)
pip install -e .

# Install with extras
pip install 'package_name[extra1,extra2]'
```

### Upgrade & Uninstall
```bash
# Upgrade package
pip install --upgrade package_name
pip install -U package_name

# Upgrade pip itself
pip install --upgrade pip

# Uninstall package
pip uninstall package_name

# Uninstall all packages
pip freeze | xargs pip uninstall -y
```

### Information
```bash
# List installed packages
pip list

# List outdated packages
pip list --outdated

# Show package details
pip show package_name

# Show package dependencies
pip show -f package_name

# Search packages (deprecated, use pypi.org)
# pip search package_name
```

### Requirements Management
```bash
# Generate requirements.txt
pip freeze > requirements.txt

# Generate minimal requirements (only top-level)
pip list --format=freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Upgrade all packages in requirements
pip install -r requirements.txt --upgrade
```

### Cache
```bash
# Clear pip cache
pip cache purge

# Show cache info
pip cache info

# List cached packages
pip cache list
```

---

## Virtual Environment Commands

### venv (Built-in)

```bash
# Create virtual environment
python3 -m venv env_name
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows Git Bash/WSL)
source venv/Scripts/activate

# Deactivate
deactivate

# Remove virtual environment
rm -rf venv
```

### virtualenv

```bash
# Install virtualenv
pip install virtualenv

# Create environment
virtualenv myenv

# Create with specific Python version
virtualenv -p python3.11 myenv
virtualenv -p /usr/bin/python3.11 myenv

# Activate/deactivate (same as venv)
source myenv/bin/activate
deactivate
```

### poetry

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create new project
poetry new myproject

# Initialize in existing directory
poetry init

# Add dependency
poetry add requests
poetry add --dev pytest

# Install dependencies
poetry install

# Update dependencies
poetry update

# Show dependencies
poetry show

# Activate shell
poetry shell

# Run command in virtual environment
poetry run python script.py
poetry run pytest

# Export requirements.txt
poetry export -f requirements.txt --output requirements.txt
```

---

## Running Python Code

### Execute Scripts
```bash
# Run Python file
python script.py
python3 script.py

# Run with arguments
python script.py arg1 arg2 --flag

# Make script executable and run directly
chmod +x script.py
./script.py  # Requires shebang: #!/usr/bin/env python3

# Run module as script
python -m my_module

# Run with specific Python version
python3.11 script.py
```

### Interactive Mode
```bash
# Start Python REPL
python
python3

# Execute file in interactive mode
python -i script.py

# Start with no site packages
python -S

# Exit REPL
exit()
quit()
# Or Ctrl+D (Linux/macOS), Ctrl+Z then Enter (Windows)
```

### One-Liners
```bash
# Print Python version
python -c "import sys; print(sys.version)"

# Check if module is available
python -c "import requests; print('requests installed')"

# Simple HTTP server (for testing)
python -m http.server 8000

# JSON pretty print
echo '{"name":"value"}' | python -m json.tool

# Base64 encode
echo "text" | python -c "import sys, base64; print(base64.b64encode(sys.stdin.read().encode()).decode())"
```

---

## Package Management

### Common DevOps Packages

```bash
# HTTP/API
pip install requests

# YAML parsing
pip install pyyaml

# Cloud - GCP
pip install google-cloud-storage
pip install google-cloud-compute
pip install google-cloud-bigquery

# Cloud - AWS (if needed)
pip install boto3

# Docker
pip install docker

# Kubernetes
pip install kubernetes

# Testing
pip install pytest
pip install pytest-cov  # Coverage
pip install pytest-mock  # Mocking

# CLI tools
pip install click
pip install rich  # Beautiful terminal output

# Utilities
pip install python-dotenv  # .env file support
pip install jinja2  # Templating
```

### Install All Course Dependencies

```bash
# From requirements.txt
pip install -r requirements.txt

# Or install individually
pip install requests pyyaml google-cloud-storage \
    google-cloud-compute docker kubernetes pytest click
```

---

## Common DevOps Snippets

### Environment Check
```bash
# Verify Python installation
python --version && pip --version

# List all installed packages with versions
pip freeze

# Check specific package version
pip show requests | grep Version
```

### Virtual Environment Setup
```bash
# Complete setup workflow
python3 -m venv devops-env
source devops-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip list
```

### Quick Script Template
```bash
# Create executable Python script
cat > script.py << 'EOF'
#!/usr/bin/env python3
"""Script description."""

import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('--input', required=True, help='Input file')
    args = parser.parse_args()
    
    logger.info(f"Processing {args.input}")
    # Your code here
    
    sys.exit(0)

if __name__ == "__main__":
    main()
EOF

chmod +x script.py
```

### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest test_script.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run with verbose output
pytest -v

# Run specific test function
pytest test_script.py::test_function_name
```

### Module Imports Test
```bash
# Test if all dependencies are available
python << 'EOF'
import sys

modules = ['requests', 'yaml', 'docker', 'kubernetes', 'pytest', 'click']
missing = []

for module in modules:
    try:
        __import__(module)
        print(f"✓ {module}")
    except ImportError:
        print(f"✗ {module}")
        missing.append(module)

if missing:
    print(f"\nMissing modules: {', '.join(missing)}")
    sys.exit(1)
else:
    print("\n✓ All modules available!")
    sys.exit(0)
EOF
```

### Environment Variables
```bash
# Set environment variable for Python
export PYTHONPATH=/path/to/modules

# Set Python to unbuffered (useful for Docker)
export PYTHONUNBUFFERED=1

# Disable .pyc files
export PYTHONDONTWRITEBYTECODE=1

# Use in script
python -c "import os; print(os.getenv('MY_VAR', 'default'))"
```

### Debugging
```bash
# Run with Python debugger
python -m pdb script.py

# Start debugger on exception
python -m pdb -c continue script.py

# Run with warnings
python -W all script.py

# Show deprecation warnings
python -W default script.py
```

### Performance Profiling
```bash
# Profile script execution
python -m cProfile script.py

# Profile with detailed output
python -m cProfile -s cumulative script.py

# Time execution
time python script.py
```

### Package Publishing (if creating tools)
```bash
# Create source distribution
python setup.py sdist

# Create wheel
python setup.py bdist_wheel

# Upload to PyPI
pip install twine
twine upload dist/*
```

---

## Keyboard Shortcuts (Python REPL)

```
Ctrl+D          Exit Python shell (Linux/macOS)
Ctrl+Z + Enter  Exit Python shell (Windows)
Ctrl+C          Keyboard interrupt
Ctrl+L          Clear screen
Tab             Auto-complete
↑ / ↓           Command history
```

---

## Useful Environment Variables

```bash
# Common Python environment variables
export PYTHONPATH=/path/to/modules        # Add to module search path
export PYTHONHOME=/path/to/python         # Python installation location
export PYTHONSTARTUP=~/.pythonrc          # Run this script on REPL start
export PYTHONUNBUFFERED=1                 # Force stdout/stderr to be unbuffered
export PYTHONDONTWRITEBYTECODE=1          # Don't create .pyc files
export PYTHONIOENCODING=utf-8             # Set encoding for stdin/stdout/stderr
export PYTHONINSPECT=1                    # Start REPL after script execution
export PYTHONWARNINGS=default             # Warning control
```

---

## Quick Troubleshooting

```bash
# Package not found
pip install --upgrade pip
pip install package_name

# Permission denied
pip install --user package_name
# Or use virtual environment

# Multiple Python versions
python3 --version
python3.11 --version
which python3

# Check pip association with Python
python3 -m pip --version

# Fix broken pip
python3 -m ensurepip --upgrade

# Clear Python cache files
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

---

## Next Steps

- For installation details: [SETUP.md](SETUP.md)
- For concepts: [CONCEPTS.md](CONCEPTS.md)
- For troubleshooting: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Start coding: [QUICK-START.md](QUICK-START.md)
