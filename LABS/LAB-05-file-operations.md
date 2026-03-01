# LAB 05: File Operations for DevOps

## Learning Objectives
By the end of this lab, you will be able to:
- Read from and write to text files
- Work with CSV files for structured data
- Parse and generate JSON configuration files
- Read and write YAML files using PyYAML
- Handle file paths with pathlib
- Implement error handling for file operations
- Process log files and configuration files

## Prerequisites
- Completed LAB-01 through LAB-04
- Understanding of functions and exception handling
- PyYAML installed: `pip install pyyaml`

---

## Part 1: Basic File Operations

### Exercise 1.1: Reading Text Files

Create a sample log file `sample.log`:
```
2024-01-15 10:00:00 INFO Application started
2024-01-15 10:00:15 INFO Connected to database
2024-01-15 10:01:30 WARNING High memory usage: 85%
2024-01-15 10:02:45 ERROR Connection timeout
2024-01-15 10:03:00 INFO Retrying connection
2024-01-15 10:03:15 INFO Connection restored
2024-01-15 10:05:20 ERROR Disk space low: 5% remaining
```

Create `read_files.py`:

```python
# Method 1: Read entire file
print("Method 1: Read entire file")
file = open("sample.log", "r")
content = file.read()
print(content)
file.close()

# Method 2: Read with context manager (recommended)
print("\nMethod 2: Using context manager")
with open("sample.log", "r") as file:
    content = file.read()
    print(content)
# File automatically closed

# Method 3: Read line by line
print("\nMethod 3: Read line by line")
with open("sample.log", "r") as file:
    for line in file:
        print(line.strip())

# Method 4: Read all lines into list
print("\nMethod 4: Read lines into list")
with open("sample.log", "r") as file:
    lines = file.readlines()
    print(f"Total lines: {len(lines)}")
    print(f"First line: {lines[0].strip()}")
    print(f"Last line: {lines[-1].strip()}")

# Process log file - extract ERROR lines
print("\nError lines only:")
with open("sample.log", "r") as file:
    for line in file:
        if "ERROR" in line:
            print(line.strip())
```

**Expected Output:**
```
Method 1: Read entire file
2024-01-15 10:00:00 INFO Application started
2024-01-15 10:00:15 INFO Connected to database
2024-01-15 10:01:30 WARNING High memory usage: 85%
2024-01-15 10:02:45 ERROR Connection timeout
2024-01-15 10:03:00 INFO Retrying connection
2024-01-15 10:03:15 INFO Connection restored
2024-01-15 10:05:20 ERROR Disk space low: 5% remaining

Method 2: Using context manager
[same content]

Method 3: Read line by line
[same content, one line at a time]

Method 4: Read lines into list
Total lines: 7
First line: 2024-01-15 10:00:00 INFO Application started
Last line: 2024-01-15 10:05:20 ERROR Disk space low: 5% remaining

Error lines only:
2024-01-15 10:02:45 ERROR Connection timeout
2024-01-15 10:05:20 ERROR Disk space low: 5% remaining
```

### Exercise 1.2: Writing Text Files

```python
# Write to file (overwrites existing content)
servers = ["web-01", "web-02", "db-01", "cache-01"]

with open("servers.txt", "w") as file:
    for server in servers:
        file.write(f"{server}\n")

print("Created servers.txt")

# Append to file
with open("servers.txt", "a") as file:
    file.write("api-01\n")
    file.write("worker-01\n")

print("Appended to servers.txt")

# Verify
with open("servers.txt", "r") as file:
    content = file.read()
    print(f"\nFile contents:\n{content}")

# Write multiple lines at once
log_entries = [
    "2024-01-15 11:00:00 INFO Service started\n",
    "2024-01-15 11:00:15 INFO Processing requests\n",
    "2024-01-15 11:01:00 INFO Backup completed\n"
]

with open("service.log", "w") as file:
    file.writelines(log_entries)

print("Created service.log")

# Generate a server report
server_metrics = [
    {"name": "web-01", "cpu": 45.2, "memory": 67.8},
    {"name": "web-02", "cpu": 78.9, "memory": 82.1},
    {"name": "db-01", "cpu": 62.3, "memory": 88.5}
]

with open("server_report.txt", "w") as file:
    file.write("SERVER HEALTH REPORT\n")
    file.write("=" * 50 + "\n\n")
    
    for server in server_metrics:
        file.write(f"Server: {server['name']}\n")
        file.write(f"  CPU: {server['cpu']}%\n")
        file.write(f"  Memory: {server['memory']}%\n")
        file.write("\n")
    
    file.write("=" * 50 + "\n")

print("Created server_report.txt")
```

