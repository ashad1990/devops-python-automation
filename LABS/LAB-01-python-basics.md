# LAB 01: Python Basics for DevOps

## Learning Objectives
By the end of this lab, you will be able to:
- Declare and use variables with appropriate naming conventions
- Work with Python data types (strings, integers, floats, booleans)
- Use arithmetic, comparison, and logical operators
- Manipulate strings and use f-strings for formatting
- Apply basic Python syntax to DevOps automation tasks

## Prerequisites
- Python 3.8+ installed
- Text editor or IDE
- Basic command line knowledge

---

## Part 1: Variables and Data Types

### Exercise 1.1: Server Configuration Variables

Create a file called `server_info.py` and declare variables for server configuration:

```python
# Server configuration variables
server_name = "web-server-01"
ip_address = "192.168.1.100"
port = 8080
is_active = True
cpu_usage = 45.7
memory_gb = 16

# Print variable types
print(f"Server Name: {server_name} (Type: {type(server_name).__name__})")
print(f"IP Address: {ip_address} (Type: {type(ip_address).__name__})")
print(f"Port: {port} (Type: {type(port).__name__})")
print(f"Is Active: {is_active} (Type: {type(is_active).__name__})")
print(f"CPU Usage: {cpu_usage}% (Type: {type(cpu_usage).__name__})")
print(f"Memory: {memory_gb}GB (Type: {type(memory_gb).__name__})")
```

**Expected Output:**
```
Server Name: web-server-01 (Type: str)
IP Address: 192.168.1.100 (Type: str)
Port: 8080 (Type: int)
Is Active: True (Type: bool)
CPU Usage: 45.7% (Type: float)
Memory: 16GB (Type: int)
```

### Exercise 1.2: Type Conversion for Port Configuration

```python
# Port number as string (from config file)
port_string = "8080"

# Convert to integer for comparison
port_number = int(port_string)

# Check if port is in valid range
min_port = 1024
max_port = 65535

is_valid_port = min_port <= port_number <= max_port
print(f"Port {port_number} is valid: {is_valid_port}")

# Convert boolean to string for logging
status = "enabled" if is_active else "disabled"
print(f"Server status: {status}")
```

**Expected Output:**
```
Port 8080 is valid: True
Server status: enabled
```

---

## Part 2: Operators

### Exercise 2.1: Arithmetic Operators for Resource Calculation

Create `resource_calculator.py`:

```python
# Server resource calculations
total_memory_gb = 64
used_memory_gb = 48

# Calculate available memory
available_memory = total_memory_gb - used_memory_gb
print(f"Available Memory: {available_memory}GB")

# Calculate memory usage percentage
memory_usage_percent = (used_memory_gb / total_memory_gb) * 100
print(f"Memory Usage: {memory_usage_percent:.2f}%")

# Calculate memory per container (integer division)
num_containers = 5
memory_per_container = used_memory_gb // num_containers
memory_remainder = used_memory_gb % num_containers
print(f"Memory per container: {memory_per_container}GB")
print(f"Remainder: {memory_remainder}GB")

# Exponential calculation for storage
base_storage_mb = 100
growth_factor = 2
days = 3
projected_storage = base_storage_mb * (growth_factor ** days)
print(f"Projected storage after {days} days: {projected_storage}MB")
```

**Expected Output:**
```
Available Memory: 16GB
Memory Usage: 75.00%
Memory per container: 9GB
Remainder: 3GB
Projected storage after 3 days: 800MB
```

### Exercise 2.2: Comparison and Logical Operators for Alerting

```python
# Server metrics
cpu_usage = 85
memory_usage = 72
disk_usage = 90
response_time_ms = 1500

# Thresholds
cpu_threshold = 80
memory_threshold = 80
disk_threshold = 85
response_threshold = 1000

# Check individual conditions
cpu_alert = cpu_usage > cpu_threshold
memory_alert = memory_usage > memory_threshold
disk_alert = disk_usage > disk_threshold
response_alert = response_time_ms > response_threshold

print(f"CPU Alert: {cpu_alert}")
print(f"Memory Alert: {memory_alert}")
print(f"Disk Alert: {disk_alert}")
print(f"Response Time Alert: {response_alert}")

# Combined conditions
critical_alert = cpu_alert and disk_alert
any_alert = cpu_alert or memory_alert or disk_alert or response_alert
healthy = not any_alert

print(f"\nCritical Alert (CPU AND Disk): {critical_alert}")
print(f"Any Alert: {any_alert}")
print(f"Server Healthy: {healthy}")
```

