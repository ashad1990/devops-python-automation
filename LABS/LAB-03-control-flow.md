# LAB 03: Control Flow for DevOps

## Learning Objectives
By the end of this lab, you will be able to:
- Use conditional statements (if/elif/else) for decision making
- Implement for loops to iterate over collections
- Use while loops for continuous operations
- Handle exceptions with try/except/finally blocks
- Apply control flow to real-world DevOps scenarios
- Implement error handling in automation scripts

## Prerequisites
- Completed LAB-01 and LAB-02
- Understanding of data structures (lists, dictionaries)

---

## Part 1: Conditional Statements (if/elif/else)

### Exercise 1.1: Basic Conditional Logic

Create `server_health_check.py`:

```python
# Server health metrics
cpu_usage = 85
memory_usage = 72
disk_usage = 95

# Simple if statement
if cpu_usage > 80:
    print("WARNING: High CPU usage detected!")

# if-else statement
if memory_usage > 90:
    print("CRITICAL: Memory critically low")
else:
    print("Memory usage is acceptable")

# if-elif-else statement
if disk_usage < 70:
    status = "OK"
elif disk_usage < 85:
    status = "WARNING"
else:
    status = "CRITICAL"

print(f"Disk status: {status} ({disk_usage}%)")

# Multiple conditions with and/or
if cpu_usage > 80 and memory_usage > 70:
    print("Server is under heavy load")

if disk_usage > 90 or cpu_usage > 90:
    print("ALERT: Immediate attention required")

# Nested conditions
if cpu_usage > 80:
    if memory_usage > 80:
        print("Both CPU and Memory are high - consider scaling")
    else:
        print("CPU is high but memory is OK")
```

**Expected Output:**
```
WARNING: High CPU usage detected!
Memory usage is acceptable
Disk status: CRITICAL (95%)
Server is under heavy load
ALERT: Immediate attention required
CPU is high but memory is OK
```

### Exercise 1.2: Ternary Operator and Conditional Expressions

```python
# Server configuration
environment = "production"
debug_mode = False
port = 8080

# Ternary operator (conditional expression)
log_level = "INFO" if environment == "production" else "DEBUG"
print(f"Log level: {log_level}")

# Multiple ternary conditions
server_status = "active" if port > 0 else "stopped"
print(f"Server status: {server_status}")

# Nested ternary (use sparingly - can be hard to read)
priority = "high" if environment == "production" else "medium" if environment == "staging" else "low"
print(f"Alert priority: {priority}")

# Using conditions in data structures
server_config = {
    "name": "web-server",
    "debug": debug_mode,
    "workers": 4 if environment == "production" else 2,
    "timeout": 60 if environment == "production" else 30
}

print(f"Server config: {server_config}")

# Conditional list building
services = ["nginx", "app"]
if environment == "production":
    services.extend(["monitoring", "logging"])

print(f"Services: {services}")
```

**Expected Output:**
```
Log level: INFO
Server status: active
Alert priority: high
Server config: {'name': 'web-server', 'debug': False, 'workers': 4, 'timeout': 60}
Services: ['nginx', 'app', 'monitoring', 'logging']
```

### Exercise 1.3: Checking Multiple Conditions

```python
# Deployment readiness checker
def check_deployment_ready(tests_pass, build_success, approval, environment):
    # Check all conditions
    if not tests_pass:
        return False, "Tests failed"
    
    if not build_success:
        return False, "Build failed"
    
    if not approval:
        return False, "Awaiting approval"
    
    if environment not in ["staging", "production"]:
        return False, "Invalid environment"
    
    return True, "Ready to deploy"

# Test different scenarios
scenarios = [
    (True, True, True, "production"),
    (False, True, True, "production"),
    (True, True, False, "production"),
    (True, True, True, "development")
]

for tests, build, approval, env in scenarios:
    ready, message = check_deployment_ready(tests, build, approval, env)
    status = "✓" if ready else "✗"
    print(f"{status} Environment: {env:12} - {message}")
```

**Expected Output:**
```
✓ Environment: production   - Ready to deploy
✗ Environment: production   - Tests failed
✗ Environment: production   - Awaiting approval
✗ Environment: development  - Invalid environment
```

