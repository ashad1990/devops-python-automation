# LAB 07: API Requests and REST Integration

## Learning Objectives
By the end of this lab, you will be able to:
- Use the `requests` library to interact with REST APIs
- Handle different HTTP methods (GET, POST, PUT, DELETE)
- Implement API authentication (Basic Auth, Bearer tokens, API keys)
- Handle API pagination and rate limiting
- Implement proper error handling for API calls
- Parse and work with JSON responses
- Build automation scripts that integrate with common DevOps APIs

## Prerequisites
- Python 3.8+ installed
- Basic understanding of HTTP and REST APIs
- Understanding of JSON data format

## Setup

Install required packages:

```bash
pip install requests
```

---

## Part 1: Basic API Requests

### Exercise 1.1: Making GET Requests

Create a file called `github_api.py` to fetch repository information:

```python
import requests
import json


def get_repository_info(owner, repo):
    """Fetch GitHub repository information."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        
        repo_data = response.json()
        
        print(f"Repository: {repo_data['full_name']}")
        print(f"Description: {repo_data['description']}")
        print(f"Stars: {repo_data['stargazers_count']}")
        print(f"Forks: {repo_data['forks_count']}")
        print(f"Language: {repo_data['language']}")
        print(f"Open Issues: {repo_data['open_issues_count']}")
        
        return repo_data
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Error connecting to GitHub API")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    
    return None


if __name__ == "__main__":
    get_repository_info("kubernetes", "kubernetes")
```

**Expected Output:**
```
Repository: kubernetes/kubernetes
Description: Production-Grade Container Scheduling and Management
Stars: 108000
Forks: 39000
Language: Go
Open Issues: 2500
```

### Exercise 1.2: Working with Query Parameters

Create `api_params.py` to search GitHub repositories:

```python
import requests


def search_repositories(query, language=None, sort='stars', max_results=5):
    """Search GitHub repositories with filters."""
    url = "https://api.github.com/search/repositories"
    
    # Build query string
    search_query = query
    if language:
        search_query += f" language:{language}"
    
    params = {
        'q': search_query,
        'sort': sort,
        'order': 'desc',
        'per_page': max_results
    }
    
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"\nFound {data['total_count']} repositories")
        print(f"\nTop {max_results} results:\n")
        
        for idx, repo in enumerate(data['items'], 1):
            print(f"{idx}. {repo['full_name']}")
            print(f"   ⭐ Stars: {repo['stargazers_count']:,}")
            print(f"   📝 {repo['description'][:80] if repo['description'] else 'No description'}")
            print()
        
        return data['items']
        
    except requests.exceptions.RequestException as e:
        print(f"Error searching repositories: {e}")
        return []


if __name__ == "__main__":
    # Search for Python DevOps tools
    search_repositories("devops automation", language="python", max_results=5)
```

---

## Part 2: Authentication

### Exercise 2.1: API Key Authentication

Create `jenkins_api.py` for Jenkins API authentication:

```python
import requests
import os
from urllib.parse import urljoin


class JenkinsAPI:
    """Jenkins API client with authentication."""
    
    def __init__(self, base_url, username, api_token):
        self.base_url = base_url.rstrip('/')
        self.auth = (username, api_token)
        self.session = requests.Session()
        self.session.auth = self.auth
    
    def get_jobs(self):
        """Get list of all Jenkins jobs."""
        url = urljoin(self.base_url, '/api/json')
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('jobs', [])
            
            print(f"\nFound {len(jobs)} Jenkins jobs:\n")
            for job in jobs:
                print(f"- {job['name']}")
                print(f"  URL: {job['url']}")
                print(f"  Color: {job['color']}")
                print()
            
            return jobs
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs: {e}")
            return []
    
    def get_job_status(self, job_name):
        """Get status of a specific job."""
        url = urljoin(self.base_url, f'/job/{job_name}/api/json')
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            print(f"\nJob: {data['name']}")
            print(f"URL: {data['url']}")
            print(f"Buildable: {data['buildable']}")
            
            if 'lastBuild' in data and data['lastBuild']:
                last_build = data['lastBuild']['number']
                print(f"Last Build: #{last_build}")
            
            if 'healthReport' in data and data['healthReport']:
                score = data['healthReport'][0].get('score', 'N/A')
                print(f"Health Score: {score}%")
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching job status: {e}")
            return None
    
    def trigger_build(self, job_name, parameters=None):
        """Trigger a Jenkins build."""
        if parameters:
            url = urljoin(self.base_url, f'/job/{job_name}/buildWithParameters')
            response = self.session.post(url, data=parameters, timeout=10)
        else:
            url = urljoin(self.base_url, f'/job/{job_name}/build')
            response = self.session.post(url, timeout=10)
        
        if response.status_code == 201:
            print(f"Build triggered successfully for {job_name}")
            return True
        else:
            print(f"Failed to trigger build: {response.status_code}")
            return False


# Example usage (with environment variables for security)
if __name__ == "__main__":
    # Use environment variables for credentials
    JENKINS_URL = os.getenv('JENKINS_URL', 'http://localhost:8080')
    JENKINS_USER = os.getenv('JENKINS_USER', 'admin')
    JENKINS_TOKEN = os.getenv('JENKINS_TOKEN', 'your-api-token')
    
    jenkins = JenkinsAPI(JENKINS_URL, JENKINS_USER, JENKINS_TOKEN)
    
    # Get all jobs
    # jenkins.get_jobs()
    
    # Get specific job status
    # jenkins.get_job_status('my-pipeline')
    
    print("Jenkins API client ready. Configure JENKINS_URL, JENKINS_USER, and JENKINS_TOKEN environment variables.")
```

### Exercise 2.2: Bearer Token Authentication

Create `github_token_auth.py`:

```python
import requests
import os


class GitHubAPI:
    """GitHub API client with token authentication."""
    
    def __init__(self, token):
        self.base_url = "https://api.github.com"
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_authenticated_user(self):
        """Get information about the authenticated user."""
        url = f"{self.base_url}/user"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        user = response.json()
        print(f"\nAuthenticated as: {user['login']}")
        print(f"Name: {user['name']}")
        print(f"Public Repos: {user['public_repos']}")
        print(f"Followers: {user['followers']}")
        
        return user
    
    def create_repository(self, name, description="", private=False):
        """Create a new GitHub repository."""
        url = f"{self.base_url}/user/repos"
        
        data = {
            'name': name,
            'description': description,
            'private': private,
            'auto_init': True
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            repo = response.json()
            print(f"\n✓ Repository created: {repo['full_name']}")
            print(f"  URL: {repo['html_url']}")
            print(f"  Clone URL: {repo['clone_url']}")
            
            return repo
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422:
                print(f"✗ Repository '{name}' already exists")
            else:
                print(f"✗ Error creating repository: {e}")
            return None
    
    def list_user_repos(self, username, repo_type='all'):
        """List repositories for a user."""
        url = f"{self.base_url}/users/{username}/repos"
        
        params = {
            'type': repo_type,
            'sort': 'updated',
            'per_page': 10
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        repos = response.json()
        
        print(f"\n{username}'s repositories ({repo_type}):\n")
        for repo in repos:
            print(f"📦 {repo['name']}")
            print(f"   ⭐ {repo['stargazers_count']} stars | "
                  f"🍴 {repo['forks_count']} forks | "
                  f"Updated: {repo['updated_at'][:10]}")
            if repo['description']:
                print(f"   {repo['description'][:100]}")
            print()
        
        return repos


if __name__ == "__main__":
    # Get token from environment variable
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        print("Please set GITHUB_TOKEN environment variable")
        print("export GITHUB_TOKEN='your-github-personal-access-token'")
    else:
        api = GitHubAPI(token)
        # api.get_authenticated_user()
        # api.list_user_repos('torvalds')
        print("GitHub API client ready.")
```

---

## Part 3: Pagination

### Exercise 3.1: Handling Paginated Responses

Create `github_pagination.py`:

```python
import requests
from typing import List, Dict


def get_all_repos(username: str) -> List[Dict]:
    """Fetch all repositories for a user using pagination."""
    base_url = "https://api.github.com"
    all_repos = []
    page = 1
    per_page = 30  # GitHub's default
    
    while True:
        url = f"{base_url}/users/{username}/repos"
        params = {
            'page': page,
            'per_page': per_page,
            'sort': 'updated'
        }
        
        print(f"Fetching page {page}...", end=' ')
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            repos = response.json()
            
            if not repos:
                print("(no more results)")
                break
            
            print(f"(got {len(repos)} repos)")
            all_repos.extend(repos)
            
            # Check if there are more pages using Link header
            if 'Link' in response.headers:
                links = response.headers['Link']
                if 'rel="next"' not in links:
                    break
            else:
                # No Link header means this is the last page
                break
            
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"\nError fetching repositories: {e}")
            break
    
    print(f"\nTotal repositories fetched: {len(all_repos)}")
    return all_repos


def get_paginated_results(url: str, params: dict = None, max_pages: int = 10):
    """Generic pagination handler for REST APIs."""
    all_results = []
    page = 1
    
    if params is None:
        params = {}
    
    while page <= max_pages:
        params['page'] = page
        params['per_page'] = params.get('per_page', 100)
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            
            # Handle both list and dict responses
            if isinstance(results, list):
                if not results:
                    break
                all_results.extend(results)
            elif isinstance(results, dict) and 'items' in results:
                items = results['items']
                if not items:
                    break
                all_results.extend(items)
                # Check if we've got all results
                total = results.get('total_count', 0)
                if len(all_results) >= total:
                    break
            else:
                break
            
            # Check for next page in Link header
            if 'Link' in response.headers:
                links = response.headers['Link']
                if 'rel="next"' not in links:
                    break
            else:
                break
            
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"Error during pagination: {e}")
            break
    
    return all_results


if __name__ == "__main__":
    # Example: Get all repos for a user
    repos = get_all_repos("kubernetes")
    
    if repos:
        print(f"\nTop 5 most recently updated repositories:")
        for i, repo in enumerate(repos[:5], 1):
            print(f"{i}. {repo['name']} (updated: {repo['updated_at'][:10]})")
```

---

## Part 4: Error Handling and Retries

### Exercise 4.1: Robust API Client with Retry Logic

Create `robust_api_client.py`:

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
from functools import wraps


