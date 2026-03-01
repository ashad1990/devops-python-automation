# LAB 06: OS Module and Subprocess for DevOps

## Learning Objectives
By the end of this lab, you will be able to:
- Use the os module for operating system interactions
- Execute shell commands with subprocess
- Manage environment variables
- Work with file system operations using os and shutil
- Use pathlib for modern path operations
- Implement system automation scripts
- Handle command output and errors

## Prerequisites
- Completed LAB-01 through LAB-05
- Understanding of file operations
- Basic shell/command line knowledge

---

## Part 1: OS Module Basics

### Exercise 1.1: Environment Variables

Create `os_environment.py`:

```python
import os

# Get environment variables
print("Environment Variables:")
print(f"User: {os.getenv('USER', 'unknown')}")
print(f"Home: {os.getenv('HOME', 'unknown')}")
print(f"Shell: {os.getenv('SHELL', 'unknown')}")
print(f"Path: {os.getenv('PATH', 'not set')[:50]}...")

# Set environment variable (for current process)
os.environ['APP_ENV'] = 'production'
os.environ['APP_PORT'] = '8080'

print(f"\nSet APP_ENV: {os.getenv('APP_ENV')}")
print(f"Set APP_PORT: {os.getenv('APP_PORT')}")

# Check if variable exists
if 'APP_ENV' in os.environ:
    print("APP_ENV is set")

# Get with default value
debug_mode = os.getenv('DEBUG', 'false')
print(f"Debug mode: {debug_mode}")

# List all environment variables
print("\nAll environment variables:")
for key, value in sorted(os.environ.items())[:5]:  # First 5
    print(f"  {key}: {value[:30]}...")

# Build configuration from environment
config = {
    'environment': os.getenv('APP_ENV', 'development'),
    'port': int(os.getenv('APP_PORT', '8000')),
    'debug': os.getenv('DEBUG', 'false').lower() == 'true',
    'log_level': os.getenv('LOG_LEVEL', 'INFO')
}

print(f"\nApplication config from environment:")
for key, value in config.items():
    print(f"  {key}: {value}")
```

**Expected Output:**
```
Environment Variables:
User: runner
Home: /home/runner
Shell: /bin/bash
Path: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr...

Set APP_ENV: production
Set APP_PORT: 8080
APP_ENV is set
Debug mode: false

All environment variables:
  HOME: /home/runner...
  HOSTNAME: ...
  LANG: ...
  PATH: ...
  PWD: ...

Application config from environment:
  environment: production
  port: 8080
  debug: False
  log_level: INFO
```

### Exercise 1.2: System Information

```python
import os
import platform

print("System Information:")
print(f"Operating System: {os.name}")
print(f"Platform: {platform.system()}")
print(f"Platform Release: {platform.release()}")
print(f"Platform Version: {platform.version()}")
print(f"Machine: {platform.machine()}")
print(f"Processor: {platform.processor()}")
print(f"Python Version: {platform.python_version()}")

# Process information
print(f"\nProcess Information:")
print(f"Process ID: {os.getpid()}")
print(f"Parent Process ID: {os.getppid()}")

# Path information
print(f"\nPath Information:")
print(f"Current directory: {os.getcwd()}")
print(f"Path separator: {os.sep}")
print(f"Path list separator: {os.pathsep}")
print(f"Line separator: {repr(os.linesep)}")

# System load (Unix-like systems only)
try:
    load_avg = os.getloadavg()
    print(f"\nSystem Load Average: {load_avg}")
except AttributeError:
    print("\nLoad average not available on this platform")

# CPU count
try:
    cpu_count = os.cpu_count()
    print(f"CPU Count: {cpu_count}")
except AttributeError:
    print("CPU count not available")
```

### Exercise 1.3: Directory Operations

```python
import os

print("Directory Operations:\n")

# Current working directory
cwd = os.getcwd()
print(f"Current directory: {cwd}")

# List directory contents
print(f"\nFiles in current directory:")
items = os.listdir('.')
for item in sorted(items)[:10]:  # First 10 items
    full_path = os.path.join('.', item)
    item_type = "DIR" if os.path.isdir(full_path) else "FILE"
    print(f"  [{item_type}] {item}")

# Create directory
test_dir = "test_automation"
if not os.path.exists(test_dir):
    os.mkdir(test_dir)
    print(f"\nCreated directory: {test_dir}")
else:
    print(f"\nDirectory already exists: {test_dir}")

# Create nested directories
nested_dir = os.path.join("logs", "archive", "2024")
os.makedirs(nested_dir, exist_ok=True)
print(f"Created nested directory: {nested_dir}")

# Change directory
original_dir = os.getcwd()
os.chdir(test_dir)
print(f"\nChanged to: {os.getcwd()}")

# Go back
os.chdir(original_dir)
print(f"Back to: {os.getcwd()}")

# Walk directory tree
print("\nDirectory tree walk:")
for root, dirs, files in os.walk('.'):
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    
    sub_indent = ' ' * 2 * (level + 1)
    for file in files[:3]:  # Limit files shown
        print(f"{sub_indent}{file}")
    
    if len(files) > 3:
        print(f"{sub_indent}... and {len(files) - 3} more files")
    
    # Limit depth
    if level >= 2:
        break
```