### Exercise 1.3: File Error Handling

```python
def read_config_file(filename):
    """Read config file with error handling"""
    try:
        with open(filename, "r") as file:
            content = file.read()
            return True, content
    
    except FileNotFoundError:
        return False, f"File '{filename}' not found"
    
    except PermissionError:
        return False, f"Permission denied to read '{filename}'"
    
    except Exception as e:
        return False, f"Error reading file: {e}"

# Test with existing file
success, result = read_config_file("sample.log")
if success:
    print(f"File read successfully ({len(result)} bytes)")
else:
    print(f"Error: {result}")

# Test with non-existent file
success, result = read_config_file("missing.txt")
if success:
    print(f"File read successfully")
else:
    print(f"Error: {result}")

# Safe file writing
def safe_write_file(filename, content):
    """Write file with error handling"""
    try:
        with open(filename, "w") as file:
            file.write(content)
        return True, f"Successfully wrote to {filename}"
    
    except PermissionError:
        return False, f"Permission denied to write '{filename}'"
    
    except Exception as e:
        return False, f"Error writing file: {e}"

success, message = safe_write_file("output.txt", "Test content")
print(message)
```

---

## Part 2: CSV File Operations

### Exercise 2.1: Reading CSV Files

Create `servers.csv`:
```csv
hostname,ip_address,port,environment,cpu,memory
web-01,10.0.1.10,8080,production,45.2,67.8
web-02,10.0.1.11,8080,production,78.9,82.1
db-01,10.0.2.10,5432,production,62.3,88.5
cache-01,10.0.3.10,6379,staging,34.5,45.2
api-01,10.0.4.10,8000,production,91.2,93.4
```

Create `csv_operations.py`:

```python
import csv

# Method 1: Read CSV as list of lists
print("Method 1: List of lists")
with open("servers.csv", "r") as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Skip header
    
    for row in csv_reader:
        print(f"{row[0]}: {row[1]}:{row[2]}")

# Method 2: Read CSV as dictionary (recommended)
print("\nMethod 2: Dictionary reader")
with open("servers.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        print(f"{row['hostname']}: CPU {row['cpu']}%, Memory {row['memory']}%")

# Filter high CPU servers
print("\nHigh CPU servers (>60%):")
with open("servers.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        if float(row['cpu']) > 60:
            print(f"  {row['hostname']}: {row['cpu']}%")

# Load CSV into list of dictionaries
servers = []
with open("servers.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    servers = list(csv_reader)

print(f"\nLoaded {len(servers)} servers")

# Calculate average CPU
total_cpu = sum(float(s['cpu']) for s in servers)
avg_cpu = total_cpu / len(servers)
print(f"Average CPU: {avg_cpu:.1f}%")

# Group by environment
from collections import defaultdict

by_env = defaultdict(list)
for server in servers:
    by_env[server['environment']].append(server['hostname'])

print("\nServers by environment:")
for env, server_list in by_env.items():
    print(f"  {env}: {', '.join(server_list)}")
```

### Exercise 2.2: Writing CSV Files

