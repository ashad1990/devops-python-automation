# Python for DevOps Concepts

Understanding how Python fits into the DevOps ecosystem and when to use it.

## Table of Contents

- [Python for DevOps vs General Python](#python-for-devops-vs-general-python)
- [When to Use Python vs Bash](#when-to-use-python-vs-bash)
- [Python Ecosystem for DevOps](#python-ecosystem-for-devops)
- [Core DevOps Python Patterns](#core-devops-python-patterns)
- [Best Practices](#best-practices)

---

## Python for DevOps vs General Python

### DevOps Focus

**DevOps Python prioritizes:**
- **Automation**: Scripting repetitive operational tasks
- **Integration**: Connecting different tools and APIs
- **Infrastructure**: Managing cloud resources, containers, VMs
- **Monitoring**: Health checks, metrics collection, alerting
- **Reliability**: Error handling, retries, logging
- **Portability**: Cross-platform compatibility

**Not focused on:**
- Web application development (Django, Flask)
- Data science/machine learning (pandas, scikit-learn)
- Game development
- Desktop GUI applications

### Key Differences

| Aspect | General Python | DevOps Python |
|--------|---------------|---------------|
| **Goal** | Build applications | Automate operations |
| **Users** | End users | Engineers, systems |
| **Runtime** | Long-running servers | Short scripts, CLI tools |
| **Dependencies** | Heavy frameworks OK | Lightweight preferred |
| **Error Handling** | User-friendly messages | Detailed logs, retries |
| **Output** | UI/Web pages | CLI output, logs, reports |
| **Testing** | Unit + Integration | Unit + Integration + Smoke |

### DevOps Python Example

```python
#!/usr/bin/env python3
"""
DevOps script: Check health of multiple API endpoints
Typical DevOps characteristics:
- CLI tool with arguments
- External integrations (APIs)
- Error handling and retries
- Logging
- Exit codes
- Configuration from files
"""

import sys
import logging
import argparse
import requests
from typing import List, Dict
import yaml

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_endpoint(url: str, timeout: int = 5) -> Dict[str, any]:
    """Check health of a single endpoint."""
    try:
        response = requests.get(url, timeout=timeout)
        return {
            'url': url,
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds()
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to check {url}: {e}")
        return {
            'url': url,
            'status': 'failed',
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Health check for API endpoints')
    parser.add_argument('--config', required=True, help='YAML config file with endpoints')
    args = parser.parse_args()
    
    # Load configuration
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    endpoints = config.get('endpoints', [])
    results = [check_endpoint(url) for url in endpoints]
    
    # Report results
    healthy = sum(1 for r in results if r['status'] == 'healthy')
    logger.info(f"Health check complete: {healthy}/{len(results)} healthy")
    
    # Exit with appropriate code
    sys.exit(0 if healthy == len(results) else 1)


if __name__ == "__main__":
    main()
```

---

## When to Use Python vs Bash

### Use Python When:

✅ **Complex Logic**
```python
# Python: Easy to read and maintain
def calculate_instance_cost(hours, instance_type, region):
    pricing = get_pricing(instance_type, region)
    discount = calculate_discount(hours)
    return hours * pricing * (1 - discount)
```

✅ **API Integration**
```python
# Python: Built-in JSON, requests library
import requests
response = requests.get('https://api.github.com/repos/owner/repo')
data = response.json()
```

✅ **Cross-Platform**
```python
# Python: Works on Windows, Linux, macOS
import os
import pathlib
config_path = pathlib.Path.home() / '.config' / 'app.yml'
```

✅ **Data Processing**
```python
# Python: Rich data structures
servers = [s for s in all_servers if s['status'] == 'running' and s['cpu'] > 80]
```

✅ **Error Handling**
```python
# Python: Structured exception handling
try:
    result = deploy_application()
except DeploymentError as e:
    rollback()
    notify_team(e)
finally:
    cleanup()
```

✅ **Testing**
```python
# Python: pytest, mocking, fixtures
def test_health_check():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        assert check_health('http://api') == 'healthy'
```

### Use Bash When:

✅ **Simple File Operations**
```bash
# Bash: Concise for basic file tasks
find /var/log -name "*.log" -mtime +30 -delete
```

✅ **Pipelines**
```bash
# Bash: Native command chaining
cat access.log | grep "ERROR" | awk '{print $1}' | sort | uniq -c
```

✅ **System Administration**
```bash
# Bash: Direct system commands
systemctl restart nginx
journalctl -u myapp -f
```

✅ **Quick One-Liners**
```bash
# Bash: Fast for ad-hoc tasks
for i in {1..10}; do curl -s http://api/health; done
```

### Hybrid Approach

Often the best solution combines both:

```bash
#!/bin/bash
# Bash script that calls Python for complex logic

# Bash: System setup
export AWS_REGION=us-west-2
source /etc/profile.d/app.sh

# Python: Complex processing
python3 << 'PYTHON'
import boto3
import json

ec2 = boto3.client('ec2')
instances = ec2.describe_instances()
# ... complex filtering and analysis ...
PYTHON

# Bash: Final system commands
sudo systemctl restart myapp
```

---

## Python Ecosystem for DevOps

### Core Libraries

#### 1. **Standard Library** (No installation needed)
```python
import os          # OS operations, environment variables
import sys         # System-specific parameters
import subprocess  # Run shell commands
import pathlib     # Modern path handling
import json        # JSON parsing
import logging     # Logging framework
import argparse    # CLI argument parsing
import datetime    # Date and time handling
import re          # Regular expressions
import shutil      # High-level file operations
```

#### 2. **HTTP & APIs**
```python
import requests    # HTTP library (pip install requests)
# Making API calls, REST integration
response = requests.post(
    'https://api.service.com/v1/resource',
    json={'key': 'value'},
    headers={'Authorization': 'Bearer token'}
)
```

#### 3. **Configuration & Data Formats**
```python
import yaml        # YAML files (pip install pyyaml)
import toml        # TOML files (pip install toml)
import csv         # CSV files (standard library)

# Parse YAML config
with open('config.yml') as f:
    config = yaml.safe_load(f)
```

#### 4. **Cloud SDKs**

**Google Cloud:**
```python
from google.cloud import storage, compute_v1
from google.cloud import bigquery

# Storage operations
client = storage.Client()
bucket = client.bucket('my-bucket')
blob = bucket.blob('file.txt')
blob.upload_from_filename('local.txt')
```

**AWS (if needed):**
```python
import boto3  # AWS SDK (pip install boto3)
s3 = boto3.client('s3')
ec2 = boto3.resource('ec2')
```

#### 5. **Container & Orchestration**
```python
import docker           # Docker SDK (pip install docker)
import kubernetes       # K8s client (pip install kubernetes)

# Docker example
client = docker.from_env()
container = client.containers.run('nginx', detach=True)

# Kubernetes example
from kubernetes import client, config
config.load_kube_config()
v1 = client.CoreV1Api()
pods = v1.list_namespaced_pod(namespace='default')
```

#### 6. **Testing**
```python
import pytest          # Testing framework (pip install pytest)
import unittest        # Built-in testing
from unittest import mock  # Mocking

@pytest.fixture
def sample_config():
    return {'env': 'test', 'timeout': 30}

def test_deploy(sample_config):
    assert deploy(sample_config) == 'success'
```

#### 7. **CLI Tools**
```python
import click          # CLI framework (pip install click)
import argparse       # Built-in argument parsing

@click.command()
@click.option('--env', required=True, help='Environment')
@click.option('--dry-run', is_flag=True)
def deploy(env, dry_run):
    click.echo(f'Deploying to {env}')
```

### DevOps-Specific Libraries

```python
# Configuration management
import ansible_runner  # Ansible integration

# Monitoring & Metrics
import prometheus_client  # Prometheus metrics

# Infrastructure
import terraform  # Terraform wrapper

# CI/CD
import jenkins  # Jenkins API client
import gitlab   # GitLab API client

# Database
import psycopg2  # PostgreSQL
import pymongo   # MongoDB
import redis     # Redis
```

---

## Core DevOps Python Patterns

### 1. **Configuration Management Pattern**

```python
"""Load configuration from multiple sources with precedence."""
import os
import yaml
from typing import Dict, Any

class Config:
    """Configuration with environment override capability."""
    
    def __init__(self, config_file: str):
        # Load from file
        with open(config_file) as f:
            self.config = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value, checking environment first."""
        # Environment variable takes precedence
        env_key = key.upper().replace('.', '_')
        env_value = os.getenv(env_key)
        
        if env_value is not None:
            return env_value
        
        # Fall back to config file
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        
        return value if value != {} else default

# Usage
config = Config('config.yml')
timeout = config.get('api.timeout', default=30)  # Check env var first
```

### 2. **Retry Pattern**

```python
"""Retry failed operations with exponential backoff."""
import time
import logging
from functools import wraps

def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """Decorator for retrying functions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        logging.error(f"Max retries reached: {e}")
                        raise
                    
                    logging.warning(f"Attempt {attempt} failed, retrying in {current_delay}s")
                    time.sleep(current_delay)
                    current_delay *= backoff
        
        return wrapper
    return decorator

# Usage
@retry(max_attempts=5, delay=2, backoff=2, exceptions=(requests.exceptions.RequestException,))
def call_api(url):
    return requests.get(url, timeout=10)
```

### 3. **Resource Context Manager Pattern**

```python
"""Ensure proper cleanup of resources."""
from contextlib import contextmanager

@contextmanager
def temporary_environment(env_vars):
    """Temporarily set environment variables."""
    import os
    old_environ = os.environ.copy()
    
    try:
        os.environ.update(env_vars)
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)

# Usage
with temporary_environment({'ENV': 'staging', 'DEBUG': 'true'}):
    deploy_application()
# Environment restored after block
```

### 4. **Parallel Execution Pattern**

```python
"""Execute tasks in parallel for efficiency."""
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_server_health(server):
    """Check health of a single server."""
    import requests
    try:
        response = requests.get(f"http://{server}/health", timeout=5)
        return server, response.status_code == 200
    except Exception as e:
        return server, False

def check_all_servers(servers, max_workers=10):
    """Check health of all servers in parallel."""
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_server_health, srv): srv for srv in servers}
        
        for future in as_completed(futures):
            server, is_healthy = future.result()
            results[server] = is_healthy
    
    return results

# Usage
servers = ['server1.com', 'server2.com', 'server3.com']
health_status = check_all_servers(servers)
```

---

## Best Practices

### 1. **Always Use Virtual Environments**
```bash
# Isolate project dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. **Type Hints for Clarity**
```python
from typing import List, Dict, Optional

def get_running_instances(region: str) -> List[Dict[str, str]]:
    """Get all running EC2 instances in region."""
    pass
```

### 3. **Proper Logging**
```python
import logging

# Configure once at module level
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use throughout code
logger.info("Starting deployment")
logger.error(f"Deployment failed: {error}")
```

### 4. **Environment Variables for Secrets**
```python
import os

# NEVER hardcode secrets
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

### 5. **Graceful Error Handling**
```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    # Attempt recovery
    rollback()
finally:
    # Always cleanup
    cleanup_resources()
```

### 6. **Use `if __name__ == "__main__":`**
```python
def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    # ... setup ...
    args = parser.parse_args()
    # ... logic ...

if __name__ == "__main__":
    main()
```

### 7. **Docstrings and Comments**
```python
def deploy_service(service: str, version: str, replicas: int = 3) -> bool:
    """
    Deploy a service to Kubernetes.
    
    Args:
        service: Service name to deploy
        version: Container image version tag
        replicas: Number of replicas (default: 3)
    
    Returns:
        bool: True if deployment succeeded, False otherwise
    
    Raises:
        KubernetesException: If deployment fails
    """
    pass
```

### 8. **Exit Codes**
```python
import sys

def main():
    try:
        result = run_automation()
        if result.success:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(2)  # Error
```

---

## Summary

Python for DevOps is about:
- ✅ **Automation** over application development
- ✅ **Reliability** with proper error handling
- ✅ **Simplicity** over complexity
- ✅ **Integration** with existing tools
- ✅ **Portability** across environments
- ✅ **Maintainability** with clean code

**Next Steps:**
- Review [COMMANDS.md](COMMANDS.md) for quick reference
- Try [QUICK-START.md](QUICK-START.md) to write your first script
- Begin [LAB-01](LABS/LAB-01-python-basics.md)