---

## Part 2: For Loops - Iteration

### Exercise 2.1: Basic For Loops

Create `server_iteration.py`:

```python
# Iterate over a list
servers = ["web-01", "web-02", "db-01", "cache-01"]

print("Restarting servers:")
for server in servers:
    print(f"  Restarting {server}...")

# Iterate with index using enumerate
print("\nServer inventory:")
for index, server in enumerate(servers):
    print(f"  {index + 1}. {server}")

# Iterate with custom start index
print("\nServer IDs:")
for index, server in enumerate(servers, start=100):
    print(f"  ID {index}: {server}")

# Iterate over a range
print("\nPort scan:")
for port in range(8000, 8005):
    print(f"  Checking port {port}")

# Iterate with step
print("\nChecking every 100 ports:")
for port in range(1000, 2000, 100):
    print(f"  Port {port}")

# Reverse iteration
print("\nServers in reverse order:")
for server in reversed(servers):
    print(f"  {server}")
```

**Expected Output:**
```
Restarting servers:
  Restarting web-01...
  Restarting web-02...
  Restarting db-01...
  Restarting cache-01...

Server inventory:
  1. web-01
  2. web-02
  3. db-01
  4. cache-01

Server IDs:
  ID 100: web-01
  ID 101: web-02
  ID 102: db-01
  ID 103: cache-01

Port scan:
  Checking port 8000
  Checking port 8001
  Checking port 8002
  Checking port 8003
  Checking port 8004

Checking every 100 ports:
  Port 1000
  Port 1100
  Port 1200
  Port 1300
  Port 1400
  Port 1500
  Port 1600
  Port 1700
  Port 1800
  Port 1900

Servers in reverse order:
  cache-01
  db-01
  web-02
  web-01
```

### Exercise 2.2: Looping Through Dictionaries

```python
# Server metrics dictionary
server_metrics = {
    "web-01": {"cpu": 45.2, "memory": 67.8, "disk": 34.5},
    "web-02": {"cpu": 78.9, "memory": 82.1, "disk": 56.7},
    "db-01": {"cpu": 62.3, "memory": 88.5, "disk": 78.2}
}

# Iterate over keys
print("Server names:")
for server in server_metrics.keys():
    print(f"  {server}")

# Iterate over values
print("\nAll metrics:")
for metrics in server_metrics.values():
    print(f"  CPU: {metrics['cpu']}%, Memory: {metrics['memory']}%")

# Iterate over items (key-value pairs)
print("\nFull server report:")
for server, metrics in server_metrics.items():
    print(f"{server}:")
    print(f"  CPU: {metrics['cpu']}%")
    print(f"  Memory: {metrics['memory']}%")
    print(f"  Disk: {metrics['disk']}%")

# Nested dictionary iteration
print("\nDetailed metrics:")
for server, metrics in server_metrics.items():
    for metric_name, value in metrics.items():
        print(f"  {server} - {metric_name}: {value}%")
```

**Expected Output:**
```
Server names:
  web-01
  web-02
  db-01

All metrics:
  CPU: 45.2%, Memory: 67.8%
  CPU: 78.9%, Memory: 82.1%
  CPU: 62.3%, Memory: 88.5%

Full server report:
web-01:
  CPU: 45.2%
  Memory: 67.8%
  Disk: 34.5%
web-02:
  CPU: 78.9%
  Memory: 82.1%
  Disk: 56.7%
db-01:
  CPU: 62.3%
  Memory: 88.5%
  Disk: 78.2%

Detailed metrics:
  web-01 - cpu: 45.2%
  web-01 - memory: 67.8%
  web-01 - disk: 34.5%
  web-02 - cpu: 78.9%
  web-02 - memory: 82.1%
  web-02 - disk: 56.7%
  db-01 - cpu: 62.3%
  db-01 - memory: 88.5%
  db-01 - disk: 78.2%
```

### Exercise 2.3: Loop Control (break, continue, else)