```python
import csv

# Method 1: Write list of lists
data = [
    ["hostname", "status", "uptime_days"],
    ["web-01", "active", "30"],
    ["web-02", "active", "25"],
    ["db-01", "maintenance", "15"]
]

with open("server_status.csv", "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)

print("Created server_status.csv")

# Method 2: Write dictionaries (recommended)
servers = [
    {"hostname": "web-01", "cpu": 45.2, "memory": 67.8, "status": "healthy"},
    {"hostname": "web-02", "cpu": 78.9, "memory": 82.1, "status": "warning"},
    {"hostname": "db-01", "cpu": 92.3, "memory": 88.5, "status": "critical"}
]

with open("server_metrics.csv", "w", newline="") as file:
    fieldnames = ["hostname", "cpu", "memory", "status"]
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    csv_writer.writeheader()
    csv_writer.writerows(servers)

print("Created server_metrics.csv")

# Generate report from data
print("\nGenerating performance report...")
with open("servers.csv", "r") as infile, \
     open("high_usage_report.csv", "w", newline="") as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = ["hostname", "environment", "cpu", "memory", "alert_level"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for row in reader:
        cpu = float(row['cpu'])
        memory = float(row['memory'])
        
        # Determine alert level
        if cpu > 80 or memory > 85:
            alert_level = "CRITICAL"
        elif cpu > 60 or memory > 70:
            alert_level = "WARNING"
        else:
            alert_level = "OK"
        
        # Only write servers with warnings or critical alerts
        if alert_level in ["WARNING", "CRITICAL"]:
            writer.writerow({
                "hostname": row['hostname'],
                "environment": row['environment'],
                "cpu": row['cpu'],
                "memory": row['memory'],
                "alert_level": alert_level
            })

print("Created high_usage_report.csv")
```

---

## Part 3: JSON File Operations

### Exercise 3.1: Reading JSON Files

Create `config.json`:
```json
{
  "app_name": "payment-api",
  "version": "1.2.3",
  "environment": "production",
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "workers": 4,
    "timeout": 30
  },
  "database": {
    "host": "db.example.com",
    "port": 5432,
    "name": "payments",
    "pool_size": 10
  },
  "features": {
    "logging": true,
    "metrics": true,
    "rate_limiting": false
  },
  "allowed_origins": [
    "https://app.example.com",
    "https://admin.example.com"
  ]
}
```

Create `json_operations.py`:

```python
import json

# Read JSON file
print("Reading JSON configuration:")
with open("config.json", "r") as file:
    config = json.load(file)

print(f"App: {config['app_name']} v{config['version']}")
print(f"Environment: {config['environment']}")
print(f"Server port: {config['server']['port']}")
print(f"Database: {config['database']['name']}")
print(f"Features: {config['features']}")
print(f"Allowed origins: {config['allowed_origins']}")

# Access nested data
server_config = config['server']
print(f"\nServer configuration:")
for key, value in server_config.items():
    print(f"  {key}: {value}")

# Modify configuration
config['server']['port'] = 8443
config['features']['rate_limiting'] = True
config['version'] = "1.2.4"

print(f"\nUpdated port: {config['server']['port']}")
print(f"Updated version: {config['version']}")

# Parse JSON string
json_string = '{"status": "healthy", "cpu": 45.2, "memory": 67.8}'
metrics = json.loads(json_string)
print(f"\nParsed metrics: {metrics}")

# Pretty print JSON
print("\nPretty printed config:")
print(json.dumps(config, indent=2))

# Handle JSON parsing errors
def safe_parse_json(json_string):
    """Parse JSON with error handling"""
    try:
        return True, json.loads(json_string)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

# Test with valid JSON
success, result = safe_parse_json('{"name": "server-01"}')
print(f"\nValid JSON: {result}")

# Test with invalid JSON
success, result = safe_parse_json('{invalid json}')
print(f"Invalid JSON: {result}")
```

### Exercise 3.2: Writing JSON Files

