# Troubleshooting Guide

Common issues when learning Python for DevOps and their solutions.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Virtual Environment Issues](#virtual-environment-issues)
- [Package Installation Issues](#package-installation-issues)
- [Import Errors](#import-errors)
- [Python Version Issues](#python-version-issues)
- [IDE/Editor Issues](#ideeditor-issues)
- [Script Execution Issues](#script-execution-issues)
- [Common DevOps-Specific Issues](#common-devops-specific-issues)
- [Cloud SDK Issues](#cloud-sdk-issues)
- [Docker/Kubernetes Client Issues](#dockerkubernetes-client-issues)

---

## Installation Issues

### Issue: `python: command not found`

**Problem:** Python not installed or not in PATH

**Solution:**
```bash
# Check if python3 is available
which python3

# If available, create alias
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc

# Or install Python (see SETUP.md)
# Ubuntu/Debian
sudo apt install python3

# macOS
brew install python@3.11
```

### Issue: `pip: command not found`

**Problem:** pip not installed

**Solution:**
```bash
# Try pip3
which pip3

# Create alias
alias pip=pip3

# Install pip
python3 -m ensurepip --upgrade

# Or use package manager
sudo apt install python3-pip  # Ubuntu/Debian
brew install python3          # macOS includes pip
```

### Issue: Permission Denied Installing Packages

**Problem:** Trying to install globally without sudo

**Solution:**
```bash
# Option 1: Use --user flag
pip install --user package_name

# Option 2: Use virtual environment (RECOMMENDED)
python3 -m venv venv
source venv/bin/activate
pip install package_name

# Option 3: Use sudo (NOT RECOMMENDED)
sudo pip install package_name  # Avoid this
```

---

## Virtual Environment Issues

### Issue: `source venv/bin/activate` does nothing

**Problem:** Wrong shell or directory

**Solution:**
```bash
# Make sure you're in the right directory
ls venv/bin/activate  # File should exist

# Try absolute path
source /full/path/to/venv/bin/activate

# For fish shell
source venv/bin/activate.fish

# For csh/tcsh
source venv/bin/activate.csh

# Check if activated
which python  # Should point to venv/bin/python
```

### Issue: Virtual environment not activating on Windows WSL

**Problem:** WSL-specific path issues

**Solution:**
```bash
# Recreate environment
rm -rf venv
python3 -m venv venv

# Activate with explicit bash
bash -c "source venv/bin/activate && python --version"

# Or use dot notation
. venv/bin/activate
```

### Issue: `cannot find python3.x` when creating venv

**Problem:** Python version not installed

**Solution:**
```bash
# List available Python versions
ls /usr/bin/python*

# Use available version
python3.11 -m venv venv

# Or install desired version
sudo apt install python3.11-venv  # Ubuntu
brew install python@3.11           # macOS
```

### Issue: Packages installed but not found in venv

**Problem:** Installing packages outside venv

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate
echo $VIRTUAL_ENV  # Should show venv path

# Check which pip you're using
which pip  # Should be venv/bin/pip

# Reinstall in venv
pip install package_name

# Verify
pip list
```

---

## Package Installation Issues

### Issue: `ERROR: Could not find a version that satisfies the requirement`

**Problem:** Package name misspelled or doesn't exist

**Solution:**
```bash
# Check package name on PyPI.org
# Common mistakes:
pip install pyyaml    # ✓ Correct
pip install yaml      # ✗ Wrong

pip install kubernetes  # ✓ Correct
pip install k8s         # ✗ Wrong

# Search for correct name
pip search package_name  # (deprecated)
# Use https://pypi.org instead
```

### Issue: SSL Certificate Verification Failed

**Problem:** Corporate proxy or outdated certificates

**Solution:**
```bash
# Option 1: Upgrade pip and certificates
pip install --upgrade pip certifi

# Option 2: Use trusted host (temporary)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org package_name

# Option 3: Update certificates (macOS)
/Applications/Python\ 3.x/Install\ Certificates.command

# Option 4: Configure proxy
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
pip install package_name
```

### Issue: Building wheel failed

**Problem:** Missing system dependencies for compiled packages

**Solution:**
```bash
# Ubuntu/Debian: Install build tools
sudo apt install build-essential python3-dev

# Specific packages
sudo apt install libssl-dev libffi-dev  # For cryptography
sudo apt install libxml2-dev libxmlsec1-dev  # For XML processing
sudo apt install libpq-dev  # For PostgreSQL

# macOS: Install Xcode command line tools
xcode-select --install

# Then retry
pip install package_name
```

### Issue: Package conflicts / dependency hell

**Problem:** Conflicting package versions

**Solution:**
```bash
# Option 1: Fresh virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 2: Use pip-tools
pip install pip-tools
pip-compile requirements.in
pip-sync

# Option 3: Use poetry (handles dependencies better)
poetry install
```

---

## Import Errors

### Issue: `ModuleNotFoundError: No module named 'xyz'`

**Problem:** Package not installed in active environment

**Solution:**
```bash
# Check if package is installed
pip list | grep package_name

# Install it
pip install package_name

# Verify Python is using correct environment
python -c "import sys; print(sys.executable)"
which python

# Common module vs package names:
import yaml          # pip install pyyaml
import cv2           # pip install opencv-python
import PIL           # pip install pillow
```

### Issue: `ImportError: cannot import name 'X' from 'Y'`

**Problem:** Wrong package version or circular import

**Solution:**
```bash
# Check package version
pip show package_name

# Upgrade to latest
pip install --upgrade package_name

# Or install specific version
pip install package_name==x.y.z

# For circular imports: restructure code
# Move import inside function instead of module level
```

### Issue: Package installs but import still fails

**Problem:** Multiple Python installations

**Solution:**
```bash
# Use python -m to ensure correct environment
python -m pip install package_name

# Verify installation
python -m pip show package_name
python -c "import package_name; print(package_name.__file__)"

# Check sys.path
python -c "import sys; print('\n'.join(sys.path))"
```

---

## Python Version Issues

### Issue: Script requires Python 3.x but system has 2.x

**Problem:** Old Python version

**Solution:**
```bash
# Use python3 explicitly
python3 script.py

# Add shebang to script
#!/usr/bin/env python3

# Make executable
chmod +x script.py
./script.py

# Install Python 3
sudo apt install python3  # Ubuntu
brew install python3       # macOS
```

### Issue: f-strings not working

**Problem:** Python version < 3.6

**Solution:**
```bash
# Check version
python --version

# Upgrade Python (see SETUP.md)
# Or use older string formatting
# Instead of: f"Hello {name}"
# Use: "Hello {}".format(name)
# Or: "Hello %s" % name
```

### Issue: Type hints causing syntax errors

**Problem:** Python < 3.5

**Solution:**
```python
# For Python 3.5+
def function(name: str) -> str:
    return name

# For older Python, remove type hints
def function(name):
    return name

# Or use comments
def function(name):  # type: (str) -> str
    return name
```

---

## IDE/Editor Issues

### Issue: VS Code not detecting virtual environment

**Problem:** VS Code using wrong Python interpreter

**Solution:**
1. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Python: Select Interpreter"
3. Choose the one in your `venv` folder
4. Or manually in `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python"
}
```

### Issue: Import errors in VS Code but script runs fine

**Problem:** VS Code using different Python than terminal

**Solution:**
```bash
# In VS Code terminal, verify Python
which python
python --version

# Reload VS Code window
# Cmd+Shift+P (macOS) or Ctrl+Shift+P (Windows/Linux)
# Type: "Developer: Reload Window"

# Restart Python language server
# Cmd+Shift+P → "Python: Restart Language Server"
```

### Issue: Pylint false positives

**Problem:** Linter not configured for project

**Solution:**
```python
# Disable specific warnings
# pylint: disable=line-too-long
# pylint: disable=invalid-name

# Create .pylintrc
pylint --generate-rcfile > .pylintrc

# Or use inline comments
import something  # pylint: disable=import-error
```

---

## Script Execution Issues

### Issue: `^M: bad interpreter` or `\r: command not found`

**Problem:** Windows line endings (CRLF) on Unix system

**Solution:**
```bash
# Convert line endings
dos2unix script.py

# Or with sed
sed -i 's/\r$//' script.py

# Or in Python
python -c "import sys; data = open(sys.argv[1], 'rb').read().replace(b'\r\n', b'\n'); open(sys.argv[1], 'wb').write(data)" script.py
```

### Issue: Script works in IDE but not from command line

**Problem:** Working directory or environment differences

**Solution:**
```bash
# Print debugging info
python -c "import sys, os; print('Python:', sys.executable); print('CWD:', os.getcwd()); print('PATH:', sys.path)"

# Use absolute paths in script
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

# Or add to path
import sys
sys.path.insert(0, '/path/to/modules')
```

### Issue: `SyntaxError: invalid syntax`

**Problem:** Code has syntax error

**Common mistakes:**
```python
# Missing colon
if condition  # ✗ Wrong
if condition:  # ✓ Correct

# Wrong indentation
def func():
print("hello")  # ✗ Wrong (no indent)

def func():
    print("hello")  # ✓ Correct

# Mixing tabs and spaces (use spaces only!)
# Use editor to show whitespace characters

# Unclosed brackets
my_list = [1, 2, 3  # ✗ Missing ]
my_list = [1, 2, 3]  # ✓ Correct
```

---

## Common DevOps-Specific Issues

### Issue: Subprocess command fails silently

**Problem:** Not checking return codes

**Solution:**
```python
import subprocess

# Bad: Doesn't check errors
subprocess.run(['ls', '/nonexistent'])

# Good: Check return code
result = subprocess.run(['ls', '/nonexistent'], capture_output=True)
if result.returncode != 0:
    print(f"Command failed: {result.stderr.decode()}")

# Better: Raise exception on error
subprocess.run(['ls', '/nonexistent'], check=True, capture_output=True)
```

### Issue: File not found when reading config

**Problem:** Relative paths don't work in all contexts

**Solution:**
```python
import os
from pathlib import Path

# Bad: Relative path
with open('config.yml') as f:
    data = f.read()

# Good: Relative to script location
script_dir = Path(__file__).parent
config_path = script_dir / 'config.yml'
with open(config_path) as f:
    data = f.read()

# Or use absolute path
config_path = Path.home() / '.config' / 'myapp' / 'config.yml'
```

### Issue: Credentials in code

**Problem:** Hardcoded secrets (security risk!)

**Solution:**
```python
import os

# Bad: Hardcoded
API_KEY = "abc123"  # ✗ NEVER DO THIS

# Good: Environment variable
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable required")

# Better: Use python-dotenv
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
```

---

## Cloud SDK Issues

### Issue: Google Cloud SDK import fails

**Problem:** google-cloud packages not installed

**Solution:**
```bash
# Install specific GCP libraries
pip install google-cloud-storage
pip install google-cloud-compute
pip install google-cloud-bigquery

# Not this (it's the gcloud CLI tool)
# pip install google-cloud

# Verify
python -c "from google.cloud import storage; print('OK')"
```

### Issue: Authentication errors with GCP

**Problem:** No credentials configured

**Solution:**
```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud auth application-default login

# Or use service account
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

# In Python
from google.cloud import storage
client = storage.Client()  # Uses default credentials
```

---

## Docker/Kubernetes Client Issues

### Issue: Docker SDK connection errors

**Problem:** Docker daemon not accessible

**Solution:**
```bash
# Check Docker is running
docker ps

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
# Log out and back in

# In Python
import docker

# Try explicit connection
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# Check permissions
ls -l /var/run/docker.sock
```

### Issue: Kubernetes client config not found

**Problem:** kubeconfig not at default location

**Solution:**
```python
from kubernetes import client, config

# Load from default location
config.load_kube_config()

# Or specify config file
config.load_kube_config(config_file='/path/to/kubeconfig')

# For in-cluster
config.load_incluster_config()
```

---

## Getting Help

If you're still stuck:

1. **Check the error message carefully** - It usually tells you what's wrong
2. **Search for the exact error** - Someone has likely encountered it before
3. **Use debugging tools**:
   ```python
   import pdb; pdb.set_trace()  # Debugger
   print(f"Debug: {variable}")   # Print debugging
   ```
4. **Simplify the problem** - Create a minimal reproducible example
5. **Check official documentation**:
   - [Python docs](https://docs.python.org/3/)
   - [PyPI packages](https://pypi.org/)
   - Library-specific docs

---

## Quick Debug Commands

```bash
# Python environment info
python --version
pip --version
which python
python -c "import sys; print(sys.executable)"
python -c "import sys; print('\n'.join(sys.path))"

# Package info
pip list
pip show package_name
python -c "import package; print(package.__version__)"
python -c "import package; print(package.__file__)"

# Virtual environment check
echo $VIRTUAL_ENV
which python
pip list

# Clean Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Test imports
python -c "import sys; import os; import json; print('OK')"
```

---

## Prevention Tips

1. **Always use virtual environments** - Avoid system-wide package conflicts
2. **Use requirements.txt** - Document dependencies
3. **Version control** - Git track your code
4. **Test in clean environment** - Catch missing dependencies
5. **Use linters** - Catch errors before running (pylint, flake8)
6. **Read error messages** - They're usually accurate
7. **Keep Python updated** - Latest stable version recommended

---

**Still having issues?** Review [SETUP.md](SETUP.md) or check [RESOURCES.md](RESOURCES.md) for more help.