```python
# Find first server with high CPU
servers = [
    ("web-01", 45.2),
    ("web-02", 78.9),
    ("db-01", 92.3),
    ("api-01", 34.1)
]

print("Finding first high CPU server (>80%):")
for name, cpu in servers:
    if cpu > 80:
        print(f"Found: {name} with {cpu}% CPU")
        break
else:
    print("No high CPU servers found")

# Skip inactive servers
server_states = [
    ("web-01", "active"),
    ("web-02", "inactive"),
    ("db-01", "active"),
    ("api-01", "inactive")
]

print("\nProcessing active servers only:")
for name, state in server_states:
    if state == "inactive":
        print(f"  Skipping {name} (inactive)")
        continue
    print(f"  Processing {name}")

# Using else with for loop (executes if loop completes without break)
print("\nSearching for server 'cache-01':")
search_name = "cache-01"
for name, state in server_states:
    if name == search_name:
        print(f"Found {search_name}")
        break
else:
    print(f"{search_name} not found in server list")

# Nested loops with break
print("\nFinding server in data center:")
data_centers = {
    "dc1": ["web-01", "web-02"],
    "dc2": ["db-01", "cache-01"],
    "dc3": ["api-01", "worker-01"]
}

search_server = "cache-01"
found = False

for dc, servers in data_centers.items():
    for server in servers:
        if server == search_server:
            print(f"Found {search_server} in {dc}")
            found = True
            break
    if found:
        break
```

**Expected Output:**
```
Finding first high CPU server (>80%):
Found: db-01 with 92.3% CPU

Processing active servers only:
  Processing web-01
  Skipping web-02 (inactive)
  Processing db-01
  Skipping api-01 (inactive)

Searching for server 'cache-01':
cache-01 not found in server list

Finding server in data center:
Found cache-01 in dc2
```

---

## Part 3: While Loops - Continuous Operations

### Exercise 3.1: Basic While Loops

Create `polling_operations.py`:

```python
# Simulate checking service status until it's ready
import time

# Simple while loop
attempts = 0
max_attempts = 5

print("Waiting for service to start...")
while attempts < max_attempts:
    attempts += 1
    print(f"  Attempt {attempts}/{max_attempts}")
    # In real scenario, you would check actual service status
    # time.sleep(2)

if attempts >= max_attempts:
    print("Service did not start in time")

# While with break
print("\nChecking until success:")
counter = 0
while True:
    counter += 1
    print(f"  Check #{counter}")
    
    if counter == 3:
        print("  Service is ready!")
        break
    
    if counter >= 10:
        print("  Timeout!")
        break

# While with continue
print("\nProcessing queue:")
queue = [1, 2, 0, 4, 5, 0, 7]
index = 0

while index < len(queue):
    item = queue[index]
    index += 1
    
    if item == 0:
        print(f"  Skipping invalid item at position {index}")
        continue
    
    print(f"  Processing item: {item}")

# Countdown timer
print("\nCountdown:")
seconds = 5
while seconds > 0:
    print(f"  {seconds} seconds remaining")
    seconds -= 1
    # time.sleep(1)
print("  Done!")
```

**Expected Output:**
```
Waiting for service to start...
  Attempt 1/5
  Attempt 2/5
  Attempt 3/5
  Attempt 4/5
  Attempt 5/5
Service did not start in time

Checking until success:
  Check #1
  Check #2
  Check #3
  Service is ready!

Processing queue:
  Processing item: 1
  Processing item: 2
  Skipping invalid item at position 3
  Processing item: 4
  Processing item: 5
  Skipping invalid item at position 6
  Processing item: 7

Countdown:
  5 seconds remaining
  4 seconds remaining
  3 seconds remaining
  2 seconds remaining
  1 seconds remaining
  Done!
```

### Exercise 3.2: While Loop for Retry Logic

