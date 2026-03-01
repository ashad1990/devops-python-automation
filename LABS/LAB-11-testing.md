# LAB 11: Testing DevOps Python Code

## Learning Objectives
By the end of this lab, you will be able to:
- Write unit tests using pytest
- Implement test fixtures and parametrization
- Mock external dependencies and APIs
- Practice test-driven development (TDD)
- Test DevOps automation scripts
- Measure code coverage
- Implement integration tests
- Apply testing best practices for DevOps code

## Prerequisites
- Python 3.8+ installed
- Understanding of functions and classes
- Basic knowledge of DevOps automation concepts

## Setup

### Install Testing Dependencies

```bash
# Install pytest and related packages
pip install pytest pytest-cov pytest-mock requests-mock

# Verify installation
pytest --version
```

---

## Part 1: Introduction to pytest

### Exercise 1.1: Basic Unit Tests

Create `test_basics.py`:

```python
"""Basic pytest examples."""


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract b from a."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


# Test functions
def test_add():
    """Test addition."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    """Test subtraction."""
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    assert subtract(0, 0) == 0


def test_multiply():
    """Test multiplication."""
    assert multiply(3, 4) == 12
    assert multiply(-2, 5) == -10
    assert multiply(0, 100) == 0


def test_divide():
    """Test division."""
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    """Test that dividing by zero raises ValueError."""
    import pytest
    
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    
    assert "Cannot divide by zero" in str(exc_info.value)


# Run tests with: pytest test_basics.py -v
```

**Run the tests:**
```bash
pytest test_basics.py -v
```

**Expected Output:**
```
test_basics.py::test_add PASSED
test_basics.py::test_subtract PASSED
test_basics.py::test_multiply PASSED
test_basics.py::test_divide PASSED
test_basics.py::test_divide_by_zero PASSED

====== 5 passed in 0.02s ======
```

### Exercise 1.2: Parametrized Tests

Create `test_parametrized.py`:

```python
"""Parametrized test examples."""
import pytest


def is_valid_ip(ip_address):
    """Check if string is a valid IPv4 address."""
    parts = ip_address.split('.')
    
    if len(parts) != 4:
        return False
    
    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False
        except ValueError:
            return False
    
    return True


def is_valid_port(port):
    """Check if port number is valid."""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except (ValueError, TypeError):
        return False


# Parametrized tests
@pytest.mark.parametrize("ip_address,expected", [
    ("192.168.1.1", True),
    ("10.0.0.1", True),
    ("255.255.255.255", True),
    ("0.0.0.0", True),
    ("256.1.1.1", False),
    ("192.168.1", False),
    ("192.168.1.1.1", False),
    ("abc.def.ghi.jkl", False),
    ("", False),
])
def test_is_valid_ip(ip_address, expected):
    """Test IP address validation with multiple inputs."""
    assert is_valid_ip(ip_address) == expected


@pytest.mark.parametrize("port,expected", [
    (80, True),
    (443, True),
    (8080, True),
    (65535, True),
    (1, True),
    (0, False),
    (65536, False),
    (-1, False),
    ("abc", False),
    (None, False),
])
def test_is_valid_port(port, expected):
    """Test port validation with multiple inputs."""
    assert is_valid_port(port) == expected


# Run with: pytest test_parametrized.py -v
```

---

## Part 2: Testing DevOps Scripts

### Exercise 2.1: Testing File Operations

Create `file_utils.py`:

```python
"""File utility functions for DevOps."""
import os
import json
import yaml


def read_config_file(filepath):
    """Read configuration file (JSON or YAML)."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        if filepath.endswith('.json'):
            return json.load(f)
        elif filepath.endswith(('.yml', '.yaml')):
            return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported file format. Use .json or .yaml")


def write_config_file(filepath, data):
    """Write configuration to file."""
    with open(filepath, 'w') as f:
        if filepath.endswith('.json'):
            json.dump(data, f, indent=2)
        elif filepath.endswith(('.yml', '.yaml')):
            yaml.dump(data, f, default_flow_style=False)
        else:
            raise ValueError("Unsupported file format. Use .json or .yaml")


def backup_file(filepath):
    """Create a backup of a file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    backup_path = f"{filepath}.bak"
    
    with open(filepath, 'r') as src:
        with open(backup_path, 'w') as dst:
            dst.write(src.read())
    
    return backup_path
```