**Expected Output:**
```
CPU Alert: True
Memory Alert: False
Disk Alert: True
Response Time Alert: True

Critical Alert (CPU AND Disk): True
Any Alert: True
Server Healthy: False
```

---

## Part 3: String Manipulation

### Exercise 3.1: String Operations for Log Processing

Create `log_processor.py`:

```python
# Sample log line
log_line = "  2024-01-15 14:32:45 ERROR Connection timeout on server-prod-01  "

# String cleaning
cleaned_log = log_line.strip()
print(f"Cleaned: '{cleaned_log}'")

# Extract log level
log_level = cleaned_log.split()[2]
print(f"Log Level: {log_level}")

# Check log severity
is_error = "ERROR" in log_line
is_critical = "CRITICAL" in log_line
print(f"Is Error: {is_error}")
print(f"Is Critical: {is_critical}")

# Case conversion
log_level_lower = log_level.lower()
log_level_upper = log_level.upper()
print(f"Lowercase: {log_level_lower}")
print(f"Uppercase: {log_level_upper}")

# String replacement
sanitized_log = log_line.replace("ERROR", "WARN")
print(f"Sanitized: {sanitized_log}")

# Check string properties
server_name = "web-server-01"
print(f"\nServer name is alphanumeric: {server_name.replace('-', '').isalnum()}")
print(f"Starts with 'web': {server_name.startswith('web')}")
print(f"Ends with '01': {server_name.endswith('01')}")
```

**Expected Output:**
```
Cleaned: '2024-01-15 14:32:45 ERROR Connection timeout on server-prod-01'
Log Level: ERROR
Is Error: True
Is Critical: False
Lowercase: error
Uppercase: ERROR
Sanitized:   2024-01-15 14:32:45 WARN Connection timeout on server-prod-01  
Server name is alphanumeric: True
Starts with 'web': True
Ends with '01': True
```

### Exercise 3.2: String Indexing and Slicing

```python
# Server hostname
hostname = "web-prod-us-east-1a"

# String indexing
first_char = hostname[0]
last_char = hostname[-1]
print(f"First character: {first_char}")
print(f"Last character: {last_char}")

# String slicing
server_type = hostname[0:3]  # First 3 characters
environment = hostname[4:8]  # Characters 4-7
region = hostname[9:16]  # Region portion
zone = hostname[-2:]  # Last 2 characters

print(f"Server Type: {server_type}")
print(f"Environment: {environment}")
print(f"Region: {region}")
print(f"Availability Zone: {zone}")

# Reverse string
reversed_hostname = hostname[::-1]
print(f"Reversed: {reversed_hostname}")

# Every other character
every_other = hostname[::2]
print(f"Every other char: {every_other}")
```

**Expected Output:**
```
First character: w
Last character: a
Server Type: web
Environment: prod
Region: us-east
Availability Zone: 1a
Reversed: a1-tsae-su-dorp-bew
Every other char: wbpodu-at1
```

---

## Part 4: F-Strings and String Formatting

### Exercise 4.1: Formatted Server Reports

Create `server_report.py`:

```python
# Server metrics
server_name = "app-server-03"
uptime_hours = 720
cpu_percent = 67.8
memory_percent = 82.3
disk_percent = 45.9
num_requests = 1250000

# Basic f-string formatting
print(f"Server: {server_name}")
print(f"Uptime: {uptime_hours} hours")

# Number formatting
uptime_days = uptime_hours / 24
print(f"Uptime: {uptime_days:.1f} days")

# Percentage formatting
print(f"CPU Usage: {cpu_percent:.1f}%")
print(f"Memory Usage: {memory_percent:.1f}%")
print(f"Disk Usage: {disk_percent:.1f}%")

# Large number formatting with comma separators
print(f"Total Requests: {num_requests:,}")

# Aligned output
print("\n--- Formatted Report ---")
print(f"{'Metric':<15} {'Value':>10}")
print(f"{'-' * 25}")
print(f"{'CPU':<15} {cpu_percent:>9.1f}%")
print(f"{'Memory':<15} {memory_percent:>9.1f}%")
print(f"{'Disk':<15} {disk_percent:>9.1f}%")
print(f"{'Requests':<15} {num_requests:>10,}")
```