---

## Part 2: File and Path Operations

### Exercise 2.1: Path Manipulation

Create `path_operations.py`:

```python
import os

# Join paths
config_dir = "config"
config_file = "app.yaml"
full_path = os.path.join(config_dir, config_file)
print(f"Joined path: {full_path}")

# More complex path joining
log_path = os.path.join("var", "log", "application", "app.log")
print(f"Log path: {log_path}")

# Split path
directory, filename = os.path.split(full_path)
print(f"\nDirectory: {directory}")
print(f"Filename: {filename}")

# Split extension
name, ext = os.path.splitext(filename)
print(f"Name: {name}")
print(f"Extension: {ext}")

# Absolute path
abs_path = os.path.abspath("sample.log")
print(f"\nAbsolute path: {abs_path}")

# Directory name and base name
print(f"Directory name: {os.path.dirname(abs_path)}")
print(f"Base name: {os.path.basename(abs_path)}")

# Expand user path
home_config = os.path.expanduser("~/.config/app")
print(f"\nExpanded path: {home_config}")

# Normalize path
messy_path = "./config/../logs/./app.log"
normalized = os.path.normpath(messy_path)
print(f"Normalized path: {normalized}")

# Check if path exists
paths = ["sample.log", "nonexistent.txt", ".", "config"]
print("\nPath existence check:")
for path in paths:
    exists = "EXISTS" if os.path.exists(path) else "NOT FOUND"
    print(f"  {path}: {exists}")

# Check path types
print("\nPath types:")
test_paths = [".", "sample.log"]
for path in test_paths:
    if os.path.exists(path):
        is_file = os.path.isfile(path)
        is_dir = os.path.isdir(path)
        is_link = os.path.islink(path)
        print(f"  {path}: file={is_file}, dir={is_dir}, link={is_link}")
```

### Exercise 2.2: File Information and Metadata

```python
import os
import time
from datetime import datetime

# File stats
filename = "sample.log"

if os.path.exists(filename):
    stats = os.stat(filename)
    
    print(f"File Information for {filename}:")
    print(f"Size: {stats.st_size} bytes")
    print(f"Mode: {oct(stats.st_mode)}")
    
    # Times
    created = datetime.fromtimestamp(stats.st_ctime)
    modified = datetime.fromtimestamp(stats.st_mtime)
    accessed = datetime.fromtimestamp(stats.st_atime)
    
    print(f"Created: {created}")
    print(f"Modified: {modified}")
    print(f"Accessed: {accessed}")
    
    # Permissions
    print(f"\nPermissions:")
    print(f"Readable: {os.access(filename, os.R_OK)}")
    print(f"Writable: {os.access(filename, os.W_OK)}")
    print(f"Executable: {os.access(filename, os.X_OK)}")
    
    # Size formatting
    def format_size(bytes_value):
        """Format bytes to human readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} TB"
    
    print(f"\nFormatted size: {format_size(stats.st_size)}")

# Get file size
def get_directory_size(directory):
    """Calculate total size of directory"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

# Test with current directory
size = get_directory_size('.')
print(f"\nCurrent directory size: {format_size(size)}")
```

---

## Part 3: Shutil for Advanced File Operations

### Exercise 3.1: Copying and Moving Files

Create `shutil_operations.py`:

```python
import shutil
import os

# Create test file
with open("test_file.txt", "w") as f:
    f.write("This is a test file for shutil operations\n")

print("File Operations with shutil:\n")

# Copy file
shutil.copy("test_file.txt", "test_file_copy.txt")
print("Copied test_file.txt to test_file_copy.txt")

# Copy file with metadata
shutil.copy2("test_file.txt", "test_file_copy2.txt")
print("Copied with metadata to test_file_copy2.txt")

# Copy to directory
os.makedirs("backup", exist_ok=True)
shutil.copy("test_file.txt", "backup/")
print("Copied to backup/ directory")

# Move file
shutil.move("test_file_copy2.txt", "backup/moved_file.txt")
print("Moved test_file_copy2.txt to backup/")

# Copy directory tree
source_dir = "logs"
target_dir = "logs_backup"

if os.path.exists(source_dir):
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    shutil.copytree(source_dir, target_dir)
    print(f"\nCopied directory tree: {source_dir} -> {target_dir}")

# Archive directory
archive_name = "logs_archive"
shutil.make_archive(archive_name, 'zip', source_dir)
print(f"Created archive: {archive_name}.zip")

# List available archive formats
formats = shutil.get_archive_formats()
print(f"\nAvailable archive formats: {[f[0] for f in formats]}")

# Extract archive
extract_dir = "extracted_logs"
if os.path.exists(f"{archive_name}.zip"):
    shutil.unpack_archive(f"{archive_name}.zip", extract_dir)
    print(f"Extracted archive to: {extract_dir}")
```