```python
def connect_to_database(attempt):
    # Simulate connection attempts
    # In reality, this would try to connect to a database
    if attempt >= 3:
        return True
    return False

max_retries = 5
retry_count = 0
connected = False

print("Connecting to database...")
while retry_count < max_retries and not connected:
    retry_count += 1
    print(f"  Attempt {retry_count}/{max_retries}")
    
    connected = connect_to_database(retry_count)
    
    if connected:
        print("  ✓ Connection successful!")
    else:
        print("  ✗ Connection failed, retrying...")

if not connected:
    print("ERROR: Could not connect after maximum retries")

# Process items until queue is empty
print("\nProcessing deployment queue:")
deployment_queue = ["app-v1.2", "app-v1.3", "app-v1.4"]

while deployment_queue:
    app = deployment_queue.pop(0)
    print(f"  Deploying {app}")
    print(f"  Remaining in queue: {len(deployment_queue)}")

print("All deployments complete!")
```

**Expected Output:**
```
Connecting to database...
  Attempt 1/5
  ✗ Connection failed, retrying...
  Attempt 2/5
  ✗ Connection failed, retrying...
  Attempt 3/5
  ✓ Connection successful!

Processing deployment queue:
  Deploying app-v1.2
  Remaining in queue: 2
  Deploying app-v1.3
  Remaining in queue: 1
  Deploying app-v1.4
  Remaining in queue: 0
All deployments complete!
```

---

## Part 4: Exception Handling (try/except/finally)

### Exercise 4.1: Basic Exception Handling

Create `error_handling.py`:

```python
# Basic try-except
print("Example 1: Basic exception handling")
try:
    port = int("8080")
    print(f"Valid port: {port}")
except ValueError:
    print("Invalid port number")

# Handling invalid conversion
print("\nExample 2: Invalid conversion")
try:
    port = int("abc")
    print(f"Port: {port}")
except ValueError as e:
    print(f"Error: Cannot convert 'abc' to integer")
    print(f"Details: {e}")

# Multiple except blocks
print("\nExample 3: Multiple exception types")
servers = {"web-01": "10.0.1.10", "web-02": "10.0.1.11"}

try:
    # This will raise KeyError
    ip = servers["db-01"]
    print(f"IP: {ip}")
except KeyError:
    print("Error: Server not found in configuration")
except ValueError:
    print("Error: Invalid value")

# Catching any exception
print("\nExample 4: Catch all exceptions")
try:
    result = 10 / 0
except Exception as e:
    print(f"An error occurred: {type(e).__name__}: {e}")

# Using else block (executes if no exception)
print("\nExample 5: Using else block")
try:
    port = int("8080")
except ValueError:
    print("Invalid port")
else:
    print(f"Port {port} is valid")
    print("Proceeding with configuration...")
```

**Expected Output:**
```
Example 1: Basic exception handling
Valid port: 8080

Example 2: Invalid conversion
Error: Cannot convert 'abc' to integer
Details: invalid literal for int() with base 10: 'abc'

Example 3: Multiple exception types
Error: Server not found in configuration

Example 4: Catch all exceptions
An error occurred: ZeroDivisionError: division by zero

Example 5: Using else block
Port 8080 is valid
Proceeding with configuration...
```

### Exercise 4.2: Finally Block for Cleanup

```python
# Finally block always executes
def read_config_file(filename):
    print(f"Attempting to read {filename}")
    config_file = None
    
    try:
        # Simulate file operations
        if filename == "config.yaml":
            print("  Reading configuration...")
            config_data = {"app": "myapp", "port": 8080}
            return config_data
        else:
            raise FileNotFoundError(f"File {filename} not found")
    
    except FileNotFoundError as e:
        print(f"  Error: {e}")
        return None
    
    finally:
        print(f"  Cleanup: Closing file handler for {filename}")

# Test with valid file
print("Test 1: Valid file")
config = read_config_file("config.yaml")
print(f"Result: {config}\n")

# Test with invalid file
print("Test 2: Invalid file")
config = read_config_file("missing.yaml")
print(f"Result: {config}\n")

# Finally with return
def connect_with_cleanup():
    try:
        print("  Establishing connection...")
        return "Connected"
    except Exception:
        print("  Connection failed")
        return "Failed"
    finally:
        print("  Cleanup: Releasing resources")

print("Test 3: Finally with return")
result = connect_with_cleanup()
print(f"Result: {result}")
```