```python
import json
from datetime import datetime

# Create configuration
app_config = {
    "app_name": "monitoring-service",
    "version": "2.0.0",
    "created_at": datetime.now().isoformat(),
    "settings": {
        "check_interval": 60,
        "alert_threshold": 80,
        "retry_attempts": 3
    },
    "servers": [
        {"name": "web-01", "ip": "10.0.1.10"},
        {"name": "web-02", "ip": "10.0.1.11"},
        {"name": "db-01", "ip": "10.0.2.10"}
    ],
    "notifications": {
        "email": True,
        "slack": True,
        "pagerduty": False
    }
}

# Write JSON file (pretty formatted)
with open("app_config.json", "w") as file:
    json.dump(app_config, file, indent=2)

print("Created app_config.json with pretty formatting")

# Write compact JSON (no indentation)
with open("app_config_compact.json", "w") as file:
    json.dump(app_config, file)

print("Created app_config_compact.json (compact)")

# Convert Python objects to JSON strings
server_data = {
    "hostname": "web-01",
    "metrics": {"cpu": 45.2, "memory": 67.8},
    "active": True
}

json_string = json.dumps(server_data)
print(f"\nJSON string: {json_string}")

# Pretty JSON string
json_pretty = json.dumps(server_data, indent=2)
print(f"\nPretty JSON string:\n{json_pretty}")

# Update existing JSON file
def update_json_config(filename, updates):
    """Update JSON config file with new values"""
    try:
        # Read existing config
        with open(filename, "r") as file:
            config = json.load(file)
        
        # Update config
        config.update(updates)
        
        # Write back
        with open(filename, "w") as file:
            json.dump(config, file, indent=2)
        
        return True, "Config updated successfully"
    
    except FileNotFoundError:
        return False, f"File {filename} not found"
    except Exception as e:
        return False, f"Error updating config: {e}"

# Test update
success, message = update_json_config("app_config.json", {
    "version": "2.0.1",
    "updated_at": datetime.now().isoformat()
})
print(f"\n{message}")
```

---

## Part 4: YAML File Operations

### Exercise 4.1: Reading YAML Files

Create `deployment.yaml`:
```yaml
apiVersion: v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web
    environment: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
          requests:
            cpu: "0.5"
            memory: "256Mi"
        env:
        - name: ENVIRONMENT
          value: production
        - name: LOG_LEVEL
          value: info
```

Create `yaml_operations.py`:

```python
import yaml

# Read YAML file
print("Reading YAML deployment:")
with open("deployment.yaml", "r") as file:
    deployment = yaml.safe_load(file)

print(f"Kind: {deployment['kind']}")
print(f"Name: {deployment['metadata']['name']}")
print(f"Replicas: {deployment['spec']['replicas']}")

# Access nested data
container = deployment['spec']['template']['spec']['containers'][0]
print(f"\nContainer name: {container['name']}")
print(f"Image: {container['image']}")
print(f"Port: {container['ports'][0]['containerPort']}")

# Print environment variables
print("\nEnvironment variables:")
for env in container['env']:
    print(f"  {env['name']}: {env['value']}")

# Print resource limits
resources = container['resources']
print("\nResource limits:")
print(f"  CPU: {resources['limits']['cpu']}")
print(f"  Memory: {resources['limits']['memory']}")

# Read multiple YAML documents
yaml_multi = """
---
name: web-01
ip: 10.0.1.10
---
name: web-02
ip: 10.0.1.11
---
name: db-01
ip: 10.0.2.10
"""

documents = yaml.safe_load_all(yaml_multi)
print("\nMultiple YAML documents:")
for doc in documents:
    print(f"  {doc['name']}: {doc['ip']}")
```

### Exercise 4.2: Writing YAML Files