### Exercise 3.2: Disk Usage and Cleanup

```python
import shutil
import os

# Get disk usage
def get_disk_usage(path='.'):
    """Get disk usage statistics"""
    usage = shutil.disk_usage(path)
    
    def format_bytes(bytes_val):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024
        return f"{bytes_val:.2f} PB"
    
    total = format_bytes(usage.total)
    used = format_bytes(usage.used)
    free = format_bytes(usage.free)
    percent = (usage.used / usage.total) * 100
    
    return {
        'total': total,
        'used': used,
        'free': free,
        'percent': f"{percent:.1f}%"
    }

# Display disk usage
usage = get_disk_usage('/')
print("Disk Usage:")
for key, value in usage.items():
    print(f"  {key}: {value}")

# Clean up old files
def cleanup_old_files(directory, days_old=7):
    """Remove files older than specified days"""
    import time
    
    if not os.path.exists(directory):
        return []
    
    current_time = time.time()
    seconds_in_day = 24 * 60 * 60
    cutoff_time = current_time - (days_old * seconds_in_day)
    
    removed_files = []
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath):
            file_modified = os.path.getmtime(filepath)
            
            if file_modified < cutoff_time:
                os.remove(filepath)
                removed_files.append(filename)
    
    return removed_files

# Test cleanup (be careful with this in real scenarios!)
# removed = cleanup_old_files('logs/archive', days_old=30)
# print(f"\nRemoved {len(removed)} old files")
```

---

## Part 4: Subprocess Module

### Exercise 4.1: Running Shell Commands

Create `subprocess_basic.py`:

```python
import subprocess

print("Running Shell Commands:\n")

# Simple command - run and wait
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)

print("Command: ls -l")
print(f"Return code: {result.returncode}")
print(f"Output:\n{result.stdout}")

# Run command and capture output
result = subprocess.run(['pwd'], capture_output=True, text=True)
print(f"Current directory: {result.stdout.strip()}")

# Run with shell=True (for complex commands)
result = subprocess.run('echo "Hello from shell"', shell=True, 
                       capture_output=True, text=True)
print(f"Shell echo: {result.stdout.strip()}")

# Check command success
result = subprocess.run(['python3', '--version'], 
                       capture_output=True, text=True)
if result.returncode == 0:
    print(f"Python version: {result.stdout.strip()}")
else:
    print(f"Error: {result.stderr}")

# Handle command that might fail
try:
    result = subprocess.run(['ls', 'nonexistent_file'], 
                           capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"\nCommand failed with exit code {e.returncode}")
    print(f"Error output: {e.stderr.strip()}")

# Multiple commands with pipe
result = subprocess.run('ls -l | head -n 5', shell=True,
                       capture_output=True, text=True)
print(f"\nFirst 5 files:\n{result.stdout}")
```

### Exercise 4.2: System Administration Commands

```python
import subprocess
import sys

def run_command(command, description=""):
    """Run command and return result"""
    if description:
        print(f"\n{description}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            shell=isinstance(command, str)
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

# System information commands
print("System Information Commands:\n")

# Disk usage
success, output = run_command('df -h', "Disk usage:")
if success:
    print(output)

# Memory usage
success, output = run_command('free -h', "\nMemory usage:")
if success:
    print(output)

# Process list (limited)
success, output = run_command('ps aux | head -n 10', "\nTop processes:")
if success:
    print(output)

# Network interfaces
success, output = run_command('ip addr show', "\nNetwork interfaces:")
if success:
    lines = output.split('\n')[:20]  # First 20 lines
    print('\n'.join(lines))

# Uptime
success, output = run_command('uptime', "\nSystem uptime:")
if success:
    print(output)

# Check if service is running (systemd)
def check_service_status(service_name):
    """Check if systemd service is running"""
    cmd = f"systemctl is-active {service_name}"
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip() == "active"

# Example (this will fail on systems without these services)
# is_active = check_service_status("nginx")
# print(f"\nNginx service active: {is_active}")
```

### Exercise 4.3: Interactive Commands and Timeouts