**Expected Output:**
```
Test 1: Valid file
Attempting to read config.yaml
  Reading configuration...
  Cleanup: Closing file handler for config.yaml
Result: {'app': 'myapp', 'port': 8080}

Test 2: Invalid file
Attempting to read missing.yaml
  Error: File missing.yaml not found
  Cleanup: Closing file handler for missing.yaml
Result: None

Test 3: Finally with return
  Establishing connection...
  Cleanup: Releasing resources
Result: Connected
```

### Exercise 4.3: Exception Handling in Loops

```python
# Handle exceptions while processing multiple items
servers = [
    {"name": "web-01", "port": "8080"},
    {"name": "web-02", "port": "invalid"},
    {"name": "web-03", "port": "8081"},
    {"name": "web-04"},  # Missing port
]

print("Processing server configurations:")
successful = 0
failed = 0

for server in servers:
    try:
        name = server["name"]
        port = int(server["port"])
        print(f"  ✓ {name}: port {port} configured successfully")
        successful += 1
    
    except KeyError:
        print(f"  ✗ {server['name']}: Missing port configuration")
        failed += 1
    
    except ValueError:
        print(f"  ✗ {name}: Invalid port value '{server['port']}'")
        failed += 1
    
    except Exception as e:
        print(f"  ✗ {server.get('name', 'Unknown')}: Unexpected error - {e}")
        failed += 1

print(f"\nSummary: {successful} successful, {failed} failed")

# Raise exceptions with custom messages
def validate_port(port):
    if not isinstance(port, int):
        raise TypeError("Port must be an integer")
    if port < 1 or port > 65535:
        raise ValueError(f"Port {port} is out of valid range (1-65535)")
    return True

print("\nPort validation:")
test_ports = [8080, "8080", 70000, 443]

for port in test_ports:
    try:
        validate_port(port)
        print(f"  ✓ Port {port} is valid")
    except (TypeError, ValueError) as e:
        print(f"  ✗ Port {port}: {e}")
```

**Expected Output:**
```
Processing server configurations:
  ✓ web-01: port 8080 configured successfully
  ✗ web-02: Invalid port value 'invalid'
  ✓ web-03: port 8081 configured successfully
  ✗ web-04: Missing port configuration

Summary: 2 successful, 2 failed

Port validation:
  ✓ Port 8080 is valid
  ✗ Port 8080: Port must be an integer
  ✗ Port 70000: Port 70000 is out of valid range (1-65535)
  ✓ Port 443 is valid
```

---

## Part 5: Practice Challenges

### Challenge 1: Server Health Monitor

Create a script that monitors server health and generates alerts:

```python
# Server data
servers = [
    {"name": "web-01", "cpu": 45, "memory": 67, "disk": 34, "status": "active"},
    {"name": "web-02", "cpu": 85, "memory": 92, "disk": 78, "status": "active"},
    {"name": "db-01", "cpu": 92, "memory": 88, "disk": 95, "status": "active"},
    {"name": "api-01", "cpu": 34, "memory": 45, "disk": 23, "status": "inactive"},
]

# Your task:
# 1. Loop through servers
# 2. Skip inactive servers
# 3. Check if CPU > 80 OR Memory > 85 OR Disk > 90
# 4. Print appropriate alert level:
#    - CRITICAL if 2 or more metrics are high
#    - WARNING if 1 metric is high
#    - OK if all metrics are normal
# 5. Count total alerts
```

<details>
<summary>Solution</summary>

