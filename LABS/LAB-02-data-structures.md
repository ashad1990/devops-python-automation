# LAB 02: Data Structures for DevOps

## Learning Objectives
By the end of this lab, you will be able to:
- Create and manipulate lists for managing collections of servers and services
- Use dictionaries to represent configuration data and metadata
- Work with tuples for immutable data like coordinates and credentials
- Utilize sets for unique collections and set operations
- Apply list and dictionary comprehensions for efficient data processing
- Choose the appropriate data structure for DevOps tasks

## Prerequisites
- Completed LAB-01: Python Basics
- Understanding of variables and operators

---

## Part 1: Lists - Managing Server Collections

### Exercise 1.1: Basic List Operations

Create `server_list.py`:

```python
# List of server names
servers = ["web-01", "web-02", "db-01", "cache-01"]

print(f"Servers: {servers}")
print(f"Total servers: {len(servers)}")
print(f"First server: {servers[0]}")
print(f"Last server: {servers[-1]}")

# Add a new server
servers.append("api-01")
print(f"After adding api-01: {servers}")

# Add multiple servers
servers.extend(["worker-01", "worker-02"])
print(f"After extending: {servers}")

# Insert at specific position
servers.insert(2, "lb-01")
print(f"After inserting lb-01 at index 2: {servers}")

# Remove a server
servers.remove("cache-01")
print(f"After removing cache-01: {servers}")

# Remove by index
removed = servers.pop(0)
print(f"Removed {removed}, remaining: {servers}")

# Check if server exists
print(f"Is 'db-01' in list: {'db-01' in servers}")
print(f"Is 'cache-01' in list: {'cache-01' in servers}")
```

**Expected Output:**
```
Servers: ['web-01', 'web-02', 'db-01', 'cache-01']
Total servers: 4
First server: web-01
Last server: cache-01
After adding api-01: ['web-01', 'web-02', 'db-01', 'cache-01', 'api-01']
After extending: ['web-01', 'web-02', 'db-01', 'cache-01', 'api-01', 'worker-01', 'worker-02']
After inserting lb-01 at index 2: ['web-01', 'web-02', 'lb-01', 'db-01', 'cache-01', 'api-01', 'worker-01', 'worker-02']
After removing cache-01: ['web-01', 'web-02', 'lb-01', 'db-01', 'api-01', 'worker-01', 'worker-02']
Removed web-01, remaining: ['web-02', 'lb-01', 'db-01', 'api-01', 'worker-01', 'worker-02']
Is 'db-01' in list: True
Is 'cache-01' in list: False
```

### Exercise 1.2: List Slicing and Sorting

```python
# Port numbers for different services
ports = [8080, 3306, 6379, 5432, 27017, 9200, 5672, 8000]

print(f"All ports: {ports}")

# Slicing
first_three = ports[:3]
last_two = ports[-2:]
middle_ports = ports[2:5]

print(f"First three: {first_three}")
print(f"Last two: {last_two}")
print(f"Middle (index 2-4): {middle_ports}")

# Sorting
sorted_ports = sorted(ports)
print(f"Sorted ascending: {sorted_ports}")

sorted_desc = sorted(ports, reverse=True)
print(f"Sorted descending: {sorted_desc}")

# In-place sorting
ports.sort()
print(f"Sorted in-place: {ports}")

# Reverse list
ports.reverse()
print(f"Reversed: {ports}")

# Find min and max
print(f"Lowest port: {min(ports)}")
print(f"Highest port: {max(ports)}")
print(f"Sum of ports: {sum(ports)}")
```

**Expected Output:**
```
All ports: [8080, 3306, 6379, 5432, 27017, 9200, 5672, 8000]
First three: [8080, 3306, 6379]
Last two: [5672, 8000]
Middle (index 2-4): [6379, 5432, 27017]
Sorted ascending: [3306, 5432, 5672, 6379, 8000, 8080, 9200, 27017]
Sorted descending: [27017, 9200, 8080, 8000, 6379, 5672, 5432, 3306]
Sorted in-place: [3306, 5432, 5672, 6379, 8000, 8080, 9200, 27017]
Reversed: [27017, 9200, 8080, 8000, 6379, 5672, 5432, 3306]
Lowest port: 3306
Highest port: 27017
Sum of ports: 57866
```