**Expected Output:**
```
Server: app-server-03
Uptime: 720 hours
Uptime: 30.0 days
CPU Usage: 67.8%
Memory Usage: 82.3%
Disk Usage: 45.9%
Total Requests: 1,250,000

--- Formatted Report ---
Metric              Value
-------------------------
CPU                  67.8%
Memory               82.3%
Disk                 45.9%
Requests         1,250,000
```

### Exercise 4.2: Multi-line Strings for Configuration

```python
server_name = "db-server-01"
ip_address = "10.0.1.50"
port = 5432
database = "production"

# Multi-line f-string
config_output = f"""
Database Server Configuration
==============================
Server Name: {server_name}
IP Address:  {ip_address}
Port:        {port}
Database:    {database}
Status:      {'Active' if True else 'Inactive'}
==============================
"""

print(config_output)

# Expression in f-strings
total_connections = 150
max_connections = 200
connection_percent = (total_connections / max_connections) * 100

print(f"Connections: {total_connections}/{max_connections} ({connection_percent:.1f}%)")
print(f"Available: {max_connections - total_connections} connections")
print(f"Status: {'WARNING' if connection_percent > 80 else 'OK'}")
```

**Expected Output:**
```
Database Server Configuration
==============================
Server Name: db-server-01
IP Address:  10.0.1.50
Port:        5432
Database:    production
Status:      Active
==============================

Connections: 150/200 (75.0%)
Available: 50 connections
Status: OK
```

---

## Part 5: Practice Challenges

### Challenge 1: Environment Variable Parser

Create a script that simulates parsing environment variables:

```python
# Environment variable string (KEY=VALUE format)
env_var = "DATABASE_URL=postgresql://localhost:5432/mydb"

# Your task: Extract the key and value
# Extract the protocol, host, port, and database name
# Print formatted output

# HINT: Use split(), indexing, and f-strings
```

**Expected Output:**
```
Key: DATABASE_URL
Value: postgresql://localhost:5432/mydb
Protocol: postgresql
Host: localhost
Port: 5432
Database: mydb
```

<details>
<summary>Solution</summary>

```python
env_var = "DATABASE_URL=postgresql://localhost:5432/mydb"

# Split key and value
key, value = env_var.split('=')
print(f"Key: {key}")
print(f"Value: {value}")

# Parse the URL
# Remove protocol
protocol, rest = value.split('://')
print(f"Protocol: {protocol}")

# Split host:port/database
host_port, database = rest.split('/')
host, port = host_port.split(':')

print(f"Host: {host}")
print(f"Port: {port}")
print(f"Database: {database}")
```
</details>

### Challenge 2: Server Status Dashboard

Create a script that displays a server status dashboard:

```python
# Server data
servers = [
    ("web-01", 45.2, 67.8, True),
    ("web-02", 78.9, 82.1, True),
    ("db-01", 92.3, 88.5, False),
]

# Your task: Create a formatted dashboard showing:
# - Server name (left-aligned, 10 chars)
# - CPU usage (right-aligned, 6 chars, 1 decimal)
# - Memory usage (right-aligned, 6 chars, 1 decimal)
# - Status (OK if active and CPU < 90, WARNING otherwise)
```

**Expected Output:**
```
SERVER STATUS DASHBOARD
==================================================
Server     CPU%   Memory%  Status
--------------------------------------------------
web-01     45.2    67.8    OK
web-02     78.9    82.1    OK
db-01      92.3    88.5    WARNING
==================================================
```

<details>
<summary>Solution</summary>

```python
servers = [
    ("web-01", 45.2, 67.8, True),
    ("web-02", 78.9, 82.1, True),
    ("db-01", 92.3, 88.5, False),
]

print("SERVER STATUS DASHBOARD")
print("=" * 50)
print(f"{'Server':<10} {'CPU%':>6} {'Memory%':>8}  {'Status'}")
print("-" * 50)

for server_name, cpu, memory, is_active in servers:
    status = "OK" if is_active and cpu < 90 else "WARNING"
    print(f"{server_name:<10} {cpu:>6.1f} {memory:>8.1f}  {status}")

print("=" * 50)
```
</details>

