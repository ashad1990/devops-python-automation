# DevOps Automation Scripts

This directory contains practical Python scripts demonstrating DevOps automation concepts and best practices. Each script is production-ready, well-documented, and follows Python best practices (PEP 8).

## 📋 Table of Contents

1. [Health Check](#1-health_checkpy)
2. [Log Analyzer](#2-log_analyzerpy)
3. [Config Parser](#3-config_parserpy)
4. [Backup Script](#4-backup_scriptpy)
5. [Deploy Helper](#5-deploy_helperpy)
6. [System Monitor](#6-system_monitorpy)
7. [API Client](#7-api_clientpy)
8. [File Organizer](#8-file_organizerpy)
9. [Docker Cleanup](#9-docker_cleanuppy)
10. [Environment Checker](#10-env_checkerpy)

## 🚀 Quick Start

### Prerequisites

```bash
# Install Python dependencies
pip install -r ../requirements.txt

# Make scripts executable (Linux/Mac)
chmod +x *.py
```

### Common Dependencies

Most scripts require the following Python packages:
- `requests` - For HTTP operations
- `pyyaml` - For YAML parsing
- `psutil` - For system monitoring

---

## 📝 Script Details

### 1. health_check.py

**Purpose**: Monitor the health of multiple HTTP/HTTPS endpoints with concurrent checks.

**Features**:
- Concurrent health checking using ThreadPoolExecutor
- Configurable timeout and thresholds
- Response time measurement
- Continuous monitoring mode
- Support for URL lists from files

**Usage**:

```bash
# Check specific URLs
./health_check.py https://example.com https://api.example.com

# Check URLs from a file
./health_check.py -f urls.txt

# Continuous monitoring every 30 seconds
./health_check.py -f urls.txt --interval 30

# Custom timeout and workers
./health_check.py https://example.com -t 20 -w 10
```

**Example Output**:
```
✓ https://example.com - UP (200) - 145.32ms
⚠ https://api.example.com - DEGRADED (404) - 89.15ms

HEALTH CHECK SUMMARY
====================================================================
Total Endpoints: 2
UP: 1 (50.0%)
DEGRADED: 1 (50.0%)
DOWN: 0 (0.0%)
Average Response Time (UP): 145.32ms
```

---

### 2. log_analyzer.py

**Purpose**: Parse and analyze log files to extract errors, warnings, and generate statistics.

**Features**:
- Pattern-based error detection
- Log level categorization
- Common error pattern recognition (timeouts, OOM, permissions, etc.)
- Statistical analysis
- Export results to file

**Usage**:

```bash
# Analyze a log file
./log_analyzer.py /var/log/application.log

# Show detailed error messages
./log_analyzer.py application.log -d

# Show top 20 patterns
./log_analyzer.py application.log -n 20

# Export analysis to file
./log_analyzer.py application.log -o analysis_report.txt
```

**Example Output**:
```
LOG ANALYSIS REPORT
======================================================================
Total Lines Processed: 10,245
Time Range: 2024-01-01 00:00:00 to 2024-01-01 23:59:59

LOG LEVELS DISTRIBUTION
----------------------------------------------------------------------
ERROR           1,234 ( 12.0%)
WARNING         2,345 ( 22.9%)
INFO            6,666 ( 65.1%)

TOP ERROR PATTERNS
----------------------------------------------------------------------
Connection refused            145
Timeout                       89
Database error                34
HTTP 5xx                      23
```

---

### 3. config_parser.py

**Purpose**: Parse, validate, and manipulate YAML configuration files.

**Features**:
- Safe YAML parsing
- Dot-notation key access
- Required key validation
- Type validation
- Configuration merging
- JSON export capability
- Sensitive value masking

**Usage**:

```bash
# Parse and display configuration
./config_parser.py config.yaml

# Get specific value
./config_parser.py config.yaml -g database.host

# Validate required keys
./config_parser.py config.yaml -r database.host database.port api.key

# Convert to JSON
./config_parser.py config.yaml -o config.json -f json

# Show sensitive values
./config_parser.py config.yaml --show-sensitive
```

**Example YAML**:
```yaml
database:
  host: localhost
  port: 5432
  username: admin
  password: secret123

api:
  url: https://api.example.com
  key: abc123xyz
```

---

### 4. backup_script.py

**Purpose**: Create compressed backups with automatic rotation.

**Features**:
- Tar/gzip compression
- Automatic rotation based on retention policy
- Backup verification
- Restore functionality
- Backup listing with metadata
- Dry-run mode

**Usage**:

```bash
# Create a backup
./backup_script.py -s /path/to/source -d /backups

# Custom backup name
./backup_script.py -s /data/app -d /backups -n myapp

# Set retention to 14 days
./backup_script.py -s /data -d /backups -r 14

# List all backups
./backup_script.py -d /backups --list

# Restore a backup
./backup_script.py --restore /backups/myapp_20240101_120000.tar.gz --restore-to /restore/path

# Verify backup integrity
./backup_script.py --verify /backups/myapp_20240101_120000.tar.gz

# Rotate old backups
./backup_script.py -d /backups --rotate
```

---

### 5. deploy_helper.py

**Purpose**: Automate deployment tasks with pre/post checks and rollback capability.

**Features**:
- Pre-deployment validation
- Git integration
- Dependency management
- Post-deployment verification
- Rollback functionality
- Dry-run mode
- Detailed logging

**Usage**:

```bash
# Deploy to staging
./deploy_helper.py staging

# Deploy to production
./deploy_helper.py production

# Dry run (simulate deployment)
./deploy_helper.py production --dry-run

# Skip pre-deployment checks
./deploy_helper.py staging --skip-checks

# Rollback to previous version
./deploy_helper.py production --rollback
```

**Example Output**:
```
============================================================
PRE-DEPLOYMENT CHECKS
============================================================
[SUCCESS] Checking Git status...
[SUCCESS] Git working directory clean
[INFO] Current branch: main
[SUCCESS] Dependencies check passed
[SUCCESS] Environment validated: production

============================================================
STARTING DEPLOYMENT TO PRODUCTION
============================================================
[SUCCESS] Pulling latest changes...
[SUCCESS] Installing/updating dependencies...
[SUCCESS] Running tests...
[SUCCESS] Deployment completed successfully
```

---

### 6. system_monitor.py

**Purpose**: Monitor system resources (CPU, memory, disk, network).

**Features**:
- Real-time resource monitoring
- Configurable alerting thresholds
- Per-CPU usage tracking
- Process monitoring (top CPU/memory consumers)
- Continuous monitoring mode
- Network statistics

**Usage**:

```bash
# Single system check
./system_monitor.py

# Show top processes
./system_monitor.py --processes

# Continuous monitoring every 10 seconds
./system_monitor.py --interval 10 --processes

# Custom thresholds
./system_monitor.py --cpu-threshold 90 --memory-threshold 85 --disk-threshold 90
```

**Example Output**:
```
SYSTEM MONITORING REPORT
================================================================================
Timestamp: 2024-01-01 12:00:00

CPU USAGE
--------------------------------------------------------------------------------
Usage: 45.2%
Physical Cores: 4
Logical Cores: 8
Frequency: 2400.00 MHz

MEMORY USAGE
--------------------------------------------------------------------------------
Usage: 67.3%
Total: 16.00 GB
Used: 10.77 GB
Available: 5.23 GB

TOP PROCESSES BY CPU
--------------------------------------------------------------------------------
PID      Name                      User            CPU%
1234     python3                   user            25.3
5678     chrome                    user            15.8
```

---

### 7. api_client.py

**Purpose**: Reusable REST API client with retry logic and error handling.

**Features**:
- Support for all HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Automatic retry with exponential backoff
- Bearer token authentication
- Custom headers
- Timeout configuration
- Health check capability
- JSON request/response handling

**Usage**:

```bash
# GET request
./api_client.py https://api.example.com -e /users

# POST request with JSON data
./api_client.py https://api.example.com -m POST -e /users -d '{"name":"John","email":"john@example.com"}'

# With API key authentication
./api_client.py https://api.example.com -e /protected --api-key your_api_key

# Custom headers
./api_client.py https://api.example.com -e /data -H "X-Custom-Header: value"

# Health check
./api_client.py https://api.example.com --health-check

# PUT request with timeout
./api_client.py https://api.example.com -m PUT -e /users/123 -d '{"name":"Jane"}' -t 60
```

---

### 8. file_organizer.py

**Purpose**: Organize files into categorized directories.

**Features**:
- Organization by file type (images, documents, code, etc.)
- Organization by modification date
- Organization by file size
- Automatic duplicate handling
- Empty directory cleanup
- Dry-run mode

**Usage**:

```bash
# Organize by file type
./file_organizer.py /path/to/messy/folder

# Organize by date (YYYY/MM structure)
./file_organizer.py /downloads -m date

# Organize by size
./file_organizer.py /downloads -m size

# Dry run (preview without moving)
./file_organizer.py /downloads --dry-run

# Clean up empty directories after organization
./file_organizer.py /downloads --clean-empty
```

**File Type Categories**:
- Images: jpg, png, gif, svg, etc.
- Documents: pdf, doc, txt, md, etc.
- Code: py, java, js, cpp, etc.
- Videos: mp4, avi, mkv, etc.
- Audio: mp3, wav, flac, etc.
- Archives: zip, tar, gz, etc.
- And more...

---

### 9. docker_cleanup.py

**Purpose**: Clean up Docker resources to free disk space.

**Features**:
- Remove stopped containers
- Remove dangling/unused images
- Remove unused volumes
- Remove unused networks
- System-wide cleanup (prune)
- Disk usage reporting
- Dry-run mode

**Usage**:

```bash
# Show Docker disk usage
./docker_cleanup.py --disk-usage

# Remove stopped containers
./docker_cleanup.py --containers

# Remove dangling images
./docker_cleanup.py --images

# Remove all unused images
./docker_cleanup.py --all-images

# Remove unused volumes
./docker_cleanup.py --volumes

# Complete cleanup (prune everything)
./docker_cleanup.py --all --volumes

# Dry run
./docker_cleanup.py --all --dry-run
```

**Safety Note**: Always use `--dry-run` first to preview what will be removed!

---

### 10. env_checker.py

**Purpose**: Validate required environment variables and configurations.

**Features**:
- Required variable validation
- Optional variable checking
- Pattern validation (regex)
- Numeric range validation
- Choice validation
- URL and email validation
- Environment variable listing
- Sensitive value masking

**Usage**:

```bash
# Check required variables
./env_checker.py -r DATABASE_URL API_KEY SECRET_KEY

# Check required and optional variables
./env_checker.py -r DATABASE_URL -o DEBUG_MODE LOG_LEVEL

# List all environment variables
./env_checker.py --list

# Filter environment variables
./env_checker.py --list --filter "AWS|AZURE|GCP"

# Show values (with masking)
./env_checker.py -r DATABASE_URL --show-values

# Show values without masking
./env_checker.py -r DATABASE_URL --show-values --no-mask
```

**Example Use Case**:
```bash
# In CI/CD pipeline
./env_checker.py -r \
  DATABASE_URL \
  REDIS_URL \
  API_KEY \
  SECRET_KEY \
  AWS_ACCESS_KEY_ID \
  AWS_SECRET_ACCESS_KEY
```

---

## 🎯 Best Practices Demonstrated

All scripts demonstrate the following DevOps and Python best practices:

### Code Quality
- ✅ PEP 8 compliant formatting
- ✅ Comprehensive docstrings
- ✅ Type hints where appropriate
- ✅ Proper error handling
- ✅ Logging instead of print statements

### DevOps Principles
- ✅ Command-line interface with argparse
- ✅ Exit codes (0 for success, 1 for errors)
- ✅ Dry-run/simulation modes
- ✅ Verbose/debug logging options
- ✅ Configuration file support
- ✅ Idempotent operations

### Reliability
- ✅ Input validation
- ✅ Exception handling
- ✅ Timeout configuration
- ✅ Retry mechanisms
- ✅ Graceful degradation

### Security
- ✅ No hardcoded credentials
- ✅ Sensitive data masking
- ✅ Environment variable usage
- ✅ Safe file operations

---

## 🔧 Common Patterns

### Running in Dry-Run Mode

Most scripts support `--dry-run` to preview actions:

```bash
./backup_script.py -s /data -d /backups --dry-run
./deploy_helper.py production --dry-run
./file_organizer.py /downloads --dry-run
./docker_cleanup.py --all --dry-run
```

### Verbose Logging

Enable detailed logging with `-v` or `--verbose`:

```bash
./health_check.py urls.txt -v
./log_analyzer.py app.log -v
./system_monitor.py -v
```

### Continuous Monitoring

Scripts that support continuous operation with `--interval`:

```bash
./health_check.py urls.txt --interval 60
./system_monitor.py --interval 30 --processes
```

---

## 🐛 Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`, install dependencies:

```bash
pip install requests pyyaml psutil
```

### Permission Errors

Make scripts executable:

```bash
chmod +x *.py
```

### Docker Not Found

For `docker_cleanup.py`, ensure Docker is installed and running:

```bash
docker --version
docker ps
```

---

## 📚 Learning Resources

These scripts cover important DevOps concepts:

1. **Monitoring & Observability**: `health_check.py`, `system_monitor.py`, `log_analyzer.py`
2. **Configuration Management**: `config_parser.py`, `env_checker.py`
3. **Backup & Recovery**: `backup_script.py`
4. **Deployment Automation**: `deploy_helper.py`
5. **Infrastructure Management**: `docker_cleanup.py`, `file_organizer.py`
6. **API Integration**: `api_client.py`

---

## 🤝 Contributing

When adding new scripts to this collection:

1. Follow the existing code structure and style
2. Include comprehensive docstrings
3. Add argparse CLI with `--help` text
4. Implement `--dry-run` for destructive operations
5. Use proper logging (not print statements)
6. Handle errors gracefully
7. Update this README with usage examples

---

## 📄 License

These scripts are provided as educational examples for DevOps automation. Feel free to modify and use them in your projects.

---

## ⚡ Quick Reference

| Script | Primary Use Case | Key Feature |
|--------|-----------------|-------------|
| health_check.py | API/Service monitoring | Concurrent checks |
| log_analyzer.py | Log analysis | Pattern detection |
| config_parser.py | Config management | YAML validation |
| backup_script.py | Data backup | Auto-rotation |
| deploy_helper.py | Deployment | Pre/post checks |
| system_monitor.py | Resource monitoring | Real-time stats |
| api_client.py | API testing | Retry logic |
| file_organizer.py | File management | Auto-categorization |
| docker_cleanup.py | Docker maintenance | Space recovery |
| env_checker.py | Environment validation | Var checking |

---

**Happy Automating! 🚀**