### Exercise 1.3: Nested Lists for Multi-Server Data

```python
# Server data: [name, cpu%, memory%, status]
servers_data = [
    ["web-01", 45.2, 67.8, "active"],
    ["web-02", 78.9, 82.1, "active"],
    ["db-01", 62.3, 88.5, "active"],
    ["api-01", 34.1, 45.2, "inactive"]
]

print("Server Status Report:")
print("-" * 50)

for server in servers_data:
    name, cpu, memory, status = server
    print(f"{name:<10} CPU: {cpu:>5.1f}% | Memory: {memory:>5.1f}% | {status}")

# Find servers with high CPU
high_cpu_servers = []
for server in servers_data:
    if server[1] > 60:
        high_cpu_servers.append(server[0])

print(f"\nHigh CPU servers (>60%): {high_cpu_servers}")

# Calculate average CPU usage
total_cpu = sum(server[1] for server in servers_data)
avg_cpu = total_cpu / len(servers_data)
print(f"Average CPU usage: {avg_cpu:.1f}%")
```

**Expected Output:**
```
Server Status Report:
--------------------------------------------------
web-01     CPU:  45.2% | Memory:  67.8% | active
web-02     CPU:  78.9% | Memory:  82.1% | active
db-01      CPU:  62.3% | Memory:  88.5% | active
api-01     CPU:  34.1% | Memory:  45.2% | inactive

High CPU servers (>60%): ['web-02', 'db-01']
Average CPU usage: 55.1%
```

---

## Part 2: Dictionaries - Configuration Management

### Exercise 2.1: Basic Dictionary Operations

Create `server_config.py`:

```python
# Server configuration dictionary
server = {
    "name": "web-prod-01",
    "ip": "10.0.1.50",
    "port": 8080,
    "environment": "production",
    "active": True,
    "tags": ["web", "frontend", "nginx"]
}

print(f"Server config: {server}")
print(f"Server name: {server['name']}")
print(f"Server IP: {server['ip']}")

# Add new key
server["region"] = "us-east-1"
print(f"After adding region: {server}")

# Update existing key
server["port"] = 8443
print(f"After updating port: {server}")

# Safe get with default
memory = server.get("memory", "Not specified")
print(f"Memory: {memory}")

# Check if key exists
print(f"Has 'ip' key: {'ip' in server}")
print(f"Has 'memory' key: {'memory' in server}")

# Get all keys, values, items
print(f"\nKeys: {list(server.keys())}")
print(f"Values: {list(server.values())}")

# Iterate over items
print("\nAll configuration:")
for key, value in server.items():
    print(f"  {key}: {value}")
```

**Expected Output:**
```
Server config: {'name': 'web-prod-01', 'ip': '10.0.1.50', 'port': 8080, 'environment': 'production', 'active': True, 'tags': ['web', 'frontend', 'nginx']}
Server name: web-prod-01
Server IP: 10.0.1.50
After adding region: {'name': 'web-prod-01', 'ip': '10.0.1.50', 'port': 8080, 'environment': 'production', 'active': True, 'tags': ['web', 'frontend', 'nginx'], 'region': 'us-east-1'}
After updating port: {'name': 'web-prod-01', 'ip': '10.0.1.50', 'port': 8443, 'environment': 'production', 'active': True, 'tags': ['web', 'frontend', 'nginx'], 'region': 'us-east-1'}
Memory: Not specified
Has 'ip' key: True
Has 'memory' key: False

Keys: ['name', 'ip', 'port', 'environment', 'active', 'tags', 'region']
Values: ['web-prod-01', '10.0.1.50', 8443, 'production', True, ['web', 'frontend', 'nginx'], 'us-east-1']

All configuration:
  name: web-prod-01
  ip: 10.0.1.50
  port: 8443
  environment: production
  active: True
  tags: ['web', 'frontend', 'nginx']
  region: us-east-1
```

### Exercise 2.2: Nested Dictionaries for Infrastructure