### Challenge 3: Uptime Calculator

Create a script that converts uptime seconds to a readable format:

```python
# Uptime in seconds
uptime_seconds = 2592000  # 30 days

# Your task: Convert to days, hours, minutes, seconds
# Display in format: "30d 0h 0m 0s"
# Also calculate if uptime > 30 days (needs reboot)
```

**Expected Output:**
```
Uptime: 30d 0h 0m 0s
Reboot Recommended: False
```

<details>
<summary>Solution</summary>

```python
uptime_seconds = 2592000

# Calculate time components
seconds_per_minute = 60
seconds_per_hour = 60 * 60
seconds_per_day = 24 * 60 * 60

days = uptime_seconds // seconds_per_day
remaining = uptime_seconds % seconds_per_day

hours = remaining // seconds_per_hour
remaining = remaining % seconds_per_hour

minutes = remaining // seconds_per_minute
seconds = remaining % seconds_per_minute

print(f"Uptime: {days}d {hours}h {minutes}m {seconds}s")
print(f"Reboot Recommended: {days > 30}")
```
</details>

---

## Part 6: Real-World Scenario

### Scenario: Container Name Generator

You're managing a Kubernetes cluster and need to generate standardized container names.

Create `container_name_generator.py`:

```python
# Container configuration
app_name = "payment-api"
environment = "production"
version = "1.2.3"
instance_number = 5

# Generate container name: app-env-version-instance
# Example: payment-api-production-v1-2-3-05

# Convert version dots to dashes
version_formatted = version.replace('.', '-')

# Pad instance number with zeros
instance_padded = str(instance_number).zfill(2)

# Generate full name
container_name = f"{app_name}-{environment}-v{version_formatted}-{instance_padded}"

print(f"Container Name: {container_name}")
print(f"Length: {len(container_name)} characters")
print(f"Valid (lowercase, dashes only): {container_name.replace('-', '').isalnum()}")

# Extract information back from name
parts = container_name.split('-')
extracted_app = parts[0]
extracted_env = parts[1]
print(f"\nExtracted App: {extracted_app}")
print(f"Extracted Environment: {extracted_env}")

# Generate multiple instances
print("\nAll instances:")
for i in range(1, 6):
    name = f"{app_name}-{environment}-v{version_formatted}-{str(i).zfill(2)}"
    print(f"  {name}")
```

**Expected Output:**
```
Container Name: payment-api-production-v1-2-3-05
Length: 33 characters
Valid (lowercase, dashes only): True

Extracted App: payment
Extracted Environment: production

All instances:
  payment-api-production-v1-2-3-01
  payment-api-production-v1-2-3-02
  payment-api-production-v1-2-3-03
  payment-api-production-v1-2-3-04
  payment-api-production-v1-2-3-05
```

---

## What You Learned

In this lab, you learned:

✅ **Variables and Data Types**
- Declaring variables with descriptive names
- Working with strings, integers, floats, and booleans
- Type conversion for data processing

✅ **Operators**
- Arithmetic operators for calculations
- Comparison operators for threshold checking
- Logical operators for complex conditions

✅ **String Manipulation**
- String methods (strip, split, replace, startswith, endswith)
- String indexing and slicing
- String validation and checking

✅ **F-Strings and Formatting**
- Modern string formatting with f-strings
- Number formatting (decimals, percentages, separators)
- Aligned output for reports
- Multi-line strings for configuration

✅ **DevOps Applications**
- Server configuration management
- Resource calculation and monitoring
- Log processing and parsing
- Generating standardized naming conventions

---

## Next Steps

- Move on to **LAB-02: Data Structures** to learn about lists, dictionaries, and more
- Practice creating more complex server monitoring scripts
- Experiment with parsing real log files from `/var/log`

## Additional Resources

- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [Python String Formatting](https://docs.python.org/3/tutorial/inputoutput.html)
- [Python Operators](https://docs.python.org/3/library/operator.html)