```python
servers = [
    {"name": "web-01", "cpu": 45, "memory": 67, "disk": 34, "status": "active"},
    {"name": "web-02", "cpu": 85, "memory": 92, "disk": 78, "status": "active"},
    {"name": "db-01", "cpu": 92, "memory": 88, "disk": 95, "status": "active"},
    {"name": "api-01", "cpu": 34, "memory": 45, "disk": 23, "status": "inactive"},
]

print("Server Health Monitor")
print("=" * 60)

critical_count = 0
warning_count = 0
ok_count = 0

for server in servers:
    if server["status"] != "active":
        continue
    
    name = server["name"]
    high_metrics = 0
    issues = []
    
    if server["cpu"] > 80:
        high_metrics += 1
        issues.append(f"CPU: {server['cpu']}%")
    
    if server["memory"] > 85:
        high_metrics += 1
        issues.append(f"Memory: {server['memory']}%")
    
    if server["disk"] > 90:
        high_metrics += 1
        issues.append(f"Disk: {server['disk']}%")
    
    if high_metrics >= 2:
        print(f"CRITICAL: {name} - {', '.join(issues)}")
        critical_count += 1
    elif high_metrics == 1:
        print(f"WARNING:  {name} - {', '.join(issues)}")
        warning_count += 1
    else:
        print(f"OK:       {name}")
        ok_count += 1

print("=" * 60)
print(f"Summary: {critical_count} critical, {warning_count} warnings, {ok_count} ok")
```
</details>

### Challenge 2: Deployment Retry with Backoff

Implement a deployment function with exponential backoff retry:

```python
# Your task:
# 1. Create a function that simulates deployment
# 2. If deployment fails, retry up to 3 times
# 3. Use exponential backoff: wait 1s, 2s, 4s between retries
# 4. Handle exceptions gracefully
# 5. Return success/failure status

# Simulated deployment function (randomly fails first 2 attempts)
attempt_count = 0

def deploy_app():
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise Exception("Deployment failed: connection timeout")
    return True

# Implement your retry logic here
```

<details>
<summary>Solution</summary>

```python
import time

attempt_count = 0

def deploy_app():
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise Exception("Deployment failed: connection timeout")
    return True

def deploy_with_retry(max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Deployment attempt {attempt}/{max_retries}")
            result = deploy_app()
            print("✓ Deployment successful!")
            return True
        
        except Exception as e:
            print(f"✗ Attempt {attempt} failed: {e}")
            
            if attempt < max_retries:
                wait_time = 2 ** (attempt - 1)
                print(f"  Waiting {wait_time} seconds before retry...")
                # time.sleep(wait_time)
            else:
                print("✗ All retry attempts exhausted")
                return False
    
    return False

# Test the function
print("Starting deployment with retry logic:")
print("-" * 50)
success = deploy_with_retry()
print("-" * 50)
print(f"Final status: {'Success' if success else 'Failed'}")
```
</details>

### Challenge 3: Configuration Validator

Create a configuration validator with comprehensive error handling:

```python
# Your task: Validate this configuration
config = {
    "app_name": "myapp",
    "port": "8080",
    "workers": "abc",
    "timeout": 30,
    # "environment" is missing
}

# Requirements:
# 1. Check that required fields exist: app_name, port, workers, environment
# 2. Validate port is a number between 1-65535
# 3. Validate workers is a positive integer
# 4. Validate timeout is a positive number
# 5. Collect all validation errors (don't stop at first error)
# 6. Return list of errors or empty list if valid
```

<details>
<summary>Solution</summary>

```python
def validate_config(config):
    errors = []
    
    # Check required fields
    required_fields = ["app_name", "port", "workers", "environment"]
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    
    # Validate port
    if "port" in config:
        try:
            port = int(config["port"])
            if port < 1 or port > 65535:
                errors.append(f"Port {port} out of valid range (1-65535)")
        except (ValueError, TypeError):
            errors.append(f"Port must be a number, got: {config['port']}")
    
    # Validate workers
    if "workers" in config:
        try:
            workers = int(config["workers"])
            if workers <= 0:
                errors.append(f"Workers must be positive, got: {workers}")
        except (ValueError, TypeError):
            errors.append(f"Workers must be an integer, got: {config['workers']}")
    
    # Validate timeout
    if "timeout" in config:
        try:
            timeout = float(config["timeout"])
            if timeout <= 0:
                errors.append(f"Timeout must be positive, got: {timeout}")
        except (ValueError, TypeError):
            errors.append(f"Timeout must be a number, got: {config['timeout']}")
    
    return errors

# Test
config = {
    "app_name": "myapp",
    "port": "8080",
    "workers": "abc",
    "timeout": 30,
}

errors = validate_config(config)

if errors:
    print("Configuration validation failed:")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")
else:
    print("✓ Configuration is valid")
```
</details>

