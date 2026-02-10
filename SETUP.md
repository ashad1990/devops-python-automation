# Python Development Environment Setup

Complete guide for setting up Python development environment across different operating systems.

## Table of Contents

- [macOS Setup](#macos-setup)
- [Linux Setup](#linux-setup)
- [Windows WSL2 Setup](#windows-wsl2-setup)
- [Virtual Environments](#virtual-environments)
- [Package Management](#package-management)
- [IDE Setup](#ide-setup)
- [Verification](#verification)

---

## macOS Setup

### Option 1: Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python@3.11

# Verify installation
python3 --version
pip3 --version
```

### Option 2: pyenv (Multiple Python Versions)

```bash
# Install pyenv via Homebrew
brew install pyenv

# Add to shell profile (~/.zshrc or ~/.bash_profile)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Install Python version
pyenv install 3.11.0
pyenv global 3.11.0

# Verify
python --version
```

---

## Linux Setup

### Ubuntu/Debian (apt)

```bash
# Update package list
sudo apt update

# Install Python 3.11 and pip
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install additional development tools
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

# Create symlinks (optional)
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Verify
python --version
pip --version
```

### RHEL/CentOS/Fedora (yum/dnf)

```bash
# For RHEL 8/CentOS 8/Fedora
sudo dnf install -y python3.11 python3.11-pip python3.11-devel

# Or for older versions (RHEL 7/CentOS 7)
sudo yum install -y python3 python3-pip python3-devel

# Install development tools
sudo dnf groupinstall -y "Development Tools"

# Verify
python3 --version
pip3 --version
```

### Using pyenv on Linux

```bash
# Install dependencies
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Install pyenv
curl https://pyenv.run | bash

# Add to ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reload shell
source ~/.bashrc

# Install Python
pyenv install 3.11.0
pyenv global 3.11.0
```

---

## Windows WSL2 Setup

### Install WSL2

```powershell
# In PowerShell (Administrator)
wsl --install -d Ubuntu-22.04

# Restart computer if prompted
# Launch Ubuntu from Start menu
```

### Install Python in WSL2

```bash
# Inside WSL2 Ubuntu terminal
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y build-essential

# Verify
python3 --version
pip3 --version
```

---

## Virtual Environments

### venv (Built-in, Recommended for Beginners)

```bash
# Create virtual environment
python3 -m venv devops-env

# Activate (macOS/Linux)
source devops-env/bin/activate

# Activate (Windows WSL)
source devops-env/bin/activate

# Deactivate
deactivate

# Install packages in venv
pip install requests pyyaml
```

### virtualenv (More Features)

```bash
# Install virtualenv
pip install virtualenv

# Create environment
virtualenv myenv

# Or specify Python version
virtualenv -p python3.11 myenv

# Activate/deactivate same as venv
source myenv/bin/activate
deactivate
```

### poetry (Modern Dependency Management)

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Create new project
poetry new myproject
cd myproject

# Or initialize in existing directory
poetry init

# Install dependencies
poetry install

# Add packages
poetry add requests pyyaml

# Activate virtual environment
poetry shell

# Run commands
poetry run python script.py
```

---

## Package Management

### pip Basics

```bash
# Install package
pip install requests

# Install specific version
pip install requests==2.28.0

# Install from requirements.txt
pip install -r requirements.txt

# Upgrade package
pip install --upgrade requests

# Uninstall package
pip uninstall requests

# List installed packages
pip list

# Show package details
pip show requests

# Freeze dependencies
pip freeze > requirements.txt
```

### Creating requirements.txt for This Course

```bash
# Create virtual environment
python3 -m venv devops-env
source devops-env/bin/activate

# Install all course dependencies
pip install -r requirements.txt

# Or install individually
pip install requests pyyaml google-cloud-storage google-cloud-compute \
    docker kubernetes pytest click
```

---

## IDE Setup

### Visual Studio Code (Recommended)

```bash
# Download from https://code.visualstudio.com/

# Install Python extension
# 1. Open VS Code
# 2. Press Ctrl+Shift+X (Cmd+Shift+X on macOS)
# 3. Search "Python"
# 4. Install "Python" by Microsoft
```

**VS Code Configuration:**

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./devops-env/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "editor.rulers": [79],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

**Recommended VS Code Extensions:**
- Python (Microsoft)
- Pylance (Microsoft)
- Python Indent
- autoDocstring
- GitLens
- YAML

### PyCharm

```bash
# Download PyCharm Community (free) or Professional
# https://www.jetbrains.com/pycharm/download/

# Configure interpreter
# File > Settings > Project > Python Interpreter
# Click gear icon > Add > Virtualenv Environment
# Select existing environment: ./devops-env
```

---

## Verification

### Verify Python Installation

```bash
# Check Python version (should be 3.9+)
python --version
python3 --version

# Check pip
pip --version
pip3 --version

# Test Python interactive shell
python3
>>> print("Hello DevOps!")
>>> exit()
```

### Verify Virtual Environment

```bash
# Create and activate venv
python3 -m venv test-env
source test-env/bin/activate

# Check you're in venv (prompt should show (test-env))
which python
# Should show path to test-env/bin/python

# Install test package
pip install requests

# Verify installation
python -c "import requests; print(requests.__version__)"

# Deactivate
deactivate

# Clean up
rm -rf test-env
```

### Verify Course Dependencies

```bash
# Activate your course environment
source devops-env/bin/activate

# Test imports
python3 << 'EOF'
import sys
import requests
import yaml
import docker
import kubernetes
import pytest
import click

print("✓ All course dependencies installed successfully!")
print(f"Python version: {sys.version}")
EOF
```

### Run Sample Script

```bash
# Create test script
cat > test_setup.py << 'EOF'
#!/usr/bin/env python3
"""Test script to verify Python setup for DevOps automation."""

import sys
import platform

def main():
    print("=" * 50)
    print("Python DevOps Environment Verification")
    print("=" * 50)
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    print("=" * 50)
    
    # Test imports
    try:
        import requests
        print("✓ requests library available")
    except ImportError:
        print("✗ requests library missing")
    
    try:
        import yaml
        print("✓ PyYAML library available")
    except ImportError:
        print("✗ PyYAML library missing")
    
    print("=" * 50)
    print("Setup verification complete!")

if __name__ == "__main__":
    main()
EOF

# Make executable and run
chmod +x test_setup.py
python test_setup.py
```

## Common Setup Commands

```bash
# Full setup workflow
python3 -m venv devops-env
source devops-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip list

# Quick environment recreation
deactivate
rm -rf devops-env
python3 -m venv devops-env
source devops-env/bin/activate
pip install -r requirements.txt
```

## Environment Variables

```bash
# Add to ~/.bashrc or ~/.zshrc for convenience

# Python aliases
alias python=python3
alias pip=pip3

# Auto-activate environment when entering project directory
cd() {
    builtin cd "$@"
    if [[ -f "devops-env/bin/activate" ]]; then
        source devops-env/bin/activate
    fi
}
```

## Next Steps

1. Verify all installations successful
2. Proceed to [QUICK-START.md](QUICK-START.md)
3. Complete setup checklist in [LAB-01](LABS/LAB-01-python-basics.md)

## Troubleshooting

If you encounter issues, refer to [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