```python
# Infrastructure configuration
infrastructure = {
    "web_servers": {
        "count": 3,
        "instance_type": "t3.medium",
        "ports": [80, 443]
    },
    "databases": {
        "count": 2,
        "instance_type": "r5.large",
        "ports": [5432]
    },
    "cache": {
        "count": 1,
        "instance_type": "r5.xlarge",
        "ports": [6379]
    }
}

# Access nested data
print(f"Web server count: {infrastructure['web_servers']['count']}")
print(f"Web server type: {infrastructure['web_servers']['instance_type']}")
print(f"Database ports: {infrastructure['databases']['ports']}")

# Iterate through infrastructure
print("\nInfrastructure Summary:")
for service, config in infrastructure.items():
    print(f"{service}:")
    print(f"  Count: {config['count']}")
    print(f"  Type: {config['instance_type']}")
    print(f"  Ports: {config['ports']}")

# Calculate total instances
total_instances = sum(config['count'] for config in infrastructure.values())
print(f"\nTotal instances: {total_instances}")

# Update nested value
infrastructure['web_servers']['count'] = 5
print(f"Updated web server count: {infrastructure['web_servers']['count']}")
```

**Expected Output:**
```
Web server count: 3
Web server type: t3.medium
Database ports: [5432]

Infrastructure Summary:
web_servers:
  Count: 3
  Type: t3.medium
  Ports: [80, 443]
databases:
  Count: 2
  Type: r5.large
  Ports: [5432]
cache:
  Count: 1
  Type: r5.xlarge
  Ports: [6379]

Total instances: 6
Updated web server count: 5
```

### Exercise 2.3: Dictionary Methods for Merging Configs

```python
# Default configuration
default_config = {
    "timeout": 30,
    "retries": 3,
    "log_level": "INFO",
    "ssl_verify": True
}

# User configuration (overrides)
user_config = {
    "timeout": 60,
    "log_level": "DEBUG"
}

# Merge configurations (user overrides default)
final_config = default_config.copy()
final_config.update(user_config)

print("Default config:", default_config)
print("User config:", user_config)
print("Final config:", final_config)

# Using dict unpacking (Python 3.5+)
merged = {**default_config, **user_config}
print("Merged with unpacking:", merged)

# Remove a key
if "retries" in final_config:
    removed_value = final_config.pop("retries")
    print(f"\nRemoved 'retries': {removed_value}")
    print(f"Config after removal: {final_config}")

# Clear all
test_dict = {"a": 1, "b": 2}
test_dict.clear()
print(f"After clear: {test_dict}")
```

**Expected Output:**
```
Default config: {'timeout': 30, 'retries': 3, 'log_level': 'INFO', 'ssl_verify': True}
User config: {'timeout': 60, 'log_level': 'DEBUG'}
Final config: {'timeout': 60, 'retries': 3, 'log_level': 'DEBUG', 'ssl_verify': True}
Merged with unpacking: {'timeout': 60, 'retries': 3, 'log_level': 'INFO', 'ssl_verify': True, 'log_level': 'DEBUG'}

Removed 'retries': 3
Config after removal: {'timeout': 60, 'log_level': 'DEBUG', 'ssl_verify': True}
After clear: {}
```

---

## Part 3: Tuples - Immutable Data

### Exercise 3.1: Basic Tuple Operations

Create `server_tuples.py`:

```python
# Server coordinate (name, x, y)
server_location = ("web-01", 40.7128, -74.0060)

print(f"Server location: {server_location}")
print(f"Server name: {server_location[0]}")
print(f"Latitude: {server_location[1]}")
print(f"Longitude: {server_location[2]}")

# Unpacking
name, lat, lon = server_location
print(f"\nUnpacked - Name: {name}, Lat: {lat}, Lon: {lon}")

# Tuple length
print(f"Tuple length: {len(server_location)}")

# Count and index
numbers = (1, 2, 3, 2, 4, 2, 5)
print(f"\nCount of 2: {numbers.count(2)}")
print(f"First index of 2: {numbers.index(2)}")

# Tuples are immutable - this would raise an error:
# server_location[0] = "web-02"  # TypeError

# Multiple return values (common in functions)
def get_server_status():
    return "web-01", "active", 45.2, 67.8

server_name, status, cpu, memory = get_server_status()
print(f"\nServer: {server_name}")
print(f"Status: {status}")
print(f"CPU: {cpu}%, Memory: {memory}%")
```

