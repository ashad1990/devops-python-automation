# LAB 04: Functions and Modules for DevOps

## Learning Objectives
By the end of this lab, you will be able to:
- Define and call functions with parameters
- Use return values effectively
- Work with *args and **kwargs for flexible functions
- Create and import custom modules
- Organize code into reusable packages
- Apply function best practices for DevOps automation

## Prerequisites
- Completed LAB-01, LAB-02, and LAB-03
- Understanding of control flow and data structures

---

## Part 1: Basic Functions

### Exercise 1.1: Defining and Calling Functions

Create `basic_functions.py`:

```python
# Simple function with no parameters
def print_banner():
    print("=" * 50)
    print("  SERVER MONITORING SYSTEM")
    print("=" * 50)

print_banner()

# Function with parameters
def check_disk_usage(used_gb, total_gb):
    usage_percent = (used_gb / total_gb) * 100
    print(f"Disk Usage: {used_gb}GB / {total_gb}GB ({usage_percent:.1f}%)")

check_disk_usage(450, 500)
check_disk_usage(120, 250)

# Function with return value
def calculate_uptime_days(uptime_seconds):
    days = uptime_seconds / (24 * 60 * 60)
    return days

uptime = calculate_uptime_days(2592000)
print(f"Uptime: {uptime:.1f} days")

# Function with multiple return values
def get_server_stats():
    cpu = 67.5
    memory = 82.3
    disk = 45.8
    return cpu, memory, disk

cpu, memory, disk = get_server_stats()
print(f"CPU: {cpu}%, Memory: {memory}%, Disk: {disk}%")

# Function with default parameters
def create_backup(filename, compression=True, encrypt=False):
    print(f"Creating backup of {filename}")
    print(f"  Compression: {compression}")
    print(f"  Encryption: {encrypt}")

create_backup("database.sql")
create_backup("database.sql", compression=False)
create_backup("database.sql", encrypt=True)
create_backup("database.sql", compression=False, encrypt=True)
```

**Expected Output:**
```
==================================================
  SERVER MONITORING SYSTEM
==================================================
Disk Usage: 450GB / 500GB (90.0%)
Disk Usage: 120GB / 250GB (48.0%)
Uptime: 30.0 days
CPU: 67.5%, Memory: 82.3%, Disk: 45.8%
Creating backup of database.sql
  Compression: True
  Encryption: False
Creating backup of database.sql
  Compression: False
  Encryption: False
Creating backup of database.sql
  Compression: True
  Encryption: True
Creating backup of database.sql
  Compression: False
  Encryption: True
```

### Exercise 1.2: Docstrings and Type Hints

```python
def validate_port(port: int) -> bool:
    """
    Validate if a port number is in the valid range.
    
    Args:
        port: Integer port number to validate
        
    Returns:
        True if port is valid (1-65535), False otherwise
        
    Examples:
        >>> validate_port(8080)
        True
        >>> validate_port(70000)
        False
    """
    return 1 <= port <= 65535

def format_server_info(name: str, ip: str, port: int) -> dict:
    """
    Format server information into a structured dictionary.
    
    Args:
        name: Server hostname
        ip: IP address
        port: Port number
        
    Returns:
        Dictionary containing formatted server information
    """
    return {
        "hostname": name,
        "ip_address": ip,
        "port": port,
        "valid_port": validate_port(port)
    }

# Test functions
print(f"Port 8080 valid: {validate_port(8080)}")
print(f"Port 70000 valid: {validate_port(70000)}")

server = format_server_info("web-01", "10.0.1.10", 8080)
print(f"\nServer info: {server}")

# Access docstring
print(f"\nDocstring:\n{validate_port.__doc__}")
```

**Expected Output:**
```
Port 8080 valid: True
Port 70000 valid: False

Server info: {'hostname': 'web-01', 'ip_address': '10.0.1.10', 'port': 8080, 'valid_port': True}

Docstring:
    Validate if a port number is in the valid range.
    
    Args:
        port: Integer port number to validate
        
    Returns:
        True if port is valid (1-65535), False otherwise
        
    Examples:
        >>> validate_port(8080)
        True
        >>> validate_port(70000)
        False
```

