# Quick Start: Your First DevOps Python Script in 5 Minutes

Get started with Python automation immediately with this hands-on guide.

## Prerequisites

- Python 3.9+ installed
- 5 minutes of your time
- A text editor (VS Code, vim, nano, etc.)

---

## Step 1: Verify Python Installation (30 seconds)

```bash
python3 --version
# Should show: Python 3.9.x or higher

pip3 --version
# Should show: pip x.x.x
```

If not installed, see [SETUP.md](SETUP.md).

---

## Step 2: Create Your First Script (2 minutes)

Create a file called `server_health_check.py`:

```python
#!/usr/bin/env python3
"""
DevOps Script: Check if web servers are responding
"""

import sys
import time
from urllib.request import urlopen
from urllib.error import URLError

def check_server(url, timeout=5):
    """Check if a server is responding."""
    try:
        with urlopen(url, timeout=timeout) as response:
            status = response.status
            if status == 200:
                print(f"✓ {url} is UP (Status: {status})")
                return True
            else:
                print(f"✗ {url} returned Status: {status}")
                return False
    except URLError as e:
        print(f"✗ {url} is DOWN - Error: {e.reason}")
        return False
    except TimeoutError:
        print(f"✗ {url} TIMEOUT after {timeout}s")
        return False

def main():
    """Main function to check multiple servers."""
    print("=" * 50)
    print("Server Health Check")
    print("=" * 50)
    
    # List of servers to check
    servers = [
        "https://www.google.com",
        "https://www.github.com",
        "https://httpbin.org/status/200",
    ]
    
    results = []
    for server in servers:
        print(f"Checking {server}...")
        is_up = check_server(server)
        results.append(is_up)
        time.sleep(0.5)  # Small delay between checks
    
    print("=" * 50)
    healthy_count = sum(results)
    total_count = len(results)
    print(f"Results: {healthy_count}/{total_count} servers healthy")
    print("=" * 50)
    
    # Exit with status code
    # 0 = success (all healthy), 1 = failure (some down)
    sys.exit(0 if all(results) else 1)

if __name__ == "__main__":
    main()
```

---

## Step 3: Make It Executable and Run (1 minute)

```bash
# Make the script executable
chmod +x server_health_check.py

# Run it
./server_health_check.py

# Or run with python3
python3 server_health_check.py
```

**Expected Output:**
```
==================================================
Server Health Check
==================================================
Checking https://www.google.com...
✓ https://www.google.com is UP (Status: 200)
Checking https://www.github.com...
✓ https://www.github.com is UP (Status: 200)
Checking https://httpbin.org/status/200...
✓ https://httpbin.org/status/200 is UP (Status: 200)
==================================================
Results: 3/3 servers healthy
==================================================
```

---

## Step 4: Customize It (1 minute)

Try modifying the script:

### Add Your Own Servers

```python
servers = [
    "https://www.google.com",
    "https://www.github.com",
    "https://your-company-api.com/health",  # Add your API
    "https://your-website.com",             # Add your website
]
```

### Change Timeout

```python
is_up = check_server(server, timeout=10)  # Wait up to 10 seconds
```

### Test Error Handling

Add a fake server to see the error handling:

```python
servers = [
    "https://www.google.com",
    "https://fake-server-that-doesnt-exist.xyz",  # This will fail
    "https://httpbin.org/status/500",             # This returns 500
]
```

---

## Step 5: Check Exit Codes (30 seconds)

Python scripts should return exit codes for automation:

```bash
# Run the script
./server_health_check.py

# Check exit code
echo $?
# Output: 0 (success) or 1 (failure)
```

**Use in shell scripts:**
```bash
#!/bin/bash
if python3 server_health_check.py; then
    echo "All servers healthy, proceeding with deployment"
    # deploy.sh
else
    echo "Some servers unhealthy, aborting deployment"
    exit 1
fi
```

---

## What You Just Learned

In 5 minutes, you created a real DevOps script that:

✅ **Checks server health** - Practical automation task  
✅ **Handles errors** - Try/except for network failures  
✅ **Returns exit codes** - Integrates with shell scripts  
✅ **Provides clear output** - Readable status messages  
✅ **Follows best practices** - Shebang, docstrings, main function  

---

## Next Steps

### Immediate Next Steps (10 minutes)

**Add command-line arguments:**

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description='Check server health')
    parser.add_argument('--timeout', type=int, default=5, help='Timeout in seconds')
    parser.add_argument('servers', nargs='+', help='URLs to check')
    args = parser.parse_args()
    
    for server in args.servers:
        check_server(server, timeout=args.timeout)

# Usage:
# ./server_health_check.py https://google.com https://github.com --timeout 10
```

**Add logging:**

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='health_check.log'
)
logger = logging.getLogger(__name__)

def check_server(url, timeout=5):
    try:
        # ... existing code ...
        logger.info(f"{url} is UP")
    except URLError as e:
        logger.error(f"{url} is DOWN: {e.reason}")
```

### Continue Your Learning

1. **Install the requests library** for better HTTP handling:
   ```bash
   pip install requests
   ```

2. **Complete LAB-01**: [Python Basics](LABS/LAB-01-python-basics.md)

3. **Read Concepts**: [CONCEPTS.md](CONCEPTS.md)

4. **Build a real project**: [Infrastructure Inventory](PROJECTS/PROJECT-01-infrastructure-inventory.md)

---

## Bonus: More Quick Examples

### Example 2: Simple File Processor (2 minutes)

```python
#!/usr/bin/env python3
"""Process log file and count errors."""

import sys
from collections import Counter

def analyze_log(filename):
    """Count error levels in log file."""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        # Count log levels
        levels = [line.split()[2] for line in lines if len(line.split()) > 2]
        counts = Counter(levels)
        
        print(f"Log Analysis: {filename}")
        print("-" * 40)
        for level, count in counts.most_common():
            print(f"{level}: {count}")
        
        return 0
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./analyze_log.py <logfile>")
        sys.exit(1)
    
    sys.exit(analyze_log(sys.argv[1]))
```

**Create test log:**
```bash
cat > test.log << 'EOF'
2024-01-01 10:00:00 INFO Application started
2024-01-01 10:00:01 INFO User logged in
2024-01-01 10:00:02 WARNING Slow query detected
2024-01-01 10:00:03 ERROR Database connection failed
2024-01-01 10:00:04 ERROR Timeout occurred
2024-01-01 10:00:05 INFO Request processed
EOF

chmod +x analyze_log.py
./analyze_log.py test.log
```

### Example 3: Environment Checker (2 minutes)

```python
#!/usr/bin/env python3
"""Check required environment variables for deployment."""

import os
import sys

REQUIRED_VARS = [
    'ENVIRONMENT',
    'DATABASE_URL',
    'API_KEY',
]

def check_environment():
    """Verify all required environment variables are set."""
    missing = []
    
    print("Environment Variable Check")
    print("=" * 50)
    
    for var in REQUIRED_VARS:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            display_value = value if 'KEY' not in var else '***'
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: NOT SET")
            missing.append(var)
    
    print("=" * 50)
    
    if missing:
        print(f"ERROR: Missing variables: {', '.join(missing)}")
        return 1
    else:
        print("All required variables are set!")
        return 0

if __name__ == "__main__":
    sys.exit(check_environment())
```

**Test it:**
```bash
# Set environment variables
export ENVIRONMENT=production
export DATABASE_URL=postgresql://localhost/mydb
export API_KEY=secret123

# Run checker
chmod +x check_env.py
./check_env.py
```

---

## Congratulations! 🎉

You've written your first DevOps Python scripts! You now understand:

- Python script structure
- Error handling
- Exit codes
- Command-line interaction
- File operations
- Environment variables

**Ready for more?** Start with [LAB-01-python-basics.md](LABS/LAB-01-python-basics.md)!