```python
import subprocess
import time

# Command with timeout
def run_with_timeout(command, timeout_seconds=5):
    """Run command with timeout"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            shell=isinstance(command, str)
        )
        return True, result.stdout, result.returncode
    
    except subprocess.TimeoutExpired:
        return False, f"Command timed out after {timeout_seconds}s", None
    
    except Exception as e:
        return False, str(e), None

# Test with quick command
success, output, code = run_with_timeout(['echo', 'test'], timeout_seconds=2)
print(f"Quick command: {output.strip()}")

# Test with timeout (sleep for long time)
success, output, code = run_with_timeout(['sleep', '10'], timeout_seconds=2)
if not success:
    print(f"Timeout test: {output}")

# Pipe commands together
def pipe_commands(cmd1, cmd2):
    """Pipe output from cmd1 to cmd2"""
    p1 = subprocess.Popen(
        cmd1,
        stdout=subprocess.PIPE,
        text=True
    )
    
    p2 = subprocess.Popen(
        cmd2,
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )
    
    p1.stdout.close()
    output, _ = p2.communicate()
    return output

# Example: ls | grep py
try:
    result = pipe_commands(['ls'], ['grep', 'py'])
    print(f"\nPython files:\n{result}")
except Exception as e:
    print(f"Pipe error: {e}")

# Run command in background
def run_background(command):
    """Start command in background"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return process

# Example background process (commented to avoid hanging)
# proc = run_background(['sleep', '5'])
# print(f"Started background process: PID {proc.pid}")
# time.sleep(1)
# if proc.poll() is None:
#     print("Process still running...")
```

---

## Part 5: Combining OS and Subprocess

### Exercise 5.1: Server Monitoring Script

Create `server_monitor.py`:

```python
import os
import subprocess
import platform
from datetime import datetime

def get_system_info():
    """Gather system information"""
    info = {
        'hostname': platform.node(),
        'os': platform.system(),
        'os_version': platform.release(),
        'python_version': platform.python_version(),
        'cpu_count': os.cpu_count(),
    }
    
    # Get load average (Unix only)
    try:
        load = os.getloadavg()
        info['load_average'] = f"{load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}"
    except AttributeError:
        info['load_average'] = "N/A"
    
    return info

def get_disk_usage():
    """Get disk usage information"""
    import shutil
    
    usage = shutil.disk_usage('/')
    total_gb = usage.total / (1024**3)
    used_gb = usage.used / (1024**3)
    free_gb = usage.free / (1024**3)
    percent = (usage.used / usage.total) * 100
    
    return {
        'total': f"{total_gb:.2f} GB",
        'used': f"{used_gb:.2f} GB",
        'free': f"{free_gb:.2f} GB",
        'percent': f"{percent:.1f}%"
    }

def get_memory_info():
    """Get memory information (Linux)"""
    try:
        result = subprocess.run(
            ['free', '-m'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            mem_line = lines[1].split()
            
            total = int(mem_line[1])
            used = int(mem_line[2])
            free = int(mem_line[3])
            percent = (used / total) * 100
            
            return {
                'total': f"{total} MB",
                'used': f"{used} MB",
                'free': f"{free} MB",
                'percent': f"{percent:.1f}%"
            }
    except Exception:
        pass
    
    return {'error': 'Unable to get memory info'}

def check_process_running(process_name):
    """Check if a process is running"""
    try:
        result = subprocess.run(
            ['pgrep', '-f', process_name],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False

def generate_monitoring_report():
    """Generate comprehensive monitoring report"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print("=" * 70)
    print(f"SERVER MONITORING REPORT - {timestamp}")
    print("=" * 70)
    
    # System Information
    print("\nSYSTEM INFORMATION:")
    sys_info = get_system_info()
    for key, value in sys_info.items():
        print(f"  {key}: {value}")
    
    # Disk Usage
    print("\nDISK USAGE:")
    disk = get_disk_usage()
    for key, value in disk.items():
        print(f"  {key}: {value}")
    
    # Memory Usage
    print("\nMEMORY USAGE:")
    mem = get_memory_info()
    for key, value in mem.items():
        print(f"  {key}: {value}")
    
    # Process Checks
    print("\nPROCESS CHECKS:")
    processes = ['python', 'bash', 'systemd']
    for proc in processes:
        status = "RUNNING" if check_process_running(proc) else "NOT FOUND"
        print(f"  {proc}: {status}")
    
    print("\n" + "=" * 70)

# Generate report
if __name__ == "__main__":
    generate_monitoring_report()
```

### Exercise 5.2: Automated Backup Script