```python
import yaml

# Create server configuration
server_config = {
    "server": {
        "name": "web-prod-01",
        "environment": "production",
        "host": "0.0.0.0",
        "port": 8080,
        "workers": 4
    },
    "database": {
        "host": "db.example.com",
        "port": 5432,
        "name": "webapp",
        "pool": {
            "min_connections": 5,
            "max_connections": 20
        }
    },
    "logging": {
        "level": "info",
        "format": "json",
        "outputs": ["stdout", "file"]
    },
    "features": ["authentication", "api", "admin"],
    "metrics": {
        "enabled": True,
        "interval": 60,
        "exporters": ["prometheus", "statsd"]
    }
}

# Write YAML file
with open("server_config.yaml", "w") as file:
    yaml.dump(server_config, file, default_flow_style=False)

print("Created server_config.yaml")

# Write with custom formatting
with open("server_config_formatted.yaml", "w") as file:
    yaml.dump(server_config, file, 
              default_flow_style=False,
              sort_keys=False,
              indent=2)

print("Created server_config_formatted.yaml")

# Write multiple documents
servers = [
    {"name": "web-01", "ip": "10.0.1.10", "role": "web"},
    {"name": "web-02", "ip": "10.0.1.11", "role": "web"},
    {"name": "db-01", "ip": "10.0.2.10", "role": "database"}
]

with open("servers.yaml", "w") as file:
    yaml.dump_all(servers, file, default_flow_style=False)

print("Created servers.yaml with multiple documents")

# Update YAML file
def update_yaml_config(filename, path, value):
    """Update value in YAML file using dot notation path"""
    try:
        with open(filename, "r") as file:
            config = yaml.safe_load(file)
        
        # Navigate to nested key (simple implementation)
        keys = path.split('.')
        current = config
        for key in keys[:-1]:
            current = current[key]
        current[keys[-1]] = value
        
        with open(filename, "w") as file:
            yaml.dump(config, file, default_flow_style=False)
        
        return True, f"Updated {path} to {value}"
    
    except Exception as e:
        return False, f"Error updating YAML: {e}"

# Test update
success, message = update_yaml_config(
    "server_config.yaml",
    "server.port",
    8443
)
print(f"\n{message}")
```

---

## Part 5: Pathlib for Modern Path Handling

### Exercise 5.1: Working with Pathlib

Create `pathlib_operations.py`:

```python
from pathlib import Path

# Current directory
current_dir = Path.cwd()
print(f"Current directory: {current_dir}")

# Home directory
home_dir = Path.home()
print(f"Home directory: {home_dir}")

# Create path objects
log_file = Path("logs/application.log")
config_file = Path("config") / "settings.yaml"  # Path joining

print(f"\nLog file path: {log_file}")
print(f"Config file path: {config_file}")

# Path properties
print(f"\nLog file name: {log_file.name}")
print(f"Log file suffix: {log_file.suffix}")
print(f"Log file stem: {log_file.stem}")
print(f"Log file parent: {log_file.parent}")

# Check if path exists
sample_log = Path("sample.log")
print(f"\nsample.log exists: {sample_log.exists()}")
print(f"Is file: {sample_log.is_file()}")
print(f"Is directory: {sample_log.is_dir()}")

# Create directories
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)  # Create if doesn't exist
print(f"\nCreated directory: {log_dir}")

# Create nested directories
nested_dir = Path("data/backups/2024")
nested_dir.mkdir(parents=True, exist_ok=True)
print(f"Created nested directory: {nested_dir}")

# List files in directory
print("\nFiles in current directory:")
for item in Path(".").iterdir():
    if item.is_file():
        print(f"  {item.name}")

# Find all .py files
print("\nPython files:")
for py_file in Path(".").glob("*.py"):
    print(f"  {py_file.name}")

# Recursive search for .yaml files
print("\nYAML files (recursive):")
for yaml_file in Path(".").rglob("*.yaml"):
    print(f"  {yaml_file}")

# Read and write with pathlib
config_path = Path("app_config.json")
if config_path.exists():
    content = config_path.read_text()
    print(f"\nRead {len(content)} bytes from {config_path.name}")

# Write file
output_path = Path("output.txt")
output_path.write_text("This is test content\n")
print(f"Wrote to {output_path}")

# Get file info
if sample_log.exists():
    stat = sample_log.stat()
    print(f"\nFile size: {stat.st_size} bytes")
    print(f"Modified time: {stat.st_mtime}")

# Resolve absolute path
abs_path = sample_log.resolve()
print(f"\nAbsolute path: {abs_path}")
```

### Exercise 5.2: Path Utility Functions