Create `test_file_utils.py`:

```python
"""Tests for file_utils module."""
import pytest
import os
import json
import tempfile
from file_utils import read_config_file, write_config_file, backup_file


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_config():
    """Sample configuration data."""
    return {
        'server': {
            'host': '0.0.0.0',
            'port': 8080
        },
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'testdb'
        }
    }


def test_read_json_config(temp_dir, sample_config):
    """Test reading JSON configuration file."""
    config_file = os.path.join(temp_dir, 'config.json')
    
    # Write test config
    with open(config_file, 'w') as f:
        json.dump(sample_config, f)
    
    # Read and verify
    result = read_config_file(config_file)
    assert result == sample_config


def test_read_yaml_config(temp_dir, sample_config):
    """Test reading YAML configuration file."""
    import yaml
    
    config_file = os.path.join(temp_dir, 'config.yaml')
    
    # Write test config
    with open(config_file, 'w') as f:
        yaml.dump(sample_config, f)
    
    # Read and verify
    result = read_config_file(config_file)
    assert result == sample_config


def test_read_nonexistent_file():
    """Test reading a file that doesn't exist."""
    with pytest.raises(FileNotFoundError) as exc_info:
        read_config_file('/nonexistent/file.json')
    
    assert "Config file not found" in str(exc_info.value)


def test_read_unsupported_format(temp_dir):
    """Test reading unsupported file format."""
    config_file = os.path.join(temp_dir, 'config.txt')
    
    with open(config_file, 'w') as f:
        f.write("some text")
    
    with pytest.raises(ValueError) as exc_info:
        read_config_file(config_file)
    
    assert "Unsupported file format" in str(exc_info.value)


def test_write_json_config(temp_dir, sample_config):
    """Test writing JSON configuration file."""
    config_file = os.path.join(temp_dir, 'config.json')
    
    write_config_file(config_file, sample_config)
    
    # Verify file was created and contains correct data
    assert os.path.exists(config_file)
    
    with open(config_file, 'r') as f:
        result = json.load(f)
    
    assert result == sample_config


def test_write_yaml_config(temp_dir, sample_config):
    """Test writing YAML configuration file."""
    import yaml
    
    config_file = os.path.join(temp_dir, 'config.yaml')
    
    write_config_file(config_file, sample_config)
    
    # Verify file was created and contains correct data
    assert os.path.exists(config_file)
    
    with open(config_file, 'r') as f:
        result = yaml.safe_load(f)
    
    assert result == sample_config


def test_backup_file(temp_dir):
    """Test file backup creation."""
    original_file = os.path.join(temp_dir, 'test.txt')
    
    # Create original file
    content = "Important data"
    with open(original_file, 'w') as f:
        f.write(content)
    
    # Create backup
    backup_path = backup_file(original_file)
    
    # Verify backup exists and has same content
    assert os.path.exists(backup_path)
    assert backup_path == f"{original_file}.bak"
    
    with open(backup_path, 'r') as f:
        backup_content = f.read()
    
    assert backup_content == content


def test_backup_nonexistent_file():
    """Test backing up a file that doesn't exist."""
    with pytest.raises(FileNotFoundError):
        backup_file('/nonexistent/file.txt')
```

### Exercise 2.2: Testing Server Management Functions

Create `server_manager.py`:

```python
"""Server management functions."""


class Server:
    """Represent a server."""
    
    def __init__(self, hostname, ip_address, port=22):
        self.hostname = hostname
        self.ip_address = ip_address
        self.port = port
        self.status = "stopped"
        self.services = []
    
    def start(self):
        """Start the server."""
        if self.status == "running":
            raise RuntimeError("Server is already running")
        self.status = "running"
        return True
    
    def stop(self):
        """Stop the server."""
        if self.status == "stopped":
            raise RuntimeError("Server is already stopped")
        self.status = "stopped"
        return True
    
    def restart(self):
        """Restart the server."""
        if self.status == "running":
            self.stop()
        self.start()
        return True
    
    def add_service(self, service_name):
        """Add a service to the server."""
        if service_name in self.services:
            raise ValueError(f"Service '{service_name}' already exists")
        self.services.append(service_name)
    
    def remove_service(self, service_name):
        """Remove a service from the server."""
        if service_name not in self.services:
            raise ValueError(f"Service '{service_name}' not found")
        self.services.remove(service_name)
    
    def get_info(self):
        """Get server information."""
        return {
            'hostname': self.hostname,
            'ip_address': self.ip_address,
            'port': self.port,
            'status': self.status,
            'services': self.services
        }


class ServerManager:
    """Manage multiple servers."""
    
    def __init__(self):
        self.servers = {}
    
    def add_server(self, server):
        """Add a server to management."""
        if server.hostname in self.servers:
            raise ValueError(f"Server '{server.hostname}' already exists")
        self.servers[server.hostname] = server
    
    def remove_server(self, hostname):
        """Remove a server from management."""
        if hostname not in self.servers:
            raise ValueError(f"Server '{hostname}' not found")
        del self.servers[hostname]
    
    def get_server(self, hostname):
        """Get a server by hostname."""
        if hostname not in self.servers:
            raise ValueError(f"Server '{hostname}' not found")
        return self.servers[hostname]
    
    def list_servers(self, status=None):
        """List all servers, optionally filtered by status."""
        if status is None:
            return list(self.servers.values())
        return [s for s in self.servers.values() if s.status == status]
    
    def start_all(self):
        """Start all stopped servers."""
        started = []
        for server in self.servers.values():
            if server.status == "stopped":
                server.start()
                started.append(server.hostname)
        return started
    
    def stop_all(self):
        """Stop all running servers."""
        stopped = []
        for server in self.servers.values():
            if server.status == "running":
                server.stop()
                stopped.append(server.hostname)
        return stopped
```

Create `test_server_manager.py`:

```python
"""Tests for server_manager module."""
import pytest
from server_manager import Server, ServerManager


class TestServer:
    """Test Server class."""
    
    @pytest.fixture
    def server(self):
        """Create a test server."""
        return Server("web-01", "192.168.1.10", port=22)
    
    def test_server_initialization(self, server):
        """Test server is initialized correctly."""
        assert server.hostname == "web-01"
        assert server.ip_address == "192.168.1.10"
        assert server.port == 22
        assert server.status == "stopped"
        assert server.services == []
    
    def test_server_start(self, server):
        """Test starting a server."""
        result = server.start()
        assert result is True
        assert server.status == "running"
    
    def test_server_start_already_running(self, server):
        """Test starting a server that's already running."""
        server.start()
        
        with pytest.raises(RuntimeError) as exc_info:
            server.start()
        
        assert "already running" in str(exc_info.value)
    
    def test_server_stop(self, server):
        """Test stopping a server."""
        server.start()
        result = server.stop()
        
        assert result is True
        assert server.status == "stopped"
    
    def test_server_stop_already_stopped(self, server):
        """Test stopping a server that's already stopped."""
        with pytest.raises(RuntimeError) as exc_info:
            server.stop()
        
        assert "already stopped" in str(exc_info.value)
    
    def test_server_restart(self, server):
        """Test restarting a server."""
        server.start()
        result = server.restart()
        
        assert result is True
        assert server.status == "running"
    
    def test_add_service(self, server):
        """Test adding a service."""
        server.add_service("nginx")
        assert "nginx" in server.services
    
    def test_add_duplicate_service(self, server):
        """Test adding a duplicate service."""
        server.add_service("nginx")
        
        with pytest.raises(ValueError) as exc_info:
            server.add_service("nginx")
        
        assert "already exists" in str(exc_info.value)
    
    def test_remove_service(self, server):
        """Test removing a service."""
        server.add_service("nginx")
        server.remove_service("nginx")
        
        assert "nginx" not in server.services
    
    def test_remove_nonexistent_service(self, server):
        """Test removing a service that doesn't exist."""
        with pytest.raises(ValueError) as exc_info:
            server.remove_service("nginx")
        
        assert "not found" in str(exc_info.value)
    
    def test_get_info(self, server):
        """Test getting server information."""
        server.start()
        server.add_service("nginx")
        
        info = server.get_info()
        
        assert info['hostname'] == "web-01"
        assert info['ip_address'] == "192.168.1.10"
        assert info['status'] == "running"
        assert "nginx" in info['services']


class TestServerManager:
    """Test ServerManager class."""
    
    @pytest.fixture
    def manager(self):
        """Create a test server manager."""
        return ServerManager()
    
    @pytest.fixture
    def servers(self):
        """Create test servers."""
        return [
            Server("web-01", "192.168.1.10"),
            Server("web-02", "192.168.1.11"),
            Server("db-01", "192.168.1.20")
        ]
    
    def test_add_server(self, manager, servers):
        """Test adding a server."""
        manager.add_server(servers[0])
        
        assert "web-01" in manager.servers
        assert manager.servers["web-01"] == servers[0]
    
    def test_add_duplicate_server(self, manager, servers):
        """Test adding a duplicate server."""
        manager.add_server(servers[0])
        
        with pytest.raises(ValueError) as exc_info:
            manager.add_server(servers[0])
        
        assert "already exists" in str(exc_info.value)
    
    def test_remove_server(self, manager, servers):
        """Test removing a server."""
        manager.add_server(servers[0])
        manager.remove_server("web-01")
        
        assert "web-01" not in manager.servers
    
    def test_remove_nonexistent_server(self, manager):
        """Test removing a server that doesn't exist."""
        with pytest.raises(ValueError) as exc_info:
            manager.remove_server("web-01")
        
        assert "not found" in str(exc_info.value)
    
    def test_get_server(self, manager, servers):
        """Test getting a server."""
        manager.add_server(servers[0])
        server = manager.get_server("web-01")
        
        assert server == servers[0]
    
    def test_list_all_servers(self, manager, servers):
        """Test listing all servers."""
        for server in servers:
            manager.add_server(server)
        
        all_servers = manager.list_servers()
        
        assert len(all_servers) == 3
    
    def test_list_servers_by_status(self, manager, servers):
        """Test listing servers filtered by status."""
        for server in servers:
            manager.add_server(server)
        
        # Start some servers
        servers[0].start()
        servers[1].start()
        
        running = manager.list_servers(status="running")
        stopped = manager.list_servers(status="stopped")
        
        assert len(running) == 2
        assert len(stopped) == 1
    
    def test_start_all(self, manager, servers):
        """Test starting all servers."""
        for server in servers:
            manager.add_server(server)
        
        started = manager.start_all()
        
        assert len(started) == 3
        assert all(s.status == "running" for s in servers)
    
    def test_stop_all(self, manager, servers):
        """Test stopping all servers."""
        for server in servers:
            manager.add_server(server)
            server.start()
        
        stopped = manager.stop_all()
        
        assert len(stopped) == 3
        assert all(s.status == "stopped" for s in servers)
```

---

## Part 3: Mocking External Dependencies

### Exercise 3.1: Mocking API Calls

Create `api_client.py`:

```python
"""API client for DevOps services."""
import requests


class GitHubClient:
    """Client for GitHub API."""
    
    def __init__(self, token=None):
        self.base_url = "https://api.github.com"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
    
    def get_repository(self, owner, repo):
        """Get repository information."""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def list_issues(self, owner, repo, state='open'):
        """List repository issues."""
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {'state': state}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_issue(self, owner, repo, title, body=None):
        """Create a new issue."""
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        data = {'title': title}
        if body:
            data['body'] = body
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()


class JenkinsClient:
    """Client for Jenkins API."""
    
    def __init__(self, base_url, username, api_token):
        self.base_url = base_url.rstrip('/')
        self.auth = (username, api_token)
    
    def get_job(self, job_name):
        """Get job information."""
        url = f"{self.base_url}/job/{job_name}/api/json"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def build_job(self, job_name, parameters=None):
        """Trigger a job build."""
        if parameters:
            url = f"{self.base_url}/job/{job_name}/buildWithParameters"
            response = requests.post(url, auth=self.auth, data=parameters)
        else:
            url = f"{self.base_url}/job/{job_name}/build"
            response = requests.post(url, auth=self.auth)
        
        return response.status_code == 201
```

Create `test_api_client.py`:

```python
"""Tests for api_client module using mocking."""
import pytest
import requests
from unittest.mock import Mock, patch
from api_client import GitHubClient, JenkinsClient


class TestGitHubClient:
    """Test GitHub API client with mocked responses."""
    
    @pytest.fixture
    def github_client(self):
        """Create a GitHub client."""
        return GitHubClient(token="fake-token")
    
    @patch('api_client.requests.get')
    def test_get_repository(self, mock_get, github_client):
        """Test getting repository information."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'name': 'test-repo',
            'full_name': 'owner/test-repo',
            'stargazers_count': 100,
            'forks_count': 50
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Make API call
        result = github_client.get_repository('owner', 'test-repo')
        
        # Verify
        assert result['name'] == 'test-repo'
        assert result['stargazers_count'] == 100
        
        # Verify requests.get was called correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert 'https://api.github.com/repos/owner/test-repo' in str(call_args)
    
    @patch('api_client.requests.get')
    def test_list_issues(self, mock_get, github_client):
        """Test listing issues."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = [
            {'number': 1, 'title': 'Bug fix', 'state': 'open'},
            {'number': 2, 'title': 'Feature request', 'state': 'open'}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Make API call
        result = github_client.list_issues('owner', 'test-repo')
        
        # Verify
        assert len(result) == 2
        assert result[0]['title'] == 'Bug fix'
    
    @patch('api_client.requests.post')
    def test_create_issue(self, mock_post, github_client):
        """Test creating an issue."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'number': 123,
            'title': 'New bug',
            'state': 'open'
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # Make API call
        result = github_client.create_issue(
            'owner',
            'test-repo',
            'New bug',
            'Bug description'
        )
        
        # Verify
        assert result['number'] == 123
        assert result['title'] == 'New bug'
        
        # Verify POST was called with correct data
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args.kwargs['json']['title'] == 'New bug'
    
    @patch('api_client.requests.get')
    def test_api_error_handling(self, mock_get, github_client):
        """Test handling API errors."""
        # Setup mock to raise an exception
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        # Verify exception is raised
        with pytest.raises(requests.exceptions.HTTPError):
            github_client.get_repository('owner', 'nonexistent')


class TestJenkinsClient:
    """Test Jenkins API client with mocked responses."""
    
    @pytest.fixture
    def jenkins_client(self):
        """Create a Jenkins client."""
        return JenkinsClient(
            'http://jenkins.example.com',
            'admin',
            'fake-token'
        )
    
    @patch('api_client.requests.get')
    def test_get_job(self, mock_get, jenkins_client):
        """Test getting job information."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'name': 'test-job',
            'buildable': True,
            'lastBuild': {'number': 42}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Make API call
        result = jenkins_client.get_job('test-job')
        
        # Verify
        assert result['name'] == 'test-job'
        assert result['buildable'] is True
    
    @patch('api_client.requests.post')
    def test_build_job(self, mock_post, jenkins_client):
        """Test triggering a job build."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        # Make API call
        result = jenkins_client.build_job('test-job')
        
        # Verify
        assert result is True
        mock_post.assert_called_once()
    
    @patch('api_client.requests.post')
    def test_build_job_with_parameters(self, mock_post, jenkins_client):
        """Test triggering a parameterized build."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        # Make API call
        parameters = {'branch': 'main', 'environment': 'production'}
        result = jenkins_client.build_job('test-job', parameters)
        
        # Verify
        assert result is True
        call_args = mock_post.call_args
        assert call_args.kwargs['data'] == parameters
```