def retry_on_failure(max_retries=3, backoff_factor=1):
    """Decorator for retrying failed API calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = backoff_factor * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed: {e}")
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator


class RobustAPIClient:
    """API client with retry logic and proper error handling."""
    
    def __init__(self, base_url, timeout=10, max_retries=3):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def get(self, endpoint, params=None, headers=None):
        """Make a GET request with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.ConnectionError:
            print(f"Failed to connect to {url}")
        except requests.exceptions.Timeout:
            print(f"Request to {url} timed out after {self.timeout}s")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        
        return None
    
    def post(self, endpoint, data=None, json_data=None, headers=None):
        """Make a POST request with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.post(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json() if response.text else {}
            
        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        
        return None
    
    def _handle_http_error(self, error):
        """Handle HTTP errors with appropriate messages."""
        status_code = error.response.status_code
        
        error_messages = {
            400: "Bad Request - Invalid parameters",
            401: "Unauthorized - Check your credentials",
            403: "Forbidden - Insufficient permissions",
            404: "Not Found - Resource doesn't exist",
            429: "Rate Limited - Too many requests",
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable"
        }
        
        message = error_messages.get(status_code, f"HTTP {status_code} error")
        print(f"✗ {message}")
        
        # Try to get error details from response
        try:
            error_detail = error.response.json()
            if 'message' in error_detail:
                print(f"  Details: {error_detail['message']}")
        except:
            pass


# Example usage
if __name__ == "__main__":
    # GitHub API client
    github_client = RobustAPIClient("https://api.github.com")
    
    # This will automatically retry on failure
    repo_data = github_client.get("/repos/docker/docker")
    
    if repo_data:
        print(f"\n✓ Repository: {repo_data['full_name']}")
        print(f"  Stars: {repo_data['stargazers_count']:,}")
        print(f"  Language: {repo_data['language']}")
```

---

## Part 5: Rate Limiting

### Exercise 5.1: Handling API Rate Limits

Create `rate_limiter.py`:

```python
import requests
import time
from datetime import datetime


class RateLimitedAPI:
    """API client that respects rate limits."""
    
    def __init__(self, base_url, calls_per_minute=60):
        self.base_url = base_url
        self.calls_per_minute = calls_per_minute
        self.min_interval = 60.0 / calls_per_minute
        self.last_call_time = 0
    
    def _wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        
        if time_since_last_call < self.min_interval:
            sleep_time = self.min_interval - time_since_last_call
            print(f"⏱️  Rate limiting: waiting {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_call_time = time.time()
    
    def get(self, endpoint, **kwargs):
        """Make a rate-limited GET request."""
        self._wait_if_needed()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, **kwargs)
        
        # Check GitHub rate limit headers
        if 'X-RateLimit-Remaining' in response.headers:
            remaining = response.headers['X-RateLimit-Remaining']
            limit = response.headers['X-RateLimit-Limit']
            reset_time = int(response.headers['X-RateLimit-Reset'])
            
            print(f"📊 Rate limit: {remaining}/{limit} remaining")
            
            if int(remaining) < 10:
                reset_dt = datetime.fromtimestamp(reset_time)
                print(f"⚠️  Low on API calls! Resets at {reset_dt}")
        
        response.raise_for_status()
        return response.json()


def check_github_rate_limit(token=None):
    """Check current GitHub API rate limit status."""
    url = "https://api.github.com/rate_limit"
    
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    print("\n📊 GitHub API Rate Limit Status\n")
    
    for resource, limits in data['resources'].items():
        remaining = limits['remaining']
        limit = limits['limit']
        reset_time = datetime.fromtimestamp(limits['reset'])
        
        print(f"{resource}:")
        print(f"  Limit: {limit}")
        print(f"  Remaining: {remaining}")
        print(f"  Resets at: {reset_time}")
        
        if remaining < limit * 0.1:  # Less than 10% remaining
            print(f"  ⚠️  WARNING: Low on API calls!")
        print()


if __name__ == "__main__":
    # Check rate limit
    check_github_rate_limit()
    
    # Example of rate-limited requests
    api = RateLimitedAPI("https://api.github.com", calls_per_minute=30)
    
    repos_to_check = ["docker/docker", "kubernetes/kubernetes", "ansible/ansible"]
    
    for repo in repos_to_check:
        print(f"\nFetching {repo}...")
        data = api.get(f"/repos/{repo}")
        print(f"✓ {data['full_name']}: {data['stargazers_count']:,} stars")
```

---

## Part 6: Real-World DevOps Integration

### Exercise 6.1: CI/CD Pipeline Monitor

Create `pipeline_monitor.py`:

```python
import requests
import time
import os
from datetime import datetime


class PipelineMonitor:
    """Monitor CI/CD pipelines across different platforms."""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
    
    def check_github_actions(self, owner, repo, workflow_id=None):
        """Check GitHub Actions workflow runs."""
        base_url = "https://api.github.com"
        
        if workflow_id:
            url = f"{base_url}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"
        else:
            url = f"{base_url}/repos/{owner}/{repo}/actions/runs"
        
        headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
        
        params = {'per_page': 10}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            runs = data['workflow_runs']
            
            print(f"\n{'='*70}")
            print(f"GitHub Actions Status for {owner}/{repo}")
            print(f"{'='*70}\n")
            
            for run in runs[:5]:
                status_emoji = {
                    'completed': '✓',
                    'in_progress': '⏳',
                    'queued': '⏸️'
                }.get(run['status'], '❓')
                
                conclusion_emoji = {
                    'success': '✅',
                    'failure': '❌',
                    'cancelled': '⛔'
                }.get(run.get('conclusion', ''), '❓')
                
                created = datetime.strptime(
                    run['created_at'], 
                    '%Y-%m-%dT%H:%M:%SZ'
                )
                
                print(f"{status_emoji} {run['name']}")
                print(f"   Status: {run['status']} {conclusion_emoji}")
                print(f"   Branch: {run['head_branch']}")
                print(f"   Commit: {run['head_sha'][:7]}")
                print(f"   Started: {created.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   URL: {run['html_url']}")
                print()
            
            return runs
            
        except requests.exceptions.RequestException as e:
            print(f"Error checking GitHub Actions: {e}")
            return []
    
    def wait_for_workflow(self, owner, repo, run_id, max_wait=600, interval=30):
        """Wait for a workflow run to complete."""
        base_url = "https://api.github.com"
        url = f"{base_url}/repos/{owner}/{repo}/actions/runs/{run_id}"
        
        headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
        
        start_time = time.time()
        
        print(f"\n⏳ Waiting for workflow run {run_id} to complete...")
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                run = response.json()
                status = run['status']
                
                if status == 'completed':
                    conclusion = run['conclusion']
                    elapsed = time.time() - start_time
                    
                    print(f"\n✓ Workflow completed in {elapsed:.0f}s")
                    print(f"  Conclusion: {conclusion}")
                    
                    if conclusion == 'success':
                        print("  ✅ SUCCESS")
                        return True
                    else:
                        print(f"  ❌ {conclusion.upper()}")
                        return False
                else:
                    print(f"  Status: {status}... (checking again in {interval}s)")
                    time.sleep(interval)
                    
            except requests.exceptions.RequestException as e:
                print(f"Error checking workflow: {e}")
                time.sleep(interval)
        
        print(f"\n⚠️  Timeout: Workflow did not complete in {max_wait}s")
        return False


if __name__ == "__main__":
    monitor = PipelineMonitor()
    
    # Example: Monitor GitHub Actions
    monitor.check_github_actions("docker", "docker-py")
    
    # Example: Wait for a specific workflow
    # monitor.wait_for_workflow("owner", "repo", 123456789)
```

---

## Practice Challenges

### Challenge 1: Multi-Service Health Checker
Create a script that checks the health of multiple services (APIs, databases, web servers) and reports their status.

```python
# health_checker.py
import requests
import concurrent.futures
from typing import Dict, List


def check_service_health(service: Dict) -> Dict:
    """Check if a service is healthy."""
    # Implement health check logic
    # Return service status with response time
    pass


def check_all_services(services: List[Dict]) -> List[Dict]:
    """Check all services concurrently."""
    # Use ThreadPoolExecutor for concurrent checks
    pass


if __name__ == "__main__":
    services = [
        {'name': 'API Gateway', 'url': 'https://api.example.com/health'},
        {'name': 'Database', 'url': 'https://db.example.com/ping'},
        # Add more services
    ]
    
    results = check_all_services(services)
    # Print formatted report
```

### Challenge 2: Automated Deployment Trigger
Create a script that triggers deployments when certain conditions are met (e.g., all tests pass, specific branch is updated).

**Requirements:**
- Check GitHub for new commits
- Verify CI status
- Trigger deployment via API
- Send notifications

### Challenge 3: API Data Aggregator
Build a tool that fetches data from multiple DevOps tools (GitHub, Jenkins, Jira) and creates a unified dashboard report.

**Requirements:**
- Fetch from at least 3 different APIs
- Handle different authentication methods
- Aggregate and format data
- Export to JSON/CSV

### Challenge 4: Rate-Limited Bulk Operations
Create a script that performs bulk operations (e.g., updating multiple repositories) while respecting API rate limits.

**Requirements:**
- Process multiple items
- Handle pagination
- Respect rate limits
- Implement exponential backoff
- Log progress and errors

---

## What You Learned

In this lab, you learned:

✅ **Making API Requests**
- Using the `requests` library for HTTP operations
- Working with different HTTP methods (GET, POST, PUT, DELETE)
- Passing query parameters and headers
- Parsing JSON responses

✅ **Authentication**
- Implementing Basic Authentication
- Using Bearer token authentication
- API key authentication
- Securing credentials with environment variables

✅ **Pagination**
- Handling paginated API responses
- Using Link headers for navigation
- Implementing generic pagination logic
- Fetching all pages of data

✅ **Error Handling**
- Catching and handling HTTP errors
- Implementing retry logic
- Using exponential backoff
- Handling network timeouts and failures

✅ **Rate Limiting**
- Respecting API rate limits
- Implementing rate limiting logic
- Checking rate limit status
- Handling rate limit exceeded errors

✅ **DevOps Integration**
- Interacting with GitHub API
- Monitoring CI/CD pipelines
- Automating DevOps workflows
- Building robust API clients

## Next Steps

- Explore the documentation for APIs you use daily (GitHub, GitLab, Jenkins, etc.)
- Build custom integrations for your DevOps workflows
- Practice error handling and retry strategies
- Learn about webhooks for event-driven automation
- Investigate GraphQL APIs as an alternative to REST

## Additional Resources

- [Requests Documentation](https://docs.python-requests.org/)
- [GitHub REST API](https://docs.github.com/en/rest)
- [HTTP Status Codes](https://httpstatuses.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [API Authentication Methods](https://swagger.io/docs/specification/authentication/)