```python
from pathlib import Path
import shutil

def organize_files_by_extension(source_dir):
    """Organize files into subdirectories by extension"""
    source = Path(source_dir)
    
    if not source.exists():
        return False, f"Directory {source_dir} not found"
    
    # Get all files
    files = [f for f in source.iterdir() if f.is_file()]
    
    for file in files:
        ext = file.suffix[1:] if file.suffix else "no_extension"
        
        # Create directory for extension
        target_dir = source / ext
        target_dir.mkdir(exist_ok=True)
        
        # Move file
        target_file = target_dir / file.name
        if not target_file.exists():
            shutil.move(str(file), str(target_file))
            print(f"  Moved {file.name} to {ext}/")
    
    return True, "Files organized successfully"

def find_large_files(directory, size_mb=10):
    """Find files larger than specified size"""
    dir_path = Path(directory)
    large_files = []
    
    for file in dir_path.rglob("*"):
        if file.is_file():
            size_bytes = file.stat().st_size
            size_mb_actual = size_bytes / (1024 * 1024)
            
            if size_mb_actual > size_mb:
                large_files.append({
                    "path": file,
                    "size_mb": round(size_mb_actual, 2)
                })
    
    return large_files

def backup_config_files(source_dir, backup_dir):
    """Backup all configuration files"""
    source = Path(source_dir)
    backup = Path(backup_dir)
    
    # Create backup directory
    backup.mkdir(parents=True, exist_ok=True)
    
    # Config file extensions
    config_extensions = [".yaml", ".yml", ".json", ".conf", ".cfg"]
    
    backed_up = []
    for ext in config_extensions:
        for config_file in source.rglob(f"*{ext}"):
            if config_file.is_file():
                target = backup / config_file.name
                shutil.copy2(str(config_file), str(target))
                backed_up.append(config_file.name)
    
    return backed_up

# Test functions
print("Testing path utilities:\n")

# Find Python files
py_files = list(Path(".").glob("*.py"))
print(f"Found {len(py_files)} Python files")

# Simulate finding large files
print("\nSearching for large files...")
# large = find_large_files(".", size_mb=0.001)
# for file in large[:5]:
#     print(f"  {file['path'].name}: {file['size_mb']} MB")
```

---

## Part 6: Practice Challenges

### Challenge 1: Log Analyzer

Create a script that analyzes log files:

```python
# Your task: Analyze sample.log
# 1. Count logs by level (INFO, WARNING, ERROR)
# 2. Find all ERROR messages
# 3. Calculate time between first and last log entry
# 4. Write summary to analysis_report.txt

# Expected output in report:
# - Total lines
# - Counts per log level
# - List of all ERROR messages
# - Time span of logs
```

<details>
<summary>Solution</summary>

```python
from datetime import datetime
from collections import Counter

def analyze_log_file(filename):
    """Analyze log file and generate report"""
    
    with open(filename, "r") as file:
        lines = file.readlines()
    
    # Count by level
    levels = []
    errors = []
    timestamps = []
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            timestamp_str = f"{parts[0]} {parts[1]}"
            level = parts[2]
            message = " ".join(parts[3:])
            
            levels.append(level)
            timestamps.append(timestamp_str)
            
            if level == "ERROR":
                errors.append(line.strip())
    
    # Count levels
    level_counts = Counter(levels)
    
    # Time span
    if timestamps:
        first = datetime.strptime(timestamps[0], "%Y-%m-%d %H:%M:%S")
        last = datetime.strptime(timestamps[-1], "%Y-%m-%d %H:%M:%S")
        duration = last - first
    else:
        duration = None
    
    # Write report
    with open("analysis_report.txt", "w") as report:
        report.write("LOG ANALYSIS REPORT\n")
        report.write("=" * 50 + "\n\n")
        report.write(f"Total lines: {len(lines)}\n\n")
        
        report.write("Counts by level:\n")
        for level, count in level_counts.items():
            report.write(f"  {level}: {count}\n")
        
        report.write(f"\nERROR messages:\n")
        for error in errors:
            report.write(f"  {error}\n")
        
        if duration:
            report.write(f"\nTime span: {duration}\n")
        
        report.write("\n" + "=" * 50 + "\n")
    
    return True, "Analysis complete"

# Run analysis
success, message = analyze_log_file("sample.log")
print(message)

# Read and display report
with open("analysis_report.txt", "r") as file:
    print("\n" + file.read())
```
</details>