**Expected Output:**
```
Server location: ('web-01', 40.7128, -74.006)
Server name: web-01
Latitude: 40.7128
Longitude: -74.006

Unpacked - Name: web-01, Lat: 40.7128, Lon: -74.006
Tuple length: 3

Count of 2: 3
First index of 2: 1

Server: web-01
Status: active
CPU: 45.2%, Memory: 67.8%
```

### Exercise 3.2: Tuples in Lists (Database Records)

```python
# List of tuples - server records
servers = [
    ("web-01", "10.0.1.10", 8080, "active"),
    ("web-02", "10.0.1.11", 8080, "active"),
    ("db-01", "10.0.2.10", 5432, "active"),
    ("cache-01", "10.0.3.10", 6379, "inactive")
]

print("Server Inventory:")
print(f"{'Name':<12} {'IP':<15} {'Port':<6} {'Status'}")
print("-" * 50)

for name, ip, port, status in servers:
    print(f"{name:<12} {ip:<15} {port:<6} {status}")

# Filter active servers
active_servers = [s for s in servers if s[3] == "active"]
print(f"\nActive servers: {len(active_servers)}")

# Sort by port
sorted_by_port = sorted(servers, key=lambda x: x[2])
print("\nSorted by port:")
for server in sorted_by_port:
    print(f"  {server[0]}: {server[2]}")
```

**Expected Output:**
```
Server Inventory:
Name         IP              Port   Status
--------------------------------------------------
web-01       10.0.1.10       8080   active
web-02       10.0.1.11       8080   active
db-01        10.0.2.10       5432   active
cache-01     10.0.3.10       6379   inactive

Active servers: 3

Sorted by port:
  db-01: 5432
  cache-01: 6379
  web-01: 8080
  web-02: 8080
```

---

## Part 4: Sets - Unique Collections

### Exercise 4.1: Basic Set Operations

Create `server_sets.py`:

```python
# Sets automatically remove duplicates
deployed_apps = {"nginx", "nodejs", "redis", "nginx", "postgresql", "nodejs"}

print(f"Deployed apps (unique): {deployed_apps}")
print(f"Number of unique apps: {len(deployed_apps)}")

# Add to set
deployed_apps.add("mongodb")
print(f"After adding mongodb: {deployed_apps}")

# Remove from set
deployed_apps.remove("redis")
print(f"After removing redis: {deployed_apps}")

# Safe remove (doesn't error if not present)
deployed_apps.discard("redis")  # No error even though redis is already removed
deployed_apps.discard("mysql")  # No error

# Check membership
print(f"\nIs nginx deployed: {'nginx' in deployed_apps}")
print(f"Is apache deployed: {'apache' in deployed_apps}")

# Clear set
test_set = {1, 2, 3}
test_set.clear()
print(f"Cleared set: {test_set}")
```

**Expected Output:**
```
Deployed apps (unique): {'postgresql', 'redis', 'nodejs', 'nginx'}
Number of unique apps: 4
After adding mongodb: {'postgresql', 'mongodb', 'redis', 'nodejs', 'nginx'}
After removing redis: {'postgresql', 'mongodb', 'nodejs', 'nginx'}

Is nginx deployed: True
Is apache deployed: False
Cleared set: set()
```

### Exercise 4.2: Set Operations for Server Management