---

## Part 2: Advanced Function Parameters

### Exercise 2.1: *args - Variable Positional Arguments

Create `advanced_params.py`:

```python
def restart_servers(*server_names):
    """Restart multiple servers"""
    print(f"Restarting {len(server_names)} servers...")
    for server in server_names:
        print(f"  - Restarting {server}")

# Can pass any number of arguments
restart_servers("web-01")
restart_servers("web-01", "web-02", "web-03")
restart_servers("db-01", "cache-01", "api-01", "worker-01")

# Calculate average of any number of metrics
def calculate_average(*values):
    """Calculate average of multiple values"""
    if not values:
        return 0
    total = sum(values)
    return total / len(values)

avg_cpu = calculate_average(45.2, 67.8, 82.3, 34.1)
print(f"\nAverage CPU: {avg_cpu:.1f}%")

avg_memory = calculate_average(67.8, 82.1, 88.5)
print(f"Average Memory: {avg_memory:.1f}%")

# Combine required params with *args
def deploy_application(environment, *services):
    """Deploy multiple services to an environment"""
    print(f"Deploying to {environment}:")
    for service in services:
        print(f"  - Deploying {service}")

deploy_application("production", "web-app", "api", "worker")
```

**Expected Output:**
```
Restarting 1 servers...
  - Restarting web-01
Restarting 3 servers...
  - Restarting web-01
  - Restarting web-02
  - Restarting web-03
Restarting 4 servers...
  - Restarting db-01
  - Restarting cache-01
  - Restarting api-01
  - Restarting worker-01

Average CPU: 57.4%
Average Memory: 79.5%
Deploying to production:
  - Deploying web-app
  - Deploying api
  - Deploying worker
```

### Exercise 2.2: **kwargs - Variable Keyword Arguments

```python
def create_server_config(**options):
    """Create server configuration from keyword arguments"""
    print("Server Configuration:")
    for key, value in options.items():
        print(f"  {key}: {value}")

create_server_config(
    name="web-01",
    port=8080,
    workers=4,
    timeout=30
)

print()

create_server_config(
    name="db-01",
    port=5432,
    max_connections=100,
    ssl=True
)

# Combine *args and **kwargs
def deploy_with_options(environment, *services, **config):
    """Deploy services with configuration options"""
    print(f"Deploying to: {environment}")
    print(f"Services: {', '.join(services)}")
    print("Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")

print()
deploy_with_options(
    "production",
    "web-app", "api", "worker",
    replicas=3,
    auto_scale=True,
    max_memory="2GB"
)

# Unpacking dictionaries
def configure_database(host, port, database, user, password):
    """Configure database connection"""
    print(f"Connecting to {database} at {host}:{port}")
    print(f"User: {user}")

db_config = {
    "host": "localhost",
    "port": 5432,
    "database": "myapp",
    "user": "admin",
    "password": "secret"
}

print()
configure_database(**db_config)
```

**Expected Output:**
```
Server Configuration:
  name: web-01
  port: 8080
  workers: 4
  timeout: 30

Server Configuration:
  name: db-01
  port: 5432
  max_connections: 100
  ssl: True

Deploying to: production
Services: web-app, api, worker
Configuration:
  replicas: 3
  auto_scale: True
  max_memory: 2GB

Connecting to myapp at localhost:5432
User: admin
```

---

## Part 3: Function Scope and Lambda Functions

### Exercise 3.1: Variable Scope

Create `scope_demo.py`:

```python
# Global variable
server_count = 10

def add_server():
    """Demonstrates local scope"""
    # This creates a local variable
    server_count = 11
    print(f"Inside function: {server_count}")

print(f"Before function: {server_count}")
add_server()
print(f"After function: {server_count}")

# Modifying global variable
total_requests = 0

def increment_requests(count):
    """Modify global variable"""
    global total_requests
    total_requests += count
    print(f"Total requests: {total_requests}")

increment_requests(100)
increment_requests(50)
increment_requests(75)

# Nested functions and closures
def create_logger(prefix):
    """Create a logger function with specific prefix"""
    def log(message):
        print(f"[{prefix}] {message}")
    return log

app_logger = create_logger("APP")
db_logger = create_logger("DB")

print()
app_logger("Application started")
app_logger("Processing request")
db_logger("Connection established")
db_logger("Query executed")
```

**Expected Output:**
```
Before function: 10
Inside function: 11
After function: 10
Total requests: 100
Total requests: 150
Total requests: 225

[APP] Application started
[APP] Processing request
[DB] Connection established
[DB] Query executed
```

### Exercise 3.2: Lambda Functions

```python
# Simple lambda function
square = lambda x: x ** 2
print(f"Square of 5: {square(5)}")

# Lambda with multiple parameters
calculate_usage = lambda used, total: (used / total) * 100
usage = calculate_usage(450, 500)
print(f"Usage: {usage:.1f}%")

# Using lambda with built-in functions
servers = [
    {"name": "web-01", "cpu": 45.2},
    {"name": "web-02", "cpu": 78.9},
    {"name": "db-01", "cpu": 62.3},
]

# Sort by CPU usage
sorted_servers = sorted(servers, key=lambda s: s["cpu"])
print("\nServers sorted by CPU:")
for server in sorted_servers:
    print(f"  {server['name']}: {server['cpu']}%")

# Filter with lambda
high_cpu = list(filter(lambda s: s["cpu"] > 60, servers))
print("\nHigh CPU servers:")
for server in high_cpu:
    print(f"  {server['name']}: {server['cpu']}%")

# Map with lambda
cpu_values = list(map(lambda s: s["cpu"], servers))
print(f"\nCPU values: {cpu_values}")

# Lambda in list comprehension alternative
# Using lambda
doubled = list(map(lambda x: x * 2, [1, 2, 3, 4]))
print(f"Doubled (lambda): {doubled}")

# Using comprehension (more Pythonic)
doubled = [x * 2 for x in [1, 2, 3, 4]]
print(f"Doubled (comprehension): {doubled}")
```

**Expected Output:**
```
Square of 5: 25
Usage: 90.0%

Servers sorted by CPU:
  web-01: 45.2%
  db-01: 62.3%
  web-02: 78.9%

High CPU servers:
  web-02: 78.9%
  db-01: 62.3%

CPU values: [45.2, 78.9, 62.3]
Doubled (lambda): [2, 4, 6, 8]
Doubled (comprehension): [2, 4, 6, 8]
```

---

## Part 4: Modules and Imports

### Exercise 4.1: Creating Custom Modules

Create a file named `server_utils.py`:

```python
"""
Server utility functions for DevOps automation.
"""

def validate_port(port):
    """Validate if port is in valid range"""
    return isinstance(port, int) and 1 <= port <= 65535

def calculate_uptime_days(seconds):
    """Convert uptime seconds to days"""
    return seconds / (24 * 60 * 60)

def format_bytes(bytes_value):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def get_status_color(value, warning_threshold, critical_threshold):
    """Get status based on thresholds"""
    if value >= critical_threshold:
        return "CRITICAL"
    elif value >= warning_threshold:
        return "WARNING"
    else:
        return "OK"

# Module-level constants
DEFAULT_PORT = 8080
DEFAULT_TIMEOUT = 30
VALID_ENVIRONMENTS = ["development", "staging", "production"]

if __name__ == "__main__":
    # Test functions when module is run directly
    print("Testing server_utils module:")
    print(f"Port 8080 valid: {validate_port(8080)}")
    print(f"Uptime: {calculate_uptime_days(2592000):.1f} days")
    print(f"Size: {format_bytes(1536000000)}")
    print(f"Status: {get_status_color(85, 70, 90)}")
```

Create a file named `use_module.py`:

```python
# Different ways to import modules

# Import entire module
import server_utils

port_valid = server_utils.validate_port(8080)
print(f"Port valid: {port_valid}")
print(f"Default port: {server_utils.DEFAULT_PORT}")

# Import specific functions
from server_utils import calculate_uptime_days, format_bytes

uptime = calculate_uptime_days(2592000)
print(f"Uptime: {uptime:.1f} days")

size = format_bytes(1536000000)
print(f"File size: {size}")

# Import with alias
from server_utils import get_status_color as get_status

status = get_status(85, 70, 90)
print(f"Status: {status}")

# Import all (not recommended, but shown for completeness)
# from server_utils import *

# Import module with alias
import server_utils as su

print(f"Environments: {su.VALID_ENVIRONMENTS}")
```

**Expected Output:**
```
Port valid: True
Default port: 8080
Uptime: 30.0 days
File size: 1.43 GB
Status: WARNING
Environments: ['development', 'staging', 'production']
```

### Exercise 4.2: Built-in Modules

Create `builtin_modules.py`:

```python
# os module for operating system operations
import os

print("OS Module:")
print(f"Current directory: {os.getcwd()}")
print(f"User: {os.getenv('USER', 'unknown')}")
print(f"Path separator: {os.sep}")

# sys module for system-specific parameters
import sys

print(f"\nPython version: {sys.version.split()[0]}")
print(f"Platform: {sys.platform}")

# datetime module for date/time operations
from datetime import datetime, timedelta

now = datetime.now()
print(f"\nCurrent time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# Calculate uptime end time
uptime_hours = 720
uptime_start = now - timedelta(hours=uptime_hours)
print(f"Server started: {uptime_start.strftime('%Y-%m-%d %H:%M:%S')}")

# json module for JSON operations
import json

server_data = {
    "name": "web-01",
    "ip": "10.0.1.10",
    "port": 8080,
    "active": True
}

json_string = json.dumps(server_data, indent=2)
print(f"\nJSON output:\n{json_string}")

# Parse JSON
parsed = json.loads(json_string)
print(f"Parsed name: {parsed['name']}")

# random module (useful for testing)
import random

print(f"\nRandom CPU value: {random.uniform(0, 100):.1f}%")
print(f"Random port: {random.randint(8000, 9000)}")

# collections module
from collections import Counter, defaultdict

# Count occurrences
log_levels = ["INFO", "ERROR", "INFO", "WARNING", "INFO", "ERROR"]
level_counts = Counter(log_levels)
print(f"\nLog level counts: {level_counts}")

# Default dictionary
server_metrics = defaultdict(list)
server_metrics["web-01"].append(45.2)
server_metrics["web-01"].append(48.3)
server_metrics["web-02"].append(67.8)
print(f"Server metrics: {dict(server_metrics)}")
```

---

## Part 5: Creating Packages

### Exercise 5.1: Package Structure

Create the following directory structure:

```
monitoring/
├── __init__.py
├── cpu.py
├── memory.py
└── disk.py
```

**monitoring/__init__.py:**
```python
"""
Server monitoring package
"""

from .cpu import get_cpu_usage, check_cpu_health
from .memory import get_memory_usage, check_memory_health
from .disk import get_disk_usage, check_disk_health

__version__ = "1.0.0"
__all__ = [
    "get_cpu_usage",
    "get_memory_usage", 
    "get_disk_usage",
    "check_cpu_health",
    "check_memory_health",
    "check_disk_health"
]
```

**monitoring/cpu.py:**
```python
"""CPU monitoring utilities"""

def get_cpu_usage():
    """Get current CPU usage (simulated)"""
    return 67.5

def check_cpu_health(threshold=80):
    """Check if CPU usage is healthy"""
    usage = get_cpu_usage()
    return usage < threshold, usage
```

**monitoring/memory.py:**
```python
"""Memory monitoring utilities"""

def get_memory_usage():
    """Get current memory usage (simulated)"""
    return 72.3

def check_memory_health(threshold=85):
    """Check if memory usage is healthy"""
    usage = get_memory_usage()
    return usage < threshold, usage
```