---

## Part 6: Real-World Scenario

### Scenario: Automated Service Health Checker

Create `service_health_checker.py`:

```python
import time

# Service configuration
services = [
    {"name": "nginx", "port": 80, "critical": True},
    {"name": "app", "port": 8080, "critical": True},
    {"name": "redis", "port": 6379, "critical": False},
    {"name": "postgres", "port": 5432, "critical": True},
]

def check_service(service_name, port):
    """Simulate checking if service is running on port"""
    # In reality, this would try to connect to the port
    # For demo, we'll simulate: nginx and redis are up, others are down
    if service_name in ["nginx", "redis"]:
        return True
    return False

def health_check_loop(services, max_retries=3):
    """Check all services and retry critical ones if they fail"""
    
    print("Starting health check...")
    print("=" * 70)
    
    all_healthy = True
    
    for service in services:
        name = service["name"]
        port = service["port"]
        is_critical = service["critical"]
        
        print(f"\nChecking {name} (port {port})...", end=" ")
        
        # For critical services, implement retry logic
        if is_critical:
            healthy = False
            
            for attempt in range(1, max_retries + 1):
                try:
                    if check_service(name, port):
                        print(f"✓ OK")
                        healthy = True
                        break
                    else:
                        if attempt < max_retries:
                            print(f"✗ (retry {attempt}/{max_retries})...", end=" ")
                            # time.sleep(1)
                        else:
                            print(f"✗ FAILED after {max_retries} attempts")
                
                except Exception as e:
                    print(f"✗ ERROR: {e}")
                    if attempt >= max_retries:
                        healthy = False
                        break
            
            if not healthy:
                print(f"  CRITICAL: {name} is not responding!")
                all_healthy = False
        
        else:
            # Non-critical services - single check
            try:
                if check_service(name, port):
                    print(f"✓ OK")
                else:
                    print(f"✗ DOWN (non-critical)")
            
            except Exception as e:
                print(f"✗ ERROR: {e} (non-critical)")
    
    print("\n" + "=" * 70)
    
    return all_healthy

# Run health check
overall_health = health_check_loop(services)

if overall_health:
    print("✓ All critical services are healthy")
    exit(0)
else:
    print("✗ One or more critical services are down!")
    exit(1)

# Example output simulation
```

**Expected Output:**
```
Starting health check...
======================================================================

Checking nginx (port 80)... ✓ OK

Checking app (port 8080)... ✗ (retry 1/3)... ✗ (retry 2/3)... ✗ FAILED after 3 attempts
  CRITICAL: app is not responding!

Checking redis (port 6379)... ✓ OK

Checking postgres (port 5432)... ✗ (retry 1/3)... ✗ (retry 2/3)... ✗ FAILED after 3 attempts
  CRITICAL: postgres is not responding!

======================================================================
✗ One or more critical services are down!
```

---

## What You Learned

In this lab, you learned:

✅ **Conditional Statements**
- Using if/elif/else for decision making
- Multiple conditions with and/or operators
- Ternary operators for concise conditionals
- Nested conditionals

✅ **For Loops**
- Iterating over lists, dictionaries, and ranges
- Using enumerate() for indexed iteration
- Loop control with break, continue, and else
- Nested loops for complex iterations

✅ **While Loops**
- Continuous operations and polling
- Implementing retry logic
- Processing queues
- Loop control and exit conditions

✅ **Exception Handling**
- try/except blocks for error handling
- Handling multiple exception types
- Using finally for cleanup operations
- Raising custom exceptions
- Error handling in loops

✅ **DevOps Applications**
- Service health monitoring
- Deployment automation with retries
- Configuration validation
- Batch processing with error handling
- Automated polling and checking

---

## Next Steps

- Move on to **LAB-04: Functions and Modules** to organize your code better
- Practice combining control flow with data structures
- Implement more complex retry and backoff strategies
- Create real health check scripts for your services

## Additional Resources

- [Python Control Flow Documentation](https://docs.python.org/3/tutorial/controlflow.html)
- [Python Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [PEP 8 - Programming Recommendations](https://pep8.org/#programming-recommendations)