```python
# Servers in different data centers
dc1_servers = {"web-01", "web-02", "db-01", "cache-01"}
dc2_servers = {"web-03", "db-01", "cache-01", "api-01"}

print(f"DC1 servers: {dc1_servers}")
print(f"DC2 servers: {dc2_servers}")

# Union - all servers across both DCs
all_servers = dc1_servers | dc2_servers
# Or: all_servers = dc1_servers.union(dc2_servers)
print(f"\nAll servers (union): {all_servers}")

# Intersection - servers in both DCs (replicated)
replicated = dc1_servers & dc2_servers
# Or: replicated = dc1_servers.intersection(dc2_servers)
print(f"Replicated servers (intersection): {replicated}")

# Difference - servers only in DC1
dc1_only = dc1_servers - dc2_servers
# Or: dc1_only = dc1_servers.difference(dc2_servers)
print(f"DC1 only servers (difference): {dc1_only}")

# Symmetric difference - servers in one DC but not both
unique_servers = dc1_servers ^ dc2_servers
# Or: unique_servers = dc1_servers.symmetric_difference(dc2_servers)
print(f"Unique to one DC (symmetric difference): {unique_servers}")

# Check subset/superset
subset = {"web-01", "db-01"}
print(f"\n{subset} is subset of DC1: {subset.issubset(dc1_servers)}")
print(f"DC1 is superset of {subset}: {dc1_servers.issuperset(subset)}")
```

**Expected Output:**
```
DC1 servers: {'web-02', 'cache-01', 'db-01', 'web-01'}
DC2 servers: {'cache-01', 'web-03', 'db-01', 'api-01'}

All servers (union): {'web-02', 'cache-01', 'web-03', 'db-01', 'api-01', 'web-01'}
Replicated servers (intersection): {'cache-01', 'db-01'}
DC1 only servers (difference): {'web-02', 'web-01'}
Unique to one DC (symmetric difference): {'web-02', 'web-03', 'api-01', 'web-01'}

{'web-01', 'db-01'} is subset of DC1: True
DC1 is superset of {'web-01', 'db-01'}: True
```

---

## Part 5: Comprehensions - Efficient Data Processing

### Exercise 5.1: List Comprehensions

Create `comprehensions.py`:

```python
# Traditional way
servers = ["web-01", "web-02", "db-01", "cache-01", "api-01"]
uppercase_servers = []
for server in servers:
    uppercase_servers.append(server.upper())
print(f"Traditional: {uppercase_servers}")

# List comprehension
uppercase_servers = [server.upper() for server in servers]
print(f"Comprehension: {uppercase_servers}")

# With condition - filter web servers
web_servers = [s for s in servers if s.startswith("web")]
print(f"Web servers: {web_servers}")

# Transform and filter
ports = [80, 443, 8080, 22, 3306, 5432, 8000]
high_ports = [p for p in ports if p >= 1024]
print(f"High ports (>=1024): {high_ports}")

# With expression
port_labels = [f"Port {p} ({'secure' if p == 443 else 'standard'})" for p in [80, 443, 8080]]
print(f"Port labels: {port_labels}")

# Nested comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"Flattened: {flattened}")
```

**Expected Output:**
```
Traditional: ['WEB-01', 'WEB-02', 'DB-01', 'CACHE-01', 'API-01']
Comprehension: ['WEB-01', 'WEB-02', 'DB-01', 'CACHE-01', 'API-01']
Web servers: ['web-01', 'web-02']
High ports (>=1024): [8080, 3306, 5432, 8000]
Port labels: ['Port 80 (standard)', 'Port 443 (secure)', 'Port 8080 (standard)']
Flattened: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Exercise 5.2: Dictionary Comprehensions

```python
# Create dictionary from lists
servers = ["web-01", "web-02", "db-01"]
ips = ["10.0.1.10", "10.0.1.11", "10.0.2.10"]

# Traditional way
server_ips = {}
for i in range(len(servers)):
    server_ips[servers[i]] = ips[i]
print(f"Traditional: {server_ips}")

# Dictionary comprehension using zip
server_ips = {server: ip for server, ip in zip(servers, ips)}
print(f"Comprehension: {server_ips}")

# Transform keys and values
metrics = {"cpu": 45.5, "memory": 67.8, "disk": 34.2}
metrics_percent = {k.upper(): f"{v:.1f}%" for k, v in metrics.items()}
print(f"Metrics as %: {metrics_percent}")

# Filter dictionary
server_metrics = {
    "web-01": 45.2,
    "web-02": 78.9,
    "db-01": 92.3,
    "api-01": 34.1
}
high_cpu = {k: v for k, v in server_metrics.items() if v > 60}
print(f"High CPU servers: {high_cpu}")