**monitoring/disk.py:**
```python
"""Disk monitoring utilities"""

def get_disk_usage():
    """Get current disk usage (simulated)"""
    return 45.8

def check_disk_health(threshold=90):
    """Check if disk usage is healthy"""
    usage = get_disk_usage()
    return usage < threshold, usage
```

**use_package.py:**
```python
# Import from package
from monitoring import get_cpu_usage, get_memory_usage, get_disk_usage
from monitoring import check_cpu_health, check_memory_health, check_disk_health
import monitoring

print(f"Monitoring package version: {monitoring.__version__}")

# Use imported functions
cpu = get_cpu_usage()
memory = get_memory_usage()
disk = get_disk_usage()

print(f"\nCurrent Metrics:")
print(f"CPU: {cpu}%")
print(f"Memory: {memory}%")
print(f"Disk: {disk}%")

# Check health
cpu_ok, cpu_val = check_cpu_health()
mem_ok, mem_val = check_memory_health()
disk_ok, disk_val = check_disk_health()

print(f"\nHealth Check:")
print(f"CPU: {'✓ OK' if cpu_ok else '✗ CRITICAL'} ({cpu_val}%)")
print(f"Memory: {'✓ OK' if mem_ok else '✗ CRITICAL'} ({mem_val}%)")
print(f"Disk: {'✓ OK' if disk_ok else '✗ CRITICAL'} ({disk_val}%)")

# Import submodule directly
from monitoring.cpu import get_cpu_usage as get_cpu

cpu_value = get_cpu()
print(f"\nDirect CPU check: {cpu_value}%")
```

---

## Part 6: Practice Challenges

### Challenge 1: Server Configuration Generator

Create a function that generates server configurations:

```python
# Your task: Create a function that generates server configs
# Requirements:
# 1. Function name: generate_server_config
# 2. Parameters: name (required), environment (default="production")
# 3. **kwargs for additional config options
# 4. Return dictionary with: name, environment, all kwargs
# 5. Add timestamp to config

# Test it with:
# generate_server_config("web-01")
# generate_server_config("db-01", "staging", port=5432, replicas=2)
```

<details>
<summary>Solution</summary>

```python
from datetime import datetime

def generate_server_config(name, environment="production", **options):
    """
    Generate server configuration dictionary.
    
    Args:
        name: Server name
        environment: Deployment environment (default: production)
        **options: Additional configuration options
        
    Returns:
        Dictionary with server configuration
    """
    config = {
        "name": name,
        "environment": environment,
        "created_at": datetime.now().isoformat(),
    }
    
    # Add all additional options
    config.update(options)
    
    return config

# Test
config1 = generate_server_config("web-01")
print(f"Config 1: {config1}")

config2 = generate_server_config("db-01", "staging", port=5432, replicas=2)
print(f"Config 2: {config2}")

config3 = generate_server_config(
    "api-01",
    environment="development",
    port=8080,
    workers=2,
    debug=True
)
print(f"Config 3: {config3}")
```
</details>

### Challenge 2: Metric Aggregator

Create functions to aggregate server metrics:

```python
# Your task: Create metric aggregation functions
# 1. Function: aggregate_metrics(*metric_values)
#    Returns: dict with min, max, avg, count
# 2. Function: aggregate_by_server(**server_metrics)
#    Takes server metrics as kwargs
#    Returns: dict with each server's average

# Test with:
# aggregate_metrics(45.2, 67.8, 82.3, 34.1, 91.2)
# aggregate_by_server(web01=[45, 50, 48], web02=[78, 82, 80])
```

<details>
<summary>Solution</summary>