```python
import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

def create_backup_archive(source_dir, backup_dir):
    """Create timestamped backup archive"""
    
    # Create backup directory
    backup_path = Path(backup_dir)
    backup_path.mkdir(parents=True, exist_ok=True)
    
    # Create timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Archive name
    archive_name = f"backup_{timestamp}"
    archive_path = backup_path / archive_name
    
    # Create tar.gz archive
    print(f"Creating backup archive: {archive_name}.tar.gz")
    
    try:
        # Using shutil
        shutil.make_archive(
            str(archive_path),
            'gztar',
            source_dir
        )
        
        archive_file = f"{archive_path}.tar.gz"
        size = os.path.getsize(archive_file)
        size_mb = size / (1024 * 1024)
        
        print(f"✓ Backup created: {archive_file}")
        print(f"  Size: {size_mb:.2f} MB")
        
        return True, archive_file
    
    except Exception as e:
        print(f"✗ Backup failed: {e}")
        return False, None

def cleanup_old_backups(backup_dir, keep_count=5):
    """Keep only the most recent N backups"""
    
    backup_path = Path(backup_dir)
    if not backup_path.exists():
        return
    
    # Get all backup files
    backups = sorted(
        backup_path.glob("backup_*.tar.gz"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    # Remove old backups
    removed = 0
    for old_backup in backups[keep_count:]:
        old_backup.unlink()
        print(f"  Removed old backup: {old_backup.name}")
        removed += 1
    
    if removed > 0:
        print(f"✓ Cleaned up {removed} old backup(s)")

def backup_with_rsync(source, destination):
    """Backup using rsync command"""
    
    cmd = [
        'rsync',
        '-av',
        '--delete',
        source,
        destination
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✓ Rsync backup completed")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"✗ Rsync backup failed: {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ rsync command not found")
        return False

# Example usage
if __name__ == "__main__":
    print("Automated Backup Script")
    print("=" * 50)
    
    # Create test directory
    source = "logs"
    if not os.path.exists(source):
        os.makedirs(source)
        # Create some test files
        for i in range(3):
            with open(f"{source}/log_{i}.txt", "w") as f:
                f.write(f"Log entry {i}\n")
    
    # Create backup
    success, archive = create_backup_archive(source, "backups")
    
    if success:
        # Cleanup old backups
        print("\nCleaning up old backups...")
        cleanup_old_backups("backups", keep_count=3)
    
    print("\n" + "=" * 50)
```

---

## Part 6: Practice Challenges

### Challenge 1: Log Rotation Script

Create a script that rotates log files:

```python
# Your task:
# 1. Find all .log files in logs/ directory
# 2. For files > 1MB, rename to filename.log.1
# 3. If .log.1 exists, rename to .log.2, etc.
# 4. Keep max 5 rotated logs
# 5. Compress old logs with gzip

# Requirements:
# - Use os module for file operations
# - Use subprocess for gzip compression
# - Handle errors gracefully
```

<details>
<summary>Solution</summary>

```python
import os
import subprocess
from pathlib import Path

def rotate_log(log_file, max_rotations=5):
    """Rotate a single log file"""
    
    # Rotate existing backups
    for i in range(max_rotations - 1, 0, -1):
        old = f"{log_file}.{i}"
        new = f"{log_file}.{i + 1}"
        
        if os.path.exists(old):
            if i + 1 > max_rotations:
                os.remove(old)
                print(f"  Removed old rotation: {old}")
            else:
                os.rename(old, new)
                print(f"  Rotated: {old} -> {new}")
    
    # Move current log to .1
    if os.path.exists(log_file):
        os.rename(log_file, f"{log_file}.1")
        print(f"  Rotated: {log_file} -> {log_file}.1")
        
        # Create new empty log
        open(log_file, 'w').close()
        print(f"  Created new: {log_file}")

def compress_old_logs(directory):
    """Compress rotated logs with gzip"""
    
    for file in Path(directory).glob("*.log.[0-9]*"):
        if not str(file).endswith('.gz'):
            try:
                subprocess.run(
                    ['gzip', str(file)],
                    check=True
                )
                print(f"  Compressed: {file}")
            except subprocess.CalledProcessError:
                print(f"  Failed to compress: {file}")

def rotate_logs_in_directory(directory, size_limit_mb=1):
    """Rotate all logs over size limit"""
    
    size_limit_bytes = size_limit_mb * 1024 * 1024
    
    print(f"Log Rotation in {directory}")
    print("=" * 50)
    
    log_dir = Path(directory)
    if not log_dir.exists():
        print(f"Directory not found: {directory}")
        return
    
    for log_file in log_dir.glob("*.log"):
        size = log_file.stat().st_size
        size_mb = size / (1024 * 1024)
        
        if size > size_limit_bytes:
            print(f"\nRotating {log_file.name} ({size_mb:.2f} MB):")
            rotate_log(str(log_file))
    
    print("\nCompressing old logs:")
    compress_old_logs(directory)
    
    print("\n" + "=" * 50)

# Test
if __name__ == "__main__":
    # Create test logs
    os.makedirs("logs", exist_ok=True)
    
    with open("logs/app.log", "w") as f:
        f.write("X" * (2 * 1024 * 1024))  # 2MB file
    
    rotate_logs_in_directory("logs", size_limit_mb=1)
```
</details>