# Invert dictionary (swap keys and values)
inverted = {v: k for k, v in server_ips.items()}
print(f"Inverted IPs: {inverted}")
```

**Expected Output:**
```
Traditional: {'web-01': '10.0.1.10', 'web-02': '10.0.1.11', 'db-01': '10.0.2.10'}
Comprehension: {'web-01': '10.0.1.10', 'web-02': '10.0.1.11', 'db-01': '10.0.2.10'}
Metrics as %: {'CPU': '45.5%', 'MEMORY': '67.8%', 'DISK': '34.2%'}
High CPU servers: {'web-02': 78.9, 'db-01': 92.3}
Inverted IPs: {'10.0.1.10': 'web-01', '10.0.1.11': 'web-02', '10.0.2.10': 'db-01'}
```

### Exercise 5.3: Set Comprehensions

```python
# Extract unique domains from URLs
urls = [
    "http://api.example.com/v1/users",
    "http://api.example.com/v1/posts",
    "http://web.example.com/home",
    "http://api.test.com/health",
    "http://web.example.com/about"
]

# Extract unique domains
domains = {url.split('/')[2] for url in urls}
print(f"Unique domains: {domains}")

# Unique ports from server list
servers = [
    {"name": "web-01", "port": 8080},
    {"name": "web-02", "port": 8080},
    {"name": "db-01", "port": 5432},
    {"name": "api-01", "port": 8080}
]

unique_ports = {s["port"] for s in servers}
print(f"Unique ports: {unique_ports}")

# Find unique file extensions
files = ["app.py", "config.yaml", "main.py", "data.json", "test.py", "settings.yaml"]
extensions = {f.split('.')[-1] for f in files}
print(f"Unique extensions: {extensions}")
```

**Expected Output:**
```
Unique domains: {'api.test.com', 'web.example.com', 'api.example.com'}
Unique ports: {8080, 5432}
Unique extensions: {'yaml', 'py', 'json'}
```

---

## Part 6: Practice Challenges

### Challenge 1: Server Inventory Manager

Create a script that manages server inventory using a dictionary:

```python
# Your task: Create a server inventory system
# 1. Create a dictionary with server names as keys
# 2. Each server should have: ip, status, cpu%, memory%
# 3. Add a function to add new servers
# 4. Add a function to update server metrics
# 5. Add a function to list all active servers
# 6. Add a function to get servers with high CPU (>80%)

# Expected operations:
# - Add server: web-01, 10.0.1.10, active, 45.2, 67.8
# - Update metrics: web-01, cpu=85.3
# - List active servers
# - Get high CPU servers
```

<details>
<summary>Solution</summary>

```python
inventory = {}

def add_server(name, ip, status, cpu, memory):
    inventory[name] = {
        "ip": ip,
        "status": status,
        "cpu": cpu,
        "memory": memory
    }
    print(f"Added server: {name}")

def update_metrics(name, cpu=None, memory=None):
    if name in inventory:
        if cpu is not None:
            inventory[name]["cpu"] = cpu
        if memory is not None:
            inventory[name]["memory"] = memory
        print(f"Updated {name}")
    else:
        print(f"Server {name} not found")

def list_active_servers():
    active = [name for name, data in inventory.items() if data["status"] == "active"]
    return active

def get_high_cpu_servers(threshold=80):
    high_cpu = {name: data["cpu"] for name, data in inventory.items() if data["cpu"] > threshold}
    return high_cpu

# Test
add_server("web-01", "10.0.1.10", "active", 45.2, 67.8)
add_server("web-02", "10.0.1.11", "active", 85.3, 72.1)
add_server("db-01", "10.0.2.10", "inactive", 92.1, 88.5)

update_metrics("web-01", cpu=88.5)