---

## Part 4: Test-Driven Development (TDD)

### Exercise 4.1: TDD Example - Log Parser

Create `test_log_parser.py` (write tests first):

```python
"""Tests for log parser (TDD approach)."""
import pytest
from datetime import datetime


# Tests written BEFORE implementation
class TestLogParser:
    """Test log parser functionality."""
    
    def test_parse_apache_log_line(self):
        """Test parsing a single Apache log line."""
        from log_parser import parse_apache_log
        
        log_line = '192.168.1.1 - - [01/Jan/2024:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234'
        
        result = parse_apache_log(log_line)
        
        assert result['ip'] == '192.168.1.1'
        assert result['method'] == 'GET'
        assert result['path'] == '/index.html'
        assert result['status'] == 200
        assert result['size'] == 1234
    
    def test_parse_error_log_returns_none(self):
        """Test that invalid log lines return None."""
        from log_parser import parse_apache_log
        
        invalid_line = "This is not a valid log line"
        result = parse_apache_log(invalid_line)
        
        assert result is None
    
    def test_count_status_codes(self):
        """Test counting HTTP status codes."""
        from log_parser import count_status_codes
        
        logs = [
            {'status': 200},
            {'status': 200},
            {'status': 404},
            {'status': 500},
            {'status': 200}
        ]
        
        result = count_status_codes(logs)
        
        assert result[200] == 3
        assert result[404] == 1
        assert result[500] == 1
    
    def test_get_top_ips(self):
        """Test getting top IP addresses."""
        from log_parser import get_top_ips
        
        logs = [
            {'ip': '192.168.1.1'},
            {'ip': '192.168.1.2'},
            {'ip': '192.168.1.1'},
            {'ip': '192.168.1.3'},
            {'ip': '192.168.1.1'}
        ]
        
        result = get_top_ips(logs, n=2)
        
        assert len(result) == 2
        assert result[0] == ('192.168.1.1', 3)
        assert result[1] == ('192.168.1.2', 1)
```

Now create `log_parser.py` (implementation):

