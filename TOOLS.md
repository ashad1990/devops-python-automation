# Required Tools and Libraries

Complete reference of tools, libraries, and packages used in this DevOps Python automation course.

## Table of Contents

- [Core Python Tools](#core-python-tools)
- [Development Tools](#development-tools)
- [Python Libraries](#python-libraries)
- [Cloud Platform SDKs](#cloud-platform-sdks)
- [Container & Orchestration](#container--orchestration)
- [Testing & Quality](#testing--quality)
- [CLI & Utilities](#cli--utilities)
- [Installation Guide](#installation-guide)

---

## Core Python Tools

### Python 3.9+
**Required:** Yes  
**Purpose:** Core programming language  
**Installation:** See [SETUP.md](SETUP.md)

```bash
python3 --version  # Should be 3.9 or higher
```

### pip
**Required:** Yes  
**Purpose:** Package installer for Python  
**Comes with:** Python 3.4+

```bash
pip install --upgrade pip
pip --version
```

### venv
**Required:** Yes  
**Purpose:** Virtual environment management  
**Comes with:** Python 3.3+

```bash
python3 -m venv myenv
source myenv/bin/activate
```

---

## Development Tools

### Git
**Required:** Yes  
**Purpose:** Version control

```bash
# Install
sudo apt install git      # Ubuntu/Debian
brew install git          # macOS

# Verify
git --version
```

### Code Editor

**Option 1: Visual Studio Code (Recommended)**
- Download: https://code.visualstudio.com/
- Extensions:
  - Python (Microsoft)
  - Pylance
  - Python Indent
  - autoDocstring
  - YAML

**Option 2: PyCharm**
- Download: https://www.jetbrains.com/pycharm/
- Community Edition (free) is sufficient

**Option 3: Vim/Neovim**
```bash
# Install Python plugins
# vim-python/python-syntax
# davidhalter/jedi-vim
```

---

## Python Libraries

### Essential Libraries (Standard Library)

These come with Python, no installation needed:

```python
import os           # Operating system interface
import sys          # System-specific parameters
import json         # JSON encoding and decoding
import csv          # CSV file reading and writing
import logging      # Logging facility
import argparse     # Command-line argument parsing
import subprocess   # Subprocess management
import pathlib      # Object-oriented filesystem paths
import datetime     # Date and time handling
import re           # Regular expressions
import shutil       # High-level file operations
import tempfile     # Temporary files and directories
import configparser # Configuration file parser
import urllib       # URL handling
import http.server  # HTTP servers
import socket       # Low-level networking
import threading    # Thread-based parallelism
import asyncio      # Asynchronous I/O
```

### HTTP & API Libraries

#### requests
**Required:** Yes (Lab 07+)  
**Purpose:** HTTP library for API calls  
**PyPI:** https://pypi.org/project/requests/

```bash
pip install requests
```

```python
import requests

response = requests.get('https://api.github.com')
data = response.json()
```

---

### Configuration & Data Format Libraries

#### PyYAML
**Required:** Yes (Lab 05+)  
**Purpose:** YAML parser and emitter  
**PyPI:** https://pypi.org/project/PyYAML/

```bash
pip install pyyaml
```

```python
import yaml

with open('config.yml') as f:
    config = yaml.safe_load(f)
```

#### python-dotenv
**Required:** Optional  
**Purpose:** Read .env files  
**PyPI:** https://pypi.org/project/python-dotenv/

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.getenv('API_KEY')
```

#### toml
**Required:** Optional  
**Purpose:** TOML parser  
**PyPI:** https://pypi.org/project/toml/

```bash
pip install toml
```

---

## Cloud Platform SDKs

### Google Cloud Libraries

#### google-cloud-storage
**Required:** Yes (Lab 08, Projects)  
**Purpose:** Google Cloud Storage operations  
**PyPI:** https://pypi.org/project/google-cloud-storage/

```bash
pip install google-cloud-storage
```

```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('my-bucket')
```

#### google-cloud-compute
**Required:** Yes (Lab 08, Projects)  
**Purpose:** Compute Engine management  
**PyPI:** https://pypi.org/project/google-cloud-compute/

```bash
pip install google-cloud-compute
```

```python
from google.cloud import compute_v1

instances_client = compute_v1.InstancesClient()
```

#### google-cloud-bigquery
**Required:** Optional (Project 05)  
**Purpose:** BigQuery operations for billing data  
**PyPI:** https://pypi.org/project/google-cloud-bigquery/

```bash
pip install google-cloud-bigquery
```

```python
from google.cloud import bigquery

client = bigquery.Client()
```

#### google-api-python-client
**Required:** Optional  
**Purpose:** Generic Google API access  
**PyPI:** https://pypi.org/project/google-api-python-client/

```bash
pip install google-api-python-client
```

### AWS SDK (Optional, for reference)

#### boto3
**Required:** No (course focuses on GCP)  
**Purpose:** AWS SDK for Python  
**PyPI:** https://pypi.org/project/boto3/

```bash
pip install boto3  # Only if working with AWS
```

---

## Container & Orchestration

### Docker SDK

#### docker
**Required:** Yes (Lab 09)  
**Purpose:** Docker API client  
**PyPI:** https://pypi.org/project/docker/

```bash
pip install docker
```

```python
import docker

client = docker.from_env()
containers = client.containers.list()
```

### Kubernetes Client

#### kubernetes
**Required:** Yes (Lab 10)  
**Purpose:** Kubernetes API client  
**PyPI:** https://pypi.org/project/kubernetes/

```bash
pip install kubernetes
```

```python
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
pods = v1.list_pod_for_all_namespaces()
```

---

## Testing & Quality

### Testing Frameworks

#### pytest
**Required:** Yes (Lab 11)  
**Purpose:** Testing framework  
**PyPI:** https://pypi.org/project/pytest/

```bash
pip install pytest
```

```bash
# Run tests
pytest
pytest test_module.py
pytest -v
```

#### pytest-cov
**Required:** Optional  
**Purpose:** Code coverage for pytest  
**PyPI:** https://pypi.org/project/pytest-cov/

```bash
pip install pytest-cov
pytest --cov=. --cov-report=html
```

#### pytest-mock
**Required:** Optional  
**Purpose:** Mocking plugin for pytest  
**PyPI:** https://pypi.org/project/pytest-mock/

```bash
pip install pytest-mock
```

### Code Quality Tools

#### pylint
**Required:** Optional but recommended  
**Purpose:** Code linter  
**PyPI:** https://pypi.org/project/pylint/

```bash
pip install pylint
pylint mymodule.py
```

#### flake8
**Required:** Optional  
**Purpose:** Style guide enforcement  
**PyPI:** https://pypi.org/project/flake8/

```bash
pip install flake8
flake8 mymodule.py
```

#### black
**Required:** Optional  
**Purpose:** Code formatter  
**PyPI:** https://pypi.org/project/black/

```bash
pip install black
black mymodule.py
```

#### mypy
**Required:** Optional  
**Purpose:** Static type checker  
**PyPI:** https://pypi.org/project/mypy/

```bash
pip install mypy
mypy mymodule.py
```

---

## CLI & Utilities

### Command-Line Interface

#### click
**Required:** Yes (Lab 12)  
**Purpose:** CLI framework  
**PyPI:** https://pypi.org/project/click/

```bash
pip install click
```

```python
import click

@click.command()
@click.option('--name', default='World')
def hello(name):
    click.echo(f'Hello {name}!')
```

#### argparse
**Required:** Built-in  
**Purpose:** Command-line argument parsing

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True)
```

### Terminal Enhancements

#### rich
**Required:** Optional  
**Purpose:** Beautiful terminal output  
**PyPI:** https://pypi.org/project/rich/

```bash
pip install rich
```

```python
from rich.console import Console
from rich.table import Table

console = Console()
console.print("[bold green]Success![/bold green]")
```

#### colorama
**Required:** Optional  
**Purpose:** Cross-platform colored terminal text  
**PyPI:** https://pypi.org/project/colorama/

```bash
pip install colorama
```

### Utilities

#### jinja2
**Required:** Optional  
**Purpose:** Template engine  
**PyPI:** https://pypi.org/project/Jinja2/

```bash
pip install jinja2
```

```python
from jinja2 import Template

template = Template("Hello {{ name }}!")
print(template.render(name="World"))
```

#### tabulate
**Required:** Optional  
**Purpose:** Pretty-print tabular data  
**PyPI:** https://pypi.org/project/tabulate/

```bash
pip install tabulate
```

```python
from tabulate import tabulate

data = [['Alice', 24], ['Bob', 19]]
print(tabulate(data, headers=['Name', 'Age']))
```

---

## Installation Guide

### Quick Install All Course Dependencies

```bash
# Create and activate virtual environment
python3 -m venv devops-env
source devops-env/bin/activate  # Linux/macOS
# devops-env\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip

# Install from requirements.txt
pip install -r requirements.txt

# Verify installation
pip list
```

### Install by Category

```bash
# Essential
pip install requests pyyaml

# Cloud (GCP)
pip install google-cloud-storage google-cloud-compute google-cloud-bigquery

# Containers
pip install docker kubernetes

# Testing
pip install pytest pytest-cov pytest-mock

# CLI Tools
pip install click rich

# Code Quality (optional)
pip install pylint flake8 black mypy

# Utilities (optional)
pip install python-dotenv jinja2 tabulate
```

### Verify Installation

```bash
# Run verification script
python3 << 'EOF'
import sys

modules = {
    'Core': ['json', 'yaml', 'logging', 'argparse'],
    'HTTP/API': ['requests'],
    'Cloud': ['google.cloud.storage', 'google.cloud.compute'],
    'Containers': ['docker', 'kubernetes'],
    'Testing': ['pytest'],
    'CLI': ['click']
}

print("=" * 60)
print("Dependency Verification")
print("=" * 60)

all_ok = True
for category, module_list in modules.items():
    print(f"\n{category}:")
    for module in module_list:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module} - NOT INSTALLED")
            all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("✓ All required modules are installed!")
else:
    print("✗ Some modules are missing. Run: pip install -r requirements.txt")
print("=" * 60)

sys.exit(0 if all_ok else 1)
EOF
```

---

## External Tools (Not Python Packages)

### gcloud CLI
**Required:** For GCP authentication and setup  
**Install:** https://cloud.google.com/sdk/docs/install

```bash
# Authenticate
gcloud auth login
gcloud auth application-default login

# Set project
gcloud config set project PROJECT_ID
```

### Docker
**Required:** For Lab 09  
**Install:** https://docs.docker.com/get-docker/

```bash
docker --version
docker ps
```

### kubectl
**Required:** For Lab 10  
**Install:** https://kubernetes.io/docs/tasks/tools/

```bash
kubectl version --client
kubectl cluster-info
```

---

## IDE Extensions

### VS Code Extensions

Install from VS Code marketplace:

1. **Python** (ms-python.python) - Essential
2. **Pylance** (ms-python.vscode-pylance) - Language server
3. **Python Indent** - Auto-indentation
4. **autoDocstring** - Generate docstrings
5. **GitLens** - Git integration
6. **YAML** - YAML support
7. **Docker** - Docker file support
8. **Kubernetes** - K8s support

```bash
# Install via command line
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension njpwerner.autodocstring
```

---

## Troubleshooting

If you encounter issues installing packages, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

Common issues:
- Permission errors → Use virtual environment
- SSL errors → Update pip and certificates
- Build errors → Install system dependencies (`build-essential`, `python3-dev`)

---

## Summary

**Minimum Required:**
```bash
pip install requests pyyaml google-cloud-storage \
    google-cloud-compute docker kubernetes pytest click
```

**Full Course Stack:**
```bash
pip install -r requirements.txt
```

**Next Steps:**
- Complete [SETUP.md](SETUP.md) for environment setup
- Review [requirements.txt](requirements.txt) for exact versions
- Start [LAB-01](LABS/LAB-01-python-basics.md)