print(f"Active servers: {list_active_servers()}")
print(f"High CPU servers: {get_high_cpu_servers()}")
```
</details>

### Challenge 2: Log Parser with Data Structures

Parse Apache access log lines and extract statistics:

```python
# Sample log lines
logs = [
    '192.168.1.1 - - [15/Jan/2024:10:15:30] "GET /api/users HTTP/1.1" 200 1234',
    '192.168.1.2 - - [15/Jan/2024:10:16:45] "GET /api/posts HTTP/1.1" 200 5678',
    '192.168.1.1 - - [15/Jan/2024:10:17:22] "POST /api/users HTTP/1.1" 201 432',
    '192.168.1.3 - - [15/Jan/2024:10:18:10] "GET /api/users HTTP/1.1" 404 98',
    '192.168.1.2 - - [15/Jan/2024:10:19:05] "GET /api/posts HTTP/1.1" 500 156'
]

# Your task:
# 1. Extract unique IP addresses (set)
# 2. Count requests per IP (dictionary)
# 3. Count status codes (dictionary)
# 4. List all endpoints (set)
# 5. Calculate total bytes transferred
```

<details>
<summary>Solution</summary>

```python
logs = [
    '192.168.1.1 - - [15/Jan/2024:10:15:30] "GET /api/users HTTP/1.1" 200 1234',
    '192.168.1.2 - - [15/Jan/2024:10:16:45] "GET /api/posts HTTP/1.1" 200 5678',
    '192.168.1.1 - - [15/Jan/2024:10:17:22] "POST /api/users HTTP/1.1" 201 432',
    '192.168.1.3 - - [15/Jan/2024:10:18:10] "GET /api/users HTTP/1.1" 404 98',
    '192.168.1.2 - - [15/Jan/2024:10:19:05] "GET /api/posts HTTP/1.1" 500 156'
]

# Extract unique IPs
unique_ips = {log.split()[0] for log in logs}
print(f"Unique IPs: {unique_ips}")

# Count requests per IP
ip_counts = {}
for log in logs:
    ip = log.split()[0]
    ip_counts[ip] = ip_counts.get(ip, 0) + 1
print(f"Requests per IP: {ip_counts}")

# Count status codes
status_counts = {}
for log in logs:
    parts = log.split()
    status = parts[-2]
    status_counts[status] = status_counts.get(status, 0) + 1
print(f"Status codes: {status_counts}")

# Extract endpoints
endpoints = {log.split('"')[1].split()[1] for log in logs}
print(f"Endpoints: {endpoints}")

# Total bytes
total_bytes = sum(int(log.split()[-1]) for log in logs)
print(f"Total bytes: {total_bytes}")
```
</details>

### Challenge 3: Configuration Merger

Merge multiple configuration dictionaries with priority:

```python
# Your task: Merge these configs with priority (base < env < user)
base_config = {
    "app_name": "myapp",
    "port": 8080,
    "debug": False,
    "max_connections": 100,
    "timeout": 30
}

env_config = {
    "debug": True,
    "port": 8000
}

user_config = {
    "max_connections": 200
}

# Create final_config that merges all three
# Priority: user_config > env_config > base_config
```

<details>
<summary>Solution</summary>

```python
base_config = {
    "app_name": "myapp",
    "port": 8080,
    "debug": False,
    "max_connections": 100,
    "timeout": 30
}

env_config = {
    "debug": True,
    "port": 8000
}

user_config = {
    "max_connections": 200
}

# Method 1: Using update
final_config = base_config.copy()
final_config.update(env_config)
final_config.update(user_config)

print("Final config (Method 1):")
for key, value in final_config.items():
    print(f"  {key}: {value}")

# Method 2: Using dict unpacking
final_config = {**base_config, **env_config, **user_config}

print("\nFinal config (Method 2):")
for key, value in final_config.items():
    print(f"  {key}: {value}")
```
</details>

---

## Part 7: Real-World Scenario

### Scenario: Multi-Cloud Server Inventory

Create `cloud_inventory.py`:

```python
# Multi-cloud server inventory
servers = [
    {"name": "web-01", "cloud": "aws", "region": "us-east-1", "cpu": 45.2, "cost": 120},
    {"name": "web-02", "cloud": "aws", "region": "us-west-2", "cpu": 67.8, "cost": 120},
    {"name": "db-01", "cloud": "azure", "region": "eastus", "cpu": 82.3, "cost": 450},
    {"name": "cache-01", "cloud": "gcp", "region": "us-central1", "cpu": 34.5, "cost": 80},
    {"name": "api-01", "cloud": "aws", "region": "us-east-1", "cpu": 91.2, "cost": 200},
]