### Challenge 2: Service Health Checker

Create a script that checks service health:

```python
# Your task:
# 1. Check if specific ports are listening (80, 443, 22, 3306)
# 2. Check if processes are running (nginx, mysql, sshd)
# 3. Check disk usage < 80%
# 4. Check memory usage < 90%
# 5. Generate health report with status for each check
# 6. Exit with code 0 if all healthy, 1 if any issues

# Use subprocess for system commands
```

<details>
<summary>Solution</summary>

```python
import subprocess
import shutil
import sys

def check_port_listening(port):
    """Check if port is listening"""
    try:
        result = subprocess.run(
            f"netstat -tuln | grep ':{port} '",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False

def check_process_running(process_name):
    """Check if process is running"""
    try:
        result = subprocess.run(
            ['pgrep', '-f', process_name],
            capture_output=True
        )
        return result.returncode == 0
    except Exception:
        return False

def check_disk_usage(threshold=80):
    """Check if disk usage is below threshold"""
    usage = shutil.disk_usage('/')
    percent = (usage.used / usage.total) * 100
    return percent < threshold, percent

def check_memory_usage(threshold=90):
    """Check if memory usage is below threshold"""
    try:
        result = subprocess.run(
            ['free'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            mem_line = lines[1].split()
            
            total = int(mem_line[1])
            used = int(mem_line[2])
            percent = (used / total) * 100
            
            return percent < threshold, percent
    except Exception:
        pass
    
    return True, 0

def run_health_checks():
    """Run all health checks and generate report"""
    
    print("SERVICE HEALTH CHECK")
    print("=" * 60)
    
    all_healthy = True
    
    # Port checks
    print("\nPORT CHECKS:")
    ports = [22, 80, 443, 3306]
    for port in ports:
        status = check_port_listening(port)
        symbol = "✓" if status else "✗"
        status_text = "LISTENING" if status else "NOT LISTENING"
        print(f"  {symbol} Port {port}: {status_text}")
        if not status:
            all_healthy = False
    
    # Process checks
    print("\nPROCESS CHECKS:")
    processes = ['sshd', 'nginx', 'mysql']
    for proc in processes:
        status = check_process_running(proc)
        symbol = "✓" if status else "✗"
        status_text = "RUNNING" if status else "NOT RUNNING"
        print(f"  {symbol} {proc}: {status_text}")
        if not status:
            all_healthy = False
    
    # Disk check
    print("\nRESOURCE CHECKS:")
    disk_ok, disk_percent = check_disk_usage(80)
    symbol = "✓" if disk_ok else "✗"
    status = "OK" if disk_ok else "HIGH"
    print(f"  {symbol} Disk Usage: {disk_percent:.1f}% ({status})")
    if not disk_ok:
        all_healthy = False
    
    # Memory check
    mem_ok, mem_percent = check_memory_usage(90)
    symbol = "✓" if mem_ok else "✗"
    status = "OK" if mem_ok else "HIGH"
    print(f"  {symbol} Memory Usage: {mem_percent:.1f}% ({status})")
    if not mem_ok:
        all_healthy = False
    
    print("\n" + "=" * 60)
    
    if all_healthy:
        print("✓ ALL CHECKS PASSED")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        return 1

# Run checks
if __name__ == "__main__":
    exit_code = run_health_checks()
    sys.exit(exit_code)
```
</details>

### Challenge 3: Deployment Automation

Create a deployment script:

```python
# Your task:
# 1. Pull latest code from git
# 2. Install dependencies (pip install -r requirements.txt)
# 3. Run database migrations
# 4. Restart application service
# 5. Verify service is running
# 6. Rollback if any step fails

# Requirements:
# - Use subprocess for all commands
# - Implement proper error handling
# - Log all steps
# - Create backup before deployment
```

<details>
<summary>Solution</summary>