### Challenge 2: Configuration Merger

Merge multiple configuration files:

```python
# Your task:
# 1. Read config.json
# 2. Read server_config.yaml
# 3. Merge them into a single configuration
# 4. Write merged config to merged_config.json and merged_config.yaml
# 5. Handle conflicts (JSON values take precedence)
```

<details>
<summary>Solution</summary>

```python
import json
import yaml

def merge_configs(json_file, yaml_file):
    """Merge JSON and YAML config files"""
    
    # Read JSON config
    with open(json_file, "r") as file:
        json_config = json.load(file)
    
    # Read YAML config
    with open(yaml_file, "r") as file:
        yaml_config = yaml.safe_load(file)
    
    # Merge (JSON takes precedence)
    merged = yaml_config.copy()
    merged.update(json_config)
    
    # Write as JSON
    with open("merged_config.json", "w") as file:
        json.dump(merged, file, indent=2)
    
    # Write as YAML
    with open("merged_config.yaml", "w") as file:
        yaml.dump(merged, file, default_flow_style=False)
    
    return merged

# Test (if files exist)
try:
    merged = merge_configs("config.json", "server_config.yaml")
    print("Configuration merged successfully")
    print(f"Total keys: {len(merged)}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
```
</details>

### Challenge 3: Backup Manager

Create a backup management system:

```python
# Your task:
# 1. Create function to backup all .yaml and .json files
# 2. Store backups in backups/YYYY-MM-DD/ directory
# 3. Create manifest file listing all backed up files
# 4. Add function to restore from backup
```

<details>
<summary>Solution</summary>

```python
from pathlib import Path
from datetime import datetime
import shutil
import json

def create_backup(source_dir="."):
    """Create backup of config files"""
    
    # Create backup directory with timestamp
    today = datetime.now().strftime("%Y-%m-%d")
    backup_dir = Path("backups") / today
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Find config files
    source = Path(source_dir)
    config_files = []
    
    for pattern in ["*.json", "*.yaml", "*.yml"]:
        config_files.extend(source.glob(pattern))
    
    # Backup files
    manifest = {
        "backup_date": today,
        "backup_time": datetime.now().isoformat(),
        "files": []
    }
    
    for file in config_files:
        if file.is_file():
            target = backup_dir / file.name
            shutil.copy2(file, target)
            
            manifest["files"].append({
                "name": file.name,
                "size": file.stat().st_size,
                "original_path": str(file)
            })
            
            print(f"Backed up: {file.name}")
    
    # Write manifest
    manifest_file = backup_dir / "manifest.json"
    with open(manifest_file, "w") as file:
        json.dump(manifest, file, indent=2)
    
    print(f"\nBackup created: {backup_dir}")
    print(f"Files backed up: {len(manifest['files'])}")
    
    return str(backup_dir)

def restore_backup(backup_dir, target_dir="."):
    """Restore files from backup"""
    
    backup = Path(backup_dir)
    target = Path(target_dir)
    
    # Read manifest
    manifest_file = backup / "manifest.json"
    with open(manifest_file, "r") as file:
        manifest = json.load(file)
    
    # Restore files
    for file_info in manifest["files"]:
        source_file = backup / file_info["name"]
        target_file = target / file_info["name"]
        
        shutil.copy2(source_file, target_file)
        print(f"Restored: {file_info['name']}")
    
    print(f"\nRestored {len(manifest['files'])} files from {backup_dir}")

# Test backup
backup_path = create_backup()
```
</details>

---

## Part 7: Real-World Scenario

### Scenario: Multi-Format Configuration Manager

Create `config_manager.py`:

```python
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    """Manage configuration files in multiple formats"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.configs: Dict[str, Any] = {}
    
    def load_json(self, filename: str) -> bool:
        """Load JSON configuration"""
        try:
            file_path = self.config_dir / filename
            with open(file_path, "r") as file:
                self.configs[filename] = json.load(file)
            return True
        except Exception as e:
            print(f"Error loading JSON {filename}: {e}")
            return False
    
    def load_yaml(self, filename: str) -> bool:
        """Load YAML configuration"""
        try:
            file_path = self.config_dir / filename
            with open(file_path, "r") as file:
                self.configs[filename] = yaml.safe_load(file)
            return True
        except Exception as e:
            print(f"Error loading YAML {filename}: {e}")
            return False
    
    def load_all(self):
        """Load all config files from directory"""
        for file in self.config_dir.iterdir():
            if file.suffix == ".json":
                self.load_json(file.name)
            elif file.suffix in [".yaml", ".yml"]:
                self.load_yaml(file.name)
    
    def get_config(self, filename: str) -> Optional[Dict]:
        """Get loaded configuration"""
        return self.configs.get(filename)
    
    def save_json(self, filename: str, config: Dict):
        """Save configuration as JSON"""
        file_path = self.config_dir / filename
        with open(file_path, "w") as file:
            json.dump(config, file, indent=2)
        self.configs[filename] = config
    
    def save_yaml(self, filename: str, config: Dict):
        """Save configuration as YAML"""
        file_path = self.config_dir / filename
        with open(file_path, "w") as file:
            yaml.dump(config, file, default_flow_style=False)
        self.configs[filename] = config
    
    def list_configs(self):
        """List all loaded configurations"""
        return list(self.configs.keys())
    
    def validate_config(self, filename: str, required_keys: list) -> bool:
        """Validate configuration has required keys"""
        config = self.get_config(filename)
        if not config:
            return False
        
        for key in required_keys:
            if key not in config:
                print(f"Missing required key: {key}")
                return False
        
        return True

# Usage example
if __name__ == "__main__":
    manager = ConfigManager()
    
    # Create sample config
    app_config = {
        "app_name": "demo-app",
        "version": "1.0.0",
        "server": {"port": 8080, "host": "0.0.0.0"}
    }
    
    # Save in both formats
    manager.save_json("app.json", app_config)
    manager.save_yaml("app.yaml", app_config)
    
    print("Configurations saved")
    print(f"Loaded configs: {manager.list_configs()}")
    
    # Validate
    valid = manager.validate_config("app.json", ["app_name", "version"])
    print(f"Configuration valid: {valid}")
```

---

## What You Learned

In this lab, you learned:

✅ **File Operations**
- Reading and writing text files
- Using context managers (with statement)
- Error handling for file operations
- Processing log files

✅ **CSV Files**
- Reading CSV with csv.reader and csv.DictReader
- Writing CSV with csv.writer and csv.DictWriter
- Processing tabular data
- Generating reports

✅ **JSON Files**
- Parsing JSON with json.load/loads
- Writing JSON with json.dump/dumps
- Working with nested JSON structures
- Pretty printing JSON

✅ **YAML Files**
- Reading YAML with yaml.safe_load
- Writing YAML with yaml.dump
- Handling multiple YAML documents
- YAML vs JSON trade-offs

✅ **Pathlib**
- Modern path handling with Path objects
- Path manipulation and properties
- Directory operations
- File searching with glob/rglob

✅ **DevOps Applications**
- Configuration file management
- Log file analysis
- Backup and restore operations
- Multi-format config handling

---

## Next Steps

- Move on to **LAB-06: OS and Subprocess** to execute system commands
- Practice reading real configuration files from applications
- Create automated backup scripts
- Build configuration validation tools

## Additional Resources

- [Python File I/O](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [CSV Module](https://docs.python.org/3/library/csv.html)
- [JSON Module](https://docs.python.org/3/library/json.html)
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Pathlib](https://docs.python.org/3/library/pathlib.html)