# 1. Group servers by cloud provider
by_cloud = {}
for server in servers:
    cloud = server["cloud"]
    if cloud not in by_cloud:
        by_cloud[cloud] = []
    by_cloud[cloud].append(server["name"])

print("Servers by cloud:")
for cloud, server_list in by_cloud.items():
    print(f"  {cloud}: {server_list}")

# 2. Calculate total cost per cloud
cost_by_cloud = {}
for server in servers:
    cloud = server["cloud"]
    cost_by_cloud[cloud] = cost_by_cloud.get(cloud, 0) + server["cost"]

print("\nTotal cost by cloud:")
for cloud, cost in cost_by_cloud.items():
    print(f"  {cloud}: ${cost}")

# 3. Find high CPU servers (>80%) with comprehension
high_cpu = [s["name"] for s in servers if s["cpu"] > 80]
print(f"\nHigh CPU servers: {high_cpu}")

# 4. Get unique regions
unique_regions = {s["region"] for s in servers}
print(f"Unique regions: {unique_regions}")

# 5. Create mapping of server names to cloud providers
server_to_cloud = {s["name"]: s["cloud"] for s in servers}
print(f"\nServer to cloud mapping:")
for server, cloud in server_to_cloud.items():
    print(f"  {server}: {cloud}")

# 6. Find most expensive server
most_expensive = max(servers, key=lambda s: s["cost"])
print(f"\nMost expensive server: {most_expensive['name']} (${most_expensive['cost']})")

# 7. Calculate average CPU usage
avg_cpu = sum(s["cpu"] for s in servers) / len(servers)
print(f"Average CPU usage: {avg_cpu:.1f}%")

# 8. Filter AWS servers in us-east-1
aws_east = [s for s in servers if s["cloud"] == "aws" and s["region"] == "us-east-1"]
print(f"\nAWS us-east-1 servers:")
for server in aws_east:
    print(f"  {server['name']}: CPU {server['cpu']}%")
```

**Expected Output:**
```
Servers by cloud:
  aws: ['web-01', 'web-02', 'api-01']
  azure: ['db-01']
  gcp: ['cache-01']

Total cost by cloud:
  aws: $440
  azure: $450
  gcp: $80

High CPU servers: ['db-01', 'api-01']
Unique regions: {'us-west-2', 'eastus', 'us-east-1', 'us-central1'}

Server to cloud mapping:
  web-01: aws
  web-02: aws
  db-01: azure
  cache-01: gcp
  api-01: aws

Most expensive server: db-01 ($450)
Average CPU usage: 64.2%

AWS us-east-1 servers:
  web-01: CPU 45.2%
  api-01: CPU 91.2%
```

---

## What You Learned

In this lab, you learned:

✅ **Lists**
- Creating and manipulating ordered collections
- List methods (append, extend, insert, remove, pop)
- Slicing, sorting, and reversing
- Working with nested lists

✅ **Dictionaries**
- Key-value pair storage for configuration
- Dictionary methods (get, keys, values, items, update)
- Nested dictionaries for complex data
- Merging configurations

✅ **Tuples**
- Immutable sequences for fixed data
- Tuple unpacking
- Using tuples as dictionary keys
- Multiple return values

✅ **Sets**
- Unique collections
- Set operations (union, intersection, difference)
- Removing duplicates
- Membership testing

✅ **Comprehensions**
- List comprehensions for transformation and filtering
- Dictionary comprehensions for key-value creation
- Set comprehensions for unique collections
- Nested comprehensions

✅ **DevOps Applications**
- Server inventory management
- Configuration merging
- Log parsing and analysis
- Multi-cloud resource tracking

---

## Next Steps

- Move on to **LAB-03: Control Flow** to add logic and loops
- Practice by creating a more complex inventory system
- Try parsing real configuration files (JSON, YAML)

## Additional Resources

- [Python Data Structures Documentation](https://docs.python.org/3/tutorial/datastructures.html)
- [List Comprehensions Guide](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Dictionary Methods](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