```python
def aggregate_metrics(*metric_values):
    """
    Aggregate multiple metric values.
    
    Returns:
        Dictionary with min, max, avg, count
    """
    if not metric_values:
        return {"min": 0, "max": 0, "avg": 0, "count": 0}
    
    return {
        "min": min(metric_values),
        "max": max(metric_values),
        "avg": sum(metric_values) / len(metric_values),
        "count": len(metric_values)
    }

def aggregate_by_server(**server_metrics):
    """
    Aggregate metrics for each server.
    
    Args:
        **server_metrics: Server name as key, list of metrics as value
        
    Returns:
        Dictionary with each server's aggregated metrics
    """
    results = {}
    
    for server, metrics in server_metrics.items():
        results[server] = aggregate_metrics(*metrics)
    
    return results

# Test
print("Single aggregation:")
result = aggregate_metrics(45.2, 67.8, 82.3, 34.1, 91.2)
for key, value in result.items():
    print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")

print("\nServer aggregation:")
server_results = aggregate_by_server(
    web01=[45, 50, 48],
    web02=[78, 82, 80],
    db01=[88, 92, 90]
)

for server, metrics in server_results.items():
    print(f"{server}:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
```
</details>

### Challenge 3: Deployment Pipeline Functions

Create a deployment pipeline with multiple functions:

```python
# Your task: Create deployment pipeline functions
# 1. validate_config(config): Check required fields
# 2. build_application(app_name): Simulate build
# 3. run_tests(): Simulate tests
# 4. deploy(environment, app_name): Deploy if all checks pass
# 5. deploy_pipeline(config): Run complete pipeline

# Pipeline should:
# - Validate config has: app_name, environment
# - Build application
# - Run tests
# - Deploy if all successful
# - Return success/failure status
```

<details>
<summary>Solution</summary>

```python
def validate_config(config):
    """Validate deployment configuration"""
    required = ["app_name", "environment"]
    
    for field in required:
        if field not in config:
            return False, f"Missing required field: {field}"
    
    if config["environment"] not in ["staging", "production"]:
        return False, f"Invalid environment: {config['environment']}"
    
    return True, "Configuration valid"

def build_application(app_name):
    """Build the application"""
    print(f"Building {app_name}...")
    # Simulate build
    print(f"✓ Build successful")
    return True

def run_tests():
    """Run application tests"""
    print("Running tests...")
    # Simulate tests
    print("✓ All tests passed")
    return True

def deploy(environment, app_name):
    """Deploy application to environment"""
    print(f"Deploying {app_name} to {environment}...")
    print(f"✓ Deployment successful")
    return True

def deploy_pipeline(config):
    """
    Run complete deployment pipeline.
    
    Args:
        config: Deployment configuration dictionary
        
    Returns:
        Tuple of (success, message)
    """
    print("=" * 50)
    print("STARTING DEPLOYMENT PIPELINE")
    print("=" * 50)
    
    # Step 1: Validate
    print("\n1. Validating configuration...")
    valid, message = validate_config(config)
    if not valid:
        return False, f"Validation failed: {message}"
    print(f"✓ {message}")
    
    # Step 2: Build
    print("\n2. Building application...")
    if not build_application(config["app_name"]):
        return False, "Build failed"
    
    # Step 3: Test
    print("\n3. Running tests...")
    if not run_tests():
        return False, "Tests failed"
    
    # Step 4: Deploy
    print("\n4. Deploying...")
    if not deploy(config["environment"], config["app_name"]):
        return False, "Deployment failed"
    
    print("\n" + "=" * 50)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 50)
    
    return True, "Pipeline completed successfully"

# Test
config = {
    "app_name": "payment-api",
    "environment": "production",
    "version": "1.2.3"
}

success, message = deploy_pipeline(config)
print(f"\nResult: {message}")
```
</details>

---

## Part 7: Real-World Scenario

### Scenario: Server Management Library

Create a complete server management module:

**server_manager.py:**
```python
"""
Complete server management library for DevOps automation.
"""

from datetime import datetime
from typing import Dict, List, Tuple, Optional

class ServerManager:
    """Manage server inventory and operations"""
    
    def __init__(self):
        self.servers: Dict[str, dict] = {}
    
    def add_server(self, name: str, ip: str, **attributes) -> bool:
        """Add a server to inventory"""
        if name in self.servers:
            return False
        
        self.servers[name] = {
            "ip": ip,
            "added_at": datetime.now().isoformat(),
            **attributes
        }
        return True
    
    def remove_server(self, name: str) -> bool:
        """Remove a server from inventory"""
        if name in self.servers:
            del self.servers[name]
            return True
        return False
    
    def get_server(self, name: str) -> Optional[dict]:
        """Get server information"""
        return self.servers.get(name)
    
    def list_servers(self) -> List[str]:
        """List all server names"""
        return list(self.servers.keys())
    
    def update_metrics(self, name: str, **metrics) -> bool:
        """Update server metrics"""
        if name not in self.servers:
            return False
        
        if "metrics" not in self.servers[name]:
            self.servers[name]["metrics"] = {}
        
        self.servers[name]["metrics"].update(metrics)
        self.servers[name]["metrics"]["updated_at"] = datetime.now().isoformat()
        return True
    
    def get_servers_by_tag(self, tag: str) -> List[str]:
        """Get servers with specific tag"""
        result = []
        for name, info in self.servers.items():
            tags = info.get("tags", [])
            if tag in tags:
                result.append(name)
        return result
    
    def get_health_summary(self) -> Dict[str, int]:
        """Get overall health summary"""
        summary = {"healthy": 0, "warning": 0, "critical": 0, "unknown": 0}
        
        for name, info in self.servers.items():
            metrics = info.get("metrics", {})
            cpu = metrics.get("cpu", 0)
            memory = metrics.get("memory", 0)
            
            if cpu > 90 or memory > 90:
                summary["critical"] += 1
            elif cpu > 70 or memory > 80:
                summary["warning"] += 1
            elif cpu > 0 and memory > 0:
                summary["healthy"] += 1
            else:
                summary["unknown"] += 1
        
        return summary

# Usage example
if __name__ == "__main__":
    manager = ServerManager()
    
    # Add servers
    manager.add_server("web-01", "10.0.1.10", tags=["web", "production"])
    manager.add_server("web-02", "10.0.1.11", tags=["web", "production"])
    manager.add_server("db-01", "10.0.2.10", tags=["database", "production"])
    
    # Update metrics
    manager.update_metrics("web-01", cpu=45.2, memory=67.8)
    manager.update_metrics("web-02", cpu=92.3, memory=88.5)
    manager.update_metrics("db-01", cpu=62.1, memory=78.4)
    
    # Query servers
    print("All servers:", manager.list_servers())
    print("Web servers:", manager.get_servers_by_tag("web"))
    print("\nHealth summary:", manager.get_health_summary())
    
    # Get specific server
    server = manager.get_server("web-01")
    print(f"\nweb-01 details:")
    for key, value in server.items():
        print(f"  {key}: {value}")
```

---

## What You Learned

In this lab, you learned:

✅ **Function Basics**
- Defining functions with parameters
- Return values and multiple returns
- Default parameters
- Docstrings and type hints

✅ **Advanced Parameters**
- *args for variable positional arguments
- **kwargs for variable keyword arguments
- Combining different parameter types
- Unpacking arguments

✅ **Scope and Lambda**
- Local and global scope
- Nested functions and closures
- Lambda functions for simple operations
- When to use lambda vs regular functions

✅ **Modules and Packages**
- Creating custom modules
- Importing modules (import, from...import)
- Built-in Python modules
- Creating package structures
- Module initialization

✅ **DevOps Applications**
- Reusable server management functions
- Configuration generators
- Deployment pipelines
- Monitoring utilities
- Code organization for automation

---

## Next Steps

- Move on to **LAB-05: File Operations** to work with configuration files
- Practice creating your own utility modules
- Refactor previous lab code into reusable functions
- Create a package for your automation scripts

## Additional Resources

- [Python Functions Documentation](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python Modules](https://docs.python.org/3/tutorial/modules.html)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Python Packages](https://docs.python.org/3/tutorial/modules.html#packages)