```python
"""Log parser implementation (following TDD)."""
import re
from collections import Counter
from typing import Dict, List, Tuple, Optional


def parse_apache_log(log_line: str) -> Optional[Dict]:
    """
    Parse an Apache access log line.
    
    Args:
        log_line: Apache log line string
        
    Returns:
        Dictionary with parsed fields or None if invalid
    """
    # Apache log format pattern
    pattern = r'(\S+) \S+ \S+ \[(.*?)\] "(\S+) (\S+) \S+" (\d+) (\d+)'
    
    match = re.match(pattern, log_line)
    
    if not match:
        return None
    
    ip, timestamp, method, path, status, size = match.groups()
    
    return {
        'ip': ip,
        'timestamp': timestamp,
        'method': method,
        'path': path,
        'status': int(status),
        'size': int(size)
    }


def count_status_codes(logs: List[Dict]) -> Dict[int, int]:
    """
    Count occurrences of each HTTP status code.
    
    Args:
        logs: List of parsed log entries
        
    Returns:
        Dictionary mapping status codes to counts
    """
    status_codes = [log['status'] for log in logs]
    return dict(Counter(status_codes))


def get_top_ips(logs: List[Dict], n: int = 10) -> List[Tuple[str, int]]:
    """
    Get top N IP addresses by request count.
    
    Args:
        logs: List of parsed log entries
        n: Number of top IPs to return
        
    Returns:
        List of (ip, count) tuples, sorted by count descending
    """
    ips = [log['ip'] for log in logs]
    counter = Counter(ips)
    return counter.most_common(n)


def analyze_logs(log_file: str) -> Dict:
    """
    Analyze a log file and return statistics.
    
    Args:
        log_file: Path to log file
        
    Returns:
        Dictionary with analysis results
    """
    logs = []
    
    with open(log_file, 'r') as f:
        for line in f:
            parsed = parse_apache_log(line.strip())
            if parsed:
                logs.append(parsed)
    
    return {
        'total_requests': len(logs),
        'status_codes': count_status_codes(logs),
        'top_ips': get_top_ips(logs, n=10),
        'unique_ips': len(set(log['ip'] for log in logs))
    }


# Run tests to verify implementation
# pytest test_log_parser.py -v
```

---

## Part 5: Code Coverage

### Exercise 5.1: Measuring Test Coverage

Create `.coveragerc`:

```ini
[run]
source = .
omit = 
    */tests/*
    */test_*.py
    */__pycache__/*
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

**Run tests with coverage:**

```bash
# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html  # On macOS
# or
xdg-open htmlcov/index.html  # On Linux
```

**Example output:**
```
---------- coverage: platform linux, python 3.9.7 ----------
Name                    Stmts   Miss  Cover
-------------------------------------------
file_utils.py              45      2    96%
server_manager.py          78      3    96%
api_client.py              32      0   100%
log_parser.py              41      1    98%
-------------------------------------------
TOTAL                     196      6    97%
```

---

## Practice Challenges

### Challenge 1: Test a Deployment Script
Write comprehensive tests for a deployment automation script that:
- Validates configuration files
- Checks server connectivity
- Deploys applications
- Verifies deployment success

### Challenge 2: Mock Complex Workflows
Create tests for a CI/CD pipeline script that:
- Mocks Git operations
- Mocks Docker builds
- Mocks Kubernetes deployments
- Tests error scenarios

### Challenge 3: TDD - Build a Monitoring System
Use TDD to build a monitoring system that:
- Checks service health
- Collects metrics
- Sends alerts
- Generates reports

### Challenge 4: Integration Tests
Write integration tests for:
- Database connections
- API integrations
- File system operations
- External service calls

---

## What You Learned

In this lab, you learned:

✅ **pytest Fundamentals**
- Writing basic test functions
- Using assertions effectively
- Running tests and interpreting results
- Organizing test files

✅ **Test Fixtures**
- Creating reusable test fixtures
- Using pytest's built-in fixtures
- Fixture scope and lifecycle
- Parametrized tests

✅ **Testing DevOps Code**
- Testing file operations
- Testing server management functions
- Testing configuration handling
- Testing error conditions

✅ **Mocking**
- Mocking external API calls
- Using unittest.mock
- Mocking HTTP requests
- Testing error scenarios

✅ **Test-Driven Development**
- Writing tests before code
- Red-Green-Refactor cycle
- Benefits of TDD approach
- Designing testable code

✅ **Code Coverage**
- Measuring test coverage
- Interpreting coverage reports
- Identifying untested code
- Improving test coverage

✅ **Best Practices**
- Organizing test files
- Naming conventions
- Test isolation
- Continuous testing

## Next Steps

- Learn about integration testing
- Explore property-based testing with Hypothesis
- Study mutation testing
- Implement continuous testing in CI/CD
- Learn about contract testing for APIs

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Test-Driven Development with Python](https://www.obeythetestinggoat.com/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Testing Best Practices](https://realpython.com/pytest-python-testing/)