```python
import subprocess
import os
import shutil
from datetime import datetime
from pathlib import Path

class DeploymentManager:
    """Manage application deployment"""
    
    def __init__(self, app_dir, service_name):
        self.app_dir = Path(app_dir)
        self.service_name = service_name
        self.backup_dir = None
        self.log_entries = []
    
    def log(self, message, level="INFO"):
        """Log a message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"[{timestamp}] [{level}] {message}"
        self.log_entries.append(entry)
        print(entry)
    
    def run_command(self, command, description):
        """Run command and log result"""
        self.log(f"Running: {description}")
        
        try:
            result = subprocess.run(
                command,
                cwd=self.app_dir,
                capture_output=True,
                text=True,
                check=True,
                shell=isinstance(command, str)
            )
            self.log(f"✓ {description} completed")
            return True, result.stdout
        
        except subprocess.CalledProcessError as e:
            self.log(f"✗ {description} failed: {e.stderr}", "ERROR")
            return False, e.stderr
    
    def create_backup(self):
        """Create backup of application"""
        self.log("Creating backup...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = Path(f"/tmp/backup_{timestamp}")
        
        try:
            shutil.copytree(self.app_dir, self.backup_dir)
            self.log(f"✓ Backup created: {self.backup_dir}")
            return True
        except Exception as e:
            self.log(f"✗ Backup failed: {e}", "ERROR")
            return False
    
    def rollback(self):
        """Rollback to backup"""
        if not self.backup_dir or not self.backup_dir.exists():
            self.log("No backup available for rollback", "ERROR")
            return False
        
        self.log("Rolling back to backup...")
        
        try:
            # Remove current
            shutil.rmtree(self.app_dir)
            # Restore backup
            shutil.copytree(self.backup_dir, self.app_dir)
            self.log("✓ Rollback completed")
            return True
        except Exception as e:
            self.log(f"✗ Rollback failed: {e}", "ERROR")
            return False
    
    def deploy(self):
        """Run full deployment"""
        self.log("=" * 60)
        self.log("STARTING DEPLOYMENT")
        self.log("=" * 60)
        
        # Create backup
        if not self.create_backup():
            return False
        
        # Pull latest code
        success, output = self.run_command(
            "git pull origin main",
            "Pulling latest code"
        )
        if not success:
            self.rollback()
            return False
        
        # Install dependencies
        success, output = self.run_command(
            "pip install -r requirements.txt",
            "Installing dependencies"
        )
        if not success:
            self.rollback()
            return False
        
        # Run migrations (example)
        success, output = self.run_command(
            "python manage.py migrate",
            "Running database migrations"
        )
        if not success:
            self.rollback()
            return False
        
        # Restart service
        success, output = self.run_command(
            f"systemctl restart {self.service_name}",
            f"Restarting {self.service_name}"
        )
        if not success:
            self.rollback()
            return False
        
        # Verify service
        success, output = self.run_command(
            f"systemctl is-active {self.service_name}",
            f"Verifying {self.service_name}"
        )
        if not success:
            self.rollback()
            return False
        
        self.log("=" * 60)
        self.log("✓ DEPLOYMENT SUCCESSFUL")
        self.log("=" * 60)
        
        # Save log
        log_file = f"deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(log_file, 'w') as f:
            f.write('\n'.join(self.log_entries))
        
        return True

# Usage example (commented as it requires real git repo and service)
# deployer = DeploymentManager('/path/to/app', 'myapp.service')
# success = deployer.deploy()
# exit(0 if success else 1)
```
</details>

---

## Part 7: Real-World Scenario

### Scenario: Complete System Administration Tool

Create `sysadmin_tool.py`:

```python
#!/usr/bin/env python3
"""
System Administration Tool
Combines os, subprocess, and file operations for system management
"""

import os
import subprocess
import shutil
import argparse
from pathlib import Path
from datetime import datetime

class SysAdminTool:
    """System administration utilities"""
    
    def system_info(self):
        """Display system information"""
        print("\n" + "=" * 60)
        print("SYSTEM INFORMATION")
        print("=" * 60)
        
        # Basic info
        print(f"Hostname: {os.uname().nodename}")
        print(f"OS: {os.uname().sysname} {os.uname().release}")
        print(f"CPU Count: {os.cpu_count()}")
        
        # Load average
        try:
            load = os.getloadavg()
            print(f"Load Average: {load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}")
        except AttributeError:
            print("Load Average: N/A")
        
        # Disk usage
        usage = shutil.disk_usage('/')
        total_gb = usage.total / (1024**3)
        used_gb = usage.used / (1024**3)
        free_gb = usage.free / (1024**3)
        percent = (usage.used / usage.total) * 100
        
        print(f"\nDisk Usage:")
        print(f"  Total: {total_gb:.2f} GB")
        print(f"  Used: {used_gb:.2f} GB ({percent:.1f}%)")
        print(f"  Free: {free_gb:.2f} GB")
    
    def backup_directory(self, source, dest):
        """Backup directory"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{Path(source).name}_{timestamp}"
        backup_path = Path(dest) / backup_name
        
        print(f"\nBacking up {source} to {backup_path}")
        
        try:
            shutil.make_archive(
                str(backup_path),
                'gztar',
                source
            )
            
            archive = f"{backup_path}.tar.gz"
            size = os.path.getsize(archive) / (1024**2)
            
            print(f"✓ Backup created: {archive}")
            print(f"  Size: {size:.2f} MB")
            return True
        
        except Exception as e:
            print(f"✗ Backup failed: {e}")
            return False
    
    def cleanup_temp(self):
        """Clean up temporary files"""
        temp_dirs = ['/tmp', os.path.expanduser('~/.cache')]
        
        print("\nCleaning temporary files...")
        
        for temp_dir in temp_dirs:
            if not os.path.exists(temp_dir):
                continue
            
            print(f"\nChecking: {temp_dir}")
            
            try:
                # Count files older than 7 days
                count = 0
                size = 0
                
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        filepath = os.path.join(root, file)
                        try:
                            age_days = (datetime.now().timestamp() - 
                                      os.path.getmtime(filepath)) / (24*3600)
                            
                            if age_days > 7:
                                file_size = os.path.getsize(filepath)
                                count += 1
                                size += file_size
                        except Exception:
                            pass
                
                print(f"  Found {count} files ({size/(1024**2):.2f} MB)")
                
            except PermissionError:
                print(f"  Permission denied")
    
    def check_services(self, services):
        """Check service status"""
        print("\n" + "=" * 60)
        print("SERVICE STATUS")
        print("=" * 60)
        
        for service in services:
            try:
                result = subprocess.run(
                    ['systemctl', 'is-active', service],
                    capture_output=True,
                    text=True
                )
                
                status = result.stdout.strip()
                symbol = "✓" if status == "active" else "✗"
                print(f"{symbol} {service}: {status}")
                
            except FileNotFoundError:
                print(f"  {service}: systemctl not available")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='System Administration Tool'
    )
    
    parser.add_argument(
        'command',
        choices=['info', 'backup', 'cleanup', 'services'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--source',
        help='Source directory for backup'
    )
    
    parser.add_argument(
        '--dest',
        default='/tmp/backups',
        help='Destination for backups'
    )
    
    parser.add_argument(
        '--services',
        nargs='+',
        default=['ssh', 'cron'],
        help='Services to check'
    )
    
    args = parser.parse_args()
    tool = SysAdminTool()
    
    if args.command == 'info':
        tool.system_info()
    
    elif args.command == 'backup':
        if not args.source:
            print("Error: --source required for backup")
            return 1
        tool.backup_directory(args.source, args.dest)
    
    elif args.command == 'cleanup':
        tool.cleanup_temp()
    
    elif args.command == 'services':
        tool.check_services(args.services)
    
    return 0

if __name__ == "__main__":
    exit(main())
```

**Usage:**
```bash
# System information
python sysadmin_tool.py info

# Backup directory
python sysadmin_tool.py backup --source /etc/nginx --dest /backups

# Cleanup temp files
python sysadmin_tool.py cleanup

# Check services
python sysadmin_tool.py services --services nginx mysql redis
```

---

## What You Learned

In this lab, you learned:

✅ **OS Module**
- Environment variable management
- System information gathering
- Directory operations
- Path manipulation
- File metadata and permissions

✅ **Shutil Module**
- Copying and moving files
- Directory tree operations
- Creating archives
- Disk usage monitoring

✅ **Subprocess Module**
- Running shell commands
- Capturing command output
- Handling command errors
- Timeouts and background processes
- Piping commands together

✅ **Pathlib**
- Modern path handling
- Path properties and methods
- File system traversal
- Cross-platform compatibility

✅ **DevOps Applications**
- System monitoring scripts
- Automated backups
- Log rotation
- Service health checks
- Deployment automation
- System administration tools

---

## Next Steps

- Combine skills from all labs to build complete automation tools
- Explore Python libraries for cloud providers (boto3 for AWS)
- Learn about configuration management tools (Ansible, Terraform)
- Study CI/CD pipeline integration

## Additional Resources

- [Python os Module](https://docs.python.org/3/library/os.html)
- [Python subprocess](https://docs.python.org/3/library/subprocess.html)
- [Python shutil](https://docs.python.org/3/library/shutil.html)
- [Python pathlib](https://docs.python.org/3/library/pathlib.html)
- [System Administration with Python](https://python-for-system-administrators.readthedocs.io/)

---

## Congratulations!

You've completed all 6 foundational Python labs for DevOps! You now have the skills to:

- Write Python scripts for automation
- Process data and configuration files
- Implement error handling and logging
- Execute system commands
- Build complete automation tools

Continue practicing and building real-world automation projects!
