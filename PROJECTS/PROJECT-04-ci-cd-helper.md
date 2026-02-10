# PROJECT 04: CI/CD Helper CLI Tool

## Problem Statement (User Story)
**As a DevOps engineer**, I need a Python CLI tool that automates common CI/CD tasks including creating GitHub repos, managing branches, triggering deployments, and generating changelogs, so that I can standardize workflows, reduce manual errors, and accelerate software delivery cycles.

## Project Objectives
- Build a comprehensive CI/CD automation CLI tool
- Integrate with GitHub API for repository management
- Automate git workflows (branching, tagging, merging)
- Implement deployment triggers for CI/CD pipelines
- Generate automated changelogs and release notes
- Create a reusable tool demonstrating DevOps automation skills

## Requirements

### Functional Requirements
1. **GitHub Repository Management**
   - Create new repositories with templates
   - Configure repository settings (branch protection, webhooks)
   - Manage collaborators and team permissions
   - Archive/delete repositories

2. **Branch Management**
   - Create feature/hotfix/release branches
   - Merge branches with pull request creation
   - Delete merged branches
   - Enforce branch naming conventions
   - List and filter branches

3. **Deployment Automation**
   - Trigger GitHub Actions workflows
   - Monitor deployment status
   - Promote releases between environments
   - Rollback deployments
   - Integration with CI/CD platforms (Jenkins, CircleCI, GitLab CI)

4. **Release Management**
   - Generate changelogs from commits/PRs
   - Create GitHub releases
   - Semantic versioning support
   - Tag management
   - Release notes templating

5. **Pipeline Utilities**
   - Validate CI/CD configuration files
   - Check build/test status
   - Generate pipeline reports
   - Manage pipeline secrets/variables

### Non-Functional Requirements
- **Performance**: API calls with rate limit handling
- **Reliability**: Retry logic for network failures
- **Security**: Secure token management
- **Usability**: Intuitive commands with helpful docs
- **Extensibility**: Plugin architecture for custom tasks

## Technical Specification

### Features List
- [ ] GitHub authentication (token, OAuth)
- [ ] Repository creation with templates
- [ ] Branch creation and management
- [ ] Pull request automation
- [ ] GitHub Actions workflow triggers
- [ ] Deployment status monitoring
- [ ] Changelog generation (conventional commits)
- [ ] Semantic versioning automation
- [ ] Release creation and publishing
- [ ] Branch protection rules
- [ ] Webhook management
- [ ] CI/CD config validation
- [ ] Pipeline status dashboard
- [ ] Multi-repository operations
- [ ] Interactive mode

### Suggested Architecture

```
ci-cd-helper/
├── src/
│   ├── __init__.py
│   ├── main.py                     # CLI entry point
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── repo.py                 # Repo commands
│   │   ├── branch.py               # Branch commands
│   │   ├── deploy.py               # Deployment commands
│   │   ├── release.py              # Release commands
│   │   └── pipeline.py             # Pipeline commands
│   ├── github/
│   │   ├── __init__.py
│   │   ├── client.py               # GitHub API client
│   │   ├── repos.py                # Repository operations
│   │   ├── branches.py             # Branch operations
│   │   ├── pulls.py                # Pull request ops
│   │   └── actions.py              # GitHub Actions ops
│   ├── changelog/
│   │   ├── __init__.py
│   │   ├── generator.py            # Changelog generator
│   │   ├── parser.py               # Commit parser
│   │   └── templates.py            # Templates
│   ├── versioning/
│   │   ├── __init__.py
│   │   └── semver.py               # Semantic versioning
│   ├── deploy/
│   │   ├── __init__.py
│   │   ├── base.py                 # Base deployer
│   │   ├── github_actions.py       # GitHub Actions
│   │   └── jenkins.py              # Jenkins integration
│   └── utils/
│       ├── __init__.py
│       ├── config.py               # Configuration
│       ├── logger.py               # Logging
│       └── validators.py           # Validation utils
├── templates/
│   ├── repo_templates/             # Repo templates
│   ├── changelog_templates/        # Changelog templates
│   └── release_templates/          # Release templates
├── tests/
│   ├── __init__.py
│   ├── test_github_client.py
│   ├── test_changelog.py
│   ├── test_versioning.py
│   └── fixtures/
├── config/
│   └── config.yaml
├── requirements.txt
├── setup.py
└── README.md
```

### Data Models

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

class BranchType(Enum):
    """Git branch types."""
    FEATURE = "feature"
    BUGFIX = "bugfix"
    HOTFIX = "hotfix"
    RELEASE = "release"
    MAIN = "main"
    DEVELOP = "develop"

class CommitType(Enum):
    """Conventional commit types."""
    FEAT = "feat"
    FIX = "fix"
    DOCS = "docs"
    STYLE = "style"
    REFACTOR = "refactor"
    PERF = "perf"
    TEST = "test"
    CHORE = "chore"
    BREAKING = "BREAKING CHANGE"

class DeploymentStatus(Enum):
    """Deployment status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"

@dataclass
class Repository:
    """GitHub repository."""
    name: str
    owner: str
    description: str = ""
    private: bool = False
    default_branch: str = "main"
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        """Get full repository name."""
        return f"{self.owner}/{self.name}"

@dataclass
class Branch:
    """Git branch."""
    name: str
    branch_type: BranchType
    base_branch: str = "main"
    protected: bool = False
    sha: Optional[str] = None
    
    def get_full_name(self) -> str:
        """Get full branch name with prefix."""
        if self.branch_type in [BranchType.MAIN, BranchType.DEVELOP]:
            return self.name
        return f"{self.branch_type.value}/{self.name}"

@dataclass
class Commit:
    """Git commit."""
    sha: str
    message: str
    author: str
    timestamp: datetime
    commit_type: Optional[CommitType] = None
    scope: Optional[str] = None
    breaking: bool = False
    
    def parse_conventional_commit(self) -> bool:
        """
        Parse conventional commit format.
        
        Format: <type>(<scope>): <subject>
        """
        import re
        
        pattern = r'^(feat|fix|docs|style|refactor|perf|test|chore)(\([\w-]+\))?(!)?:\s*(.+)$'
        match = re.match(pattern, self.message.split('\n')[0])
        
        if match:
            self.commit_type = CommitType(match.group(1))
            self.scope = match.group(2)[1:-1] if match.group(2) else None
            self.breaking = match.group(3) == '!'
            return True
        
        return False

@dataclass
class Release:
    """Software release."""
    version: str
    tag_name: str
    name: str
    body: str
    draft: bool = False
    prerelease: bool = False
    created_at: Optional[datetime] = None
    commits: List[Commit] = field(default_factory=list)
    
    def get_changelog(self) -> str:
        """Generate changelog from commits."""
        sections = {
            CommitType.FEAT: "Features",
            CommitType.FIX: "Bug Fixes",
            CommitType.DOCS: "Documentation",
            CommitType.PERF: "Performance",
            CommitType.BREAKING: "BREAKING CHANGES"
        }
        
        changelog = [f"# {self.version}\n"]
        
        for commit_type, section_name in sections.items():
            commits = [c for c in self.commits if c.commit_type == commit_type]
            
            if commits:
                changelog.append(f"\n## {section_name}\n")
                for commit in commits:
                    scope = f"**{commit.scope}**: " if commit.scope else ""
                    changelog.append(f"* {scope}{commit.message.split(chr(10))[0]}")
        
        return "\n".join(changelog)

@dataclass
class Deployment:
    """Deployment information."""
    id: str
    environment: str
    status: DeploymentStatus
    ref: str  # Branch, tag, or SHA
    creator: str
    created_at: datetime
    updated_at: datetime
    url: Optional[str] = None
    log_url: Optional[str] = None
```

## Implementation Guidelines

### Milestone 1: GitHub API Integration (Week 1)
**Deliverables:**
- GitHub API client with authentication
- Repository CRUD operations
- Rate limit handling
- Error handling and retries

**Key Code Example:**
```python
from typing import Dict, Any, Optional, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

logger = logging.getLogger(__name__)

class GitHubClient:
    """GitHub API client."""
    
    def __init__(self, token: str, base_url: str = "https://api.github.com"):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub personal access token
            base_url: GitHub API base URL
        """
        self.token = token
        self.base_url = base_url
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic."""
        session = requests.Session()
        
        # Setup retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        # Set headers
        session.headers.update({
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        })
        
        return session
    
    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make API request with error handling.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request parameters
            
        Returns:
            Response JSON
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Check rate limit
            remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            if remaining < 100:
                logger.warning(f"GitHub API rate limit low: {remaining} remaining")
            
            response.raise_for_status()
            
            return response.json() if response.content else {}
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.error(f"Resource not found: {endpoint}")
            elif e.response.status_code == 403:
                logger.error("GitHub API rate limit exceeded or forbidden")
            else:
                logger.error(f"GitHub API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """GET request."""
        return self._request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """POST request."""
        return self._request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """PUT request."""
        return self._request("PUT", endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """PATCH request."""
        return self._request("PATCH", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> None:
        """DELETE request."""
        self._request("DELETE", endpoint, **kwargs)


class RepositoryManager:
    """Manage GitHub repositories."""
    
    def __init__(self, client: GitHubClient):
        self.client = client
    
    def create_repository(
        self,
        name: str,
        description: str = "",
        private: bool = False,
        auto_init: bool = True,
        gitignore_template: Optional[str] = None
    ) -> Repository:
        """
        Create a new GitHub repository.
        
        Args:
            name: Repository name
            description: Repository description
            private: Whether repository is private
            auto_init: Initialize with README
            gitignore_template: .gitignore template (e.g., 'Python')
            
        Returns:
            Created repository
        """
        logger.info(f"Creating repository: {name}")
        
        payload = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init
        }
        
        if gitignore_template:
            payload["gitignore_template"] = gitignore_template
        
        response = self.client.post("/user/repos", json=payload)
        
        return Repository(
            name=response["name"],
            owner=response["owner"]["login"],
            description=response["description"] or "",
            private=response["private"],
            default_branch=response["default_branch"],
            url=response["html_url"],
            created_at=datetime.fromisoformat(response["created_at"].rstrip('Z'))
        )
    
    def get_repository(self, owner: str, repo: str) -> Repository:
        """Get repository information."""
        response = self.client.get(f"/repos/{owner}/{repo}")
        
        return Repository(
            name=response["name"],
            owner=response["owner"]["login"],
            description=response["description"] or "",
            private=response["private"],
            default_branch=response["default_branch"],
            url=response["html_url"],
            created_at=datetime.fromisoformat(response["created_at"].rstrip('Z'))
        )
    
    def delete_repository(self, owner: str, repo: str) -> None:
        """Delete a repository."""
        logger.warning(f"Deleting repository: {owner}/{repo}")
        self.client.delete(f"/repos/{owner}/{repo}")
        logger.info("Repository deleted")
    
    def setup_branch_protection(
        self,
        owner: str,
        repo: str,
        branch: str,
        require_reviews: bool = True,
        required_approvals: int = 1,
        require_status_checks: bool = True,
        status_checks: Optional[List[str]] = None
    ) -> None:
        """
        Setup branch protection rules.
        
        Args:
            owner: Repository owner
            repo: Repository name
            branch: Branch name
            require_reviews: Require pull request reviews
            required_approvals: Number of required approvals
            require_status_checks: Require status checks
            status_checks: List of required status check names
        """
        logger.info(f"Setting up branch protection for {branch}")
        
        protection = {
            "required_status_checks": None,
            "enforce_admins": True,
            "required_pull_request_reviews": None,
            "restrictions": None
        }
        
        if require_status_checks and status_checks:
            protection["required_status_checks"] = {
                "strict": True,
                "contexts": status_checks
            }
        
        if require_reviews:
            protection["required_pull_request_reviews"] = {
                "required_approving_review_count": required_approvals,
                "dismiss_stale_reviews": True
            }
        
        self.client.put(
            f"/repos/{owner}/{repo}/branches/{branch}/protection",
            json=protection
        )
        
        logger.info("Branch protection configured")
```

### Milestone 2: Branch & PR Management (Week 2)
**Deliverables:**
- Branch creation with naming conventions
- Pull request automation
- Branch cleanup utilities
- Merge operations

**Key Code Example:**
```python
class BranchManager:
    """Manage Git branches."""
    
    def __init__(self, client: GitHubClient):
        self.client = client
    
    def create_branch(
        self,
        owner: str,
        repo: str,
        branch_name: str,
        base_branch: str = "main"
    ) -> Branch:
        """
        Create a new branch.
        
        Args:
            owner: Repository owner
            repo: Repository name
            branch_name: New branch name
            base_branch: Base branch to branch from
            
        Returns:
            Created branch
        """
        logger.info(f"Creating branch {branch_name} from {base_branch}")
        
        # Get base branch SHA
        base_ref = self.client.get(f"/repos/{owner}/{repo}/git/ref/heads/{base_branch}")
        base_sha = base_ref["object"]["sha"]
        
        # Create new branch
        self.client.post(
            f"/repos/{owner}/{repo}/git/refs",
            json={
                "ref": f"refs/heads/{branch_name}",
                "sha": base_sha
            }
        )
        
        return Branch(
            name=branch_name,
            branch_type=self._detect_branch_type(branch_name),
            base_branch=base_branch,
            sha=base_sha
        )
    
    def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        head: str,
        base: str,
        body: str = "",
        draft: bool = False
    ) -> Dict[str, Any]:
        """
        Create a pull request.
        
        Args:
            owner: Repository owner
            repo: Repository name
            title: PR title
            head: Head branch
            base: Base branch
            body: PR description
            draft: Create as draft PR
            
        Returns:
            Pull request data
        """
        logger.info(f"Creating PR: {head} → {base}")
        
        payload = {
            "title": title,
            "head": head,
            "base": base,
            "body": body,
            "draft": draft
        }
        
        pr = self.client.post(f"/repos/{owner}/{repo}/pulls", json=payload)
        
        logger.info(f"PR created: #{pr['number']}")
        return pr
    
    def merge_pull_request(
        self,
        owner: str,
        repo: str,
        pr_number: int,
        merge_method: str = "squash"
    ) -> None:
        """
        Merge a pull request.
        
        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: PR number
            merge_method: Merge method (merge, squash, rebase)
        """
        logger.info(f"Merging PR #{pr_number} using {merge_method}")
        
        self.client.put(
            f"/repos/{owner}/{repo}/pulls/{pr_number}/merge",
            json={"merge_method": merge_method}
        )
        
        logger.info("PR merged successfully")
    
    def delete_branch(self, owner: str, repo: str, branch: str) -> None:
        """Delete a branch."""
        logger.info(f"Deleting branch: {branch}")
        self.client.delete(f"/repos/{owner}/{repo}/git/refs/heads/{branch}")
    
    def cleanup_merged_branches(
        self,
        owner: str,
        repo: str,
        base_branch: str = "main"
    ) -> List[str]:
        """
        Delete branches that have been merged.
        
        Returns:
            List of deleted branch names
        """
        logger.info("Cleaning up merged branches...")
        
        # Get all branches
        branches = self.client.get(f"/repos/{owner}/{repo}/branches")
        
        deleted = []
        
        for branch in branches:
            branch_name = branch["name"]
            
            # Skip protected branches
            if branch_name in [base_branch, "develop"]:
                continue
            
            # Check if merged
            compare = self.client.get(
                f"/repos/{owner}/{repo}/compare/{base_branch}...{branch_name}"
            )
            
            if compare["status"] == "identical" or compare["ahead_by"] == 0:
                self.delete_branch(owner, repo, branch_name)
                deleted.append(branch_name)
        
        logger.info(f"Deleted {len(deleted)} merged branches")
        return deleted
    
    def _detect_branch_type(self, branch_name: str) -> BranchType:
        """Detect branch type from name."""
        if branch_name == "main" or branch_name == "master":
            return BranchType.MAIN
        elif branch_name == "develop":
            return BranchType.DEVELOP
        elif branch_name.startswith("feature/"):
            return BranchType.FEATURE
        elif branch_name.startswith("bugfix/"):
            return BranchType.BUGFIX
        elif branch_name.startswith("hotfix/"):
            return BranchType.HOTFIX
        elif branch_name.startswith("release/"):
            return BranchType.RELEASE
        else:
            return BranchType.FEATURE  # Default
```

### Milestone 3: Changelog & Release Management (Week 3)
**Deliverables:**
- Conventional commit parser
- Changelog generator
- Semantic versioning
- Release automation

**Key Code Example:**
```python
from typing import List, Optional, Tuple
import re
from packaging import version

class ChangelogGenerator:
    """Generate changelogs from commits."""
    
    def __init__(self, client: GitHubClient):
        self.client = client
    
    def generate_changelog(
        self,
        owner: str,
        repo: str,
        from_tag: Optional[str] = None,
        to_ref: str = "main"
    ) -> str:
        """
        Generate changelog between two refs.
        
        Args:
            owner: Repository owner
            repo: Repository name
            from_tag: Starting tag (None for all commits)
            to_ref: Ending ref (branch/tag/SHA)
            
        Returns:
            Formatted changelog
        """
        logger.info(f"Generating changelog: {from_tag or 'beginning'} → {to_ref}")
        
        # Get commits
        commits = self._get_commits(owner, repo, from_tag, to_ref)
        
        # Parse commits
        parsed_commits = [self._parse_commit(c) for c in commits]
        
        # Group by type
        grouped = self._group_commits(parsed_commits)
        
        # Format changelog
        changelog = self._format_changelog(grouped)
        
        return changelog
    
    def _get_commits(
        self,
        owner: str,
        repo: str,
        since: Optional[str],
        until: str
    ) -> List[Dict]:
        """Get commits between refs."""
        params = {"sha": until}
        
        if since:
            # Get tag commit date
            tag = self.client.get(f"/repos/{owner}/{repo}/git/refs/tags/{since}")
            commit = self.client.get(tag["object"]["url"])
            params["since"] = commit["committer"]["date"]
        
        commits = self.client.get(f"/repos/{owner}/{repo}/commits", params=params)
        
        return commits
    
    def _parse_commit(self, commit_data: Dict) -> Commit:
        """Parse commit data."""
        commit = Commit(
            sha=commit_data["sha"],
            message=commit_data["commit"]["message"],
            author=commit_data["commit"]["author"]["name"],
            timestamp=datetime.fromisoformat(
                commit_data["commit"]["author"]["date"].rstrip('Z')
            )
        )
        
        commit.parse_conventional_commit()
        
        return commit
    
    def _group_commits(self, commits: List[Commit]) -> Dict[CommitType, List[Commit]]:
        """Group commits by type."""
        grouped: Dict[CommitType, List[Commit]] = {}
        
        for commit in commits:
            if commit.commit_type:
                if commit.commit_type not in grouped:
                    grouped[commit.commit_type] = []
                grouped[commit.commit_type].append(commit)
        
        return grouped
    
    def _format_changelog(self, grouped: Dict[CommitType, List[Commit]]) -> str:
        """Format changelog sections."""
        sections_order = [
            (CommitType.BREAKING, "💥 BREAKING CHANGES"),
            (CommitType.FEAT, "✨ Features"),
            (CommitType.FIX, "🐛 Bug Fixes"),
            (CommitType.PERF, "⚡ Performance"),
            (CommitType.DOCS, "📚 Documentation"),
            (CommitType.REFACTOR, "♻️ Refactoring"),
            (CommitType.TEST, "✅ Tests"),
            (CommitType.CHORE, "🔧 Chores")
        ]
        
        lines = []
        
        for commit_type, section_name in sections_order:
            commits = grouped.get(commit_type, [])
            
            if commits:
                lines.append(f"\n### {section_name}\n")
                
                for commit in commits:
                    msg = commit.message.split('\n')[0]
                    scope = f"**{commit.scope}**: " if commit.scope else ""
                    lines.append(f"- {scope}{msg} ([{commit.sha[:7]}](commit/{commit.sha}))")
        
        return "\n".join(lines)


class SemanticVersionManager:
    """Manage semantic versioning."""
    
    @staticmethod
    def bump_version(
        current: str,
        bump_type: str,
        commits: Optional[List[Commit]] = None
    ) -> str:
        """
        Bump version based on type or commits.
        
        Args:
            current: Current version (e.g., "1.2.3")
            bump_type: "major", "minor", "patch", or "auto"
            commits: Commits to analyze for auto-bump
            
        Returns:
            New version string
        """
        current_version = version.parse(current)
        
        if bump_type == "auto" and commits:
            bump_type = SemanticVersionManager._detect_bump_type(commits)
        
        major, minor, patch = current_version.major, current_version.minor, current_version.micro
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    
    @staticmethod
    def _detect_bump_type(commits: List[Commit]) -> str:
        """Detect version bump type from commits."""
        has_breaking = any(c.breaking for c in commits)
        has_feat = any(c.commit_type == CommitType.FEAT for c in commits)
        
        if has_breaking:
            return "major"
        elif has_feat:
            return "minor"
        else:
            return "patch"


class ReleaseManager:
    """Manage GitHub releases."""
    
    def __init__(self, client: GitHubClient):
        self.client = client
        self.changelog_gen = ChangelogGenerator(client)
    
    def create_release(
        self,
        owner: str,
        repo: str,
        version: str,
        target_branch: str = "main",
        previous_tag: Optional[str] = None,
        draft: bool = False,
        prerelease: bool = False
    ) -> Release:
        """
        Create a GitHub release with auto-generated changelog.
        
        Args:
            owner: Repository owner
            repo: Repository name
            version: Release version
            target_branch: Target branch
            previous_tag: Previous release tag
            draft: Create as draft
            prerelease: Mark as prerelease
            
        Returns:
            Created release
        """
        logger.info(f"Creating release {version}")
        
        # Generate changelog
        changelog = self.changelog_gen.generate_changelog(
            owner, repo, previous_tag, target_branch
        )
        
        tag_name = f"v{version}"
        
        # Create release
        payload = {
            "tag_name": tag_name,
            "target_commitish": target_branch,
            "name": f"Release {version}",
            "body": changelog,
            "draft": draft,
            "prerelease": prerelease
        }
        
        response = self.client.post(f"/repos/{owner}/{repo}/releases", json=payload)
        
        logger.info(f"Release created: {response['html_url']}")
        
        return Release(
            version=version,
            tag_name=tag_name,
            name=response["name"],
            body=response["body"],
            draft=draft,
            prerelease=prerelease,
            created_at=datetime.fromisoformat(response["created_at"].rstrip('Z'))
        )
```

### Milestone 4: Complete CLI & Advanced Features (Week 4)
**Deliverables:**
- Full CLI with all commands
- GitHub Actions integration
- Pipeline monitoring
- Interactive mode

**Key Code Example:**
```python
import click
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
@click.option('--token', envvar='GITHUB_TOKEN', help='GitHub token')
@click.pass_context
def cli(ctx, token):
    """CI/CD Helper - Automate your DevOps workflows"""
    if not token:
        console.print("[red]Error: GitHub token not provided[/red]")
        console.print("Set GITHUB_TOKEN environment variable or use --token option")
        raise click.Abort()
    
    ctx.obj = GitHubClient(token)

# Repository commands
@cli.group()
def repo():
    """Repository management commands"""
    pass

@repo.command('create')
@click.argument('name')
@click.option('--description', '-d', default='', help='Repository description')
@click.option('--private', is_flag=True, help='Create private repository')
@click.option('--gitignore', help='Gitignore template (e.g., Python)')
@click.pass_obj
def create_repo(client, name, description, private, gitignore):
    """Create a new repository"""
    manager = RepositoryManager(client)
    
    with console.status(f"Creating repository {name}..."):
        repo = manager.create_repository(
            name=name,
            description=description,
            private=private,
            gitignore_template=gitignore
        )
    
    console.print(f"[green]✓[/green] Repository created: {repo.url}")

# Branch commands
@cli.group()
def branch():
    """Branch management commands"""
    pass

@branch.command('create')
@click.option('--owner', '-o', required=True)
@click.option('--repo', '-r', required=True)
@click.argument('branch_name')
@click.option('--from', 'base_branch', default='main', help='Base branch')
@click.pass_obj
def create_branch(client, owner, repo, branch_name, base_branch):
    """Create a new branch"""
    manager = BranchManager(client)
    
    branch = manager.create_branch(owner, repo, branch_name, base_branch)
    console.print(f"[green]✓[/green] Branch created: {branch.get_full_name()}")

@branch.command('cleanup')
@click.option('--owner', '-o', required=True)
@click.option('--repo', '-r', required=True)
@click.option('--base', default='main', help='Base branch')
@click.confirmation_option(prompt='Delete all merged branches?')
@click.pass_obj
def cleanup_branches(client, owner, repo, base):
    """Delete merged branches"""
    manager = BranchManager(client)
    
    with console.status("Finding merged branches..."):
        deleted = manager.cleanup_merged_branches(owner, repo, base)
    
    console.print(f"[green]✓[/green] Deleted {len(deleted)} branches")
    for branch in deleted:
        console.print(f"  - {branch}")

# Release commands
@cli.group()
def release():
    """Release management commands"""
    pass

@release.command('create')
@click.option('--owner', '-o', required=True)
@click.option('--repo', '-r', required=True)
@click.option('--version', '-v', required=True, help='Version number (e.g., 1.2.3)')
@click.option('--previous', '-p', help='Previous tag for changelog')
@click.option('--draft', is_flag=True, help='Create as draft')
@click.option('--prerelease', is_flag=True, help='Mark as prerelease')
@click.pass_obj
def create_release(client, owner, repo, version, previous, draft, prerelease):
    """Create a new release with changelog"""
    manager = ReleaseManager(client)
    
    with console.status(f"Creating release {version}..."):
        release = manager.create_release(
            owner, repo, version,
            previous_tag=previous,
            draft=draft,
            prerelease=prerelease
        )
    
    console.print(f"[green]✓[/green] Release {release.version} created")
    console.print(f"\n{release.body}")

@release.command('changelog')
@click.option('--owner', '-o', required=True)
@click.option('--repo', '-r', required=True)
@click.option('--from', 'from_tag', help='Starting tag')
@click.option('--to', 'to_ref', default='main', help='Ending ref')
@click.pass_obj
def generate_changelog(client, owner, repo, from_tag, to_ref):
    """Generate changelog"""
    generator = ChangelogGenerator(client)
    
    with console.status("Generating changelog..."):
        changelog = generator.generate_changelog(owner, repo, from_tag, to_ref)
    
    console.print(changelog)

# Deployment commands
@cli.group()
def deploy():
    """Deployment commands"""
    pass

@deploy.command('trigger')
@click.option('--owner', '-o', required=True)
@click.option('--repo', '-r', required=True)
@click.option('--workflow', '-w', required=True, help='Workflow file name')
@click.option('--ref', '-r', default='main', help='Branch/tag to deploy')
@click.option('--env', '-e', help='Environment name')
@click.pass_obj
def trigger_deployment(client, owner, repo, workflow, ref, env):
    """Trigger a GitHub Actions workflow"""
    console.print(f"[yellow]Triggering {workflow} on {ref}...[/yellow]")
    
    inputs = {}
    if env:
        inputs['environment'] = env
    
    client.post(
        f"/repos/{owner}/{repo}/actions/workflows/{workflow}/dispatches",
        json={"ref": ref, "inputs": inputs}
    )
    
    console.print("[green]✓[/green] Deployment triggered")

if __name__ == '__main__':
    cli()
```

## Project-Specific Requirements

### requirements.txt
```
# GitHub API
requests==2.31.0
PyGithub==2.1.1

# CLI & Display
click==8.1.7
rich==13.7.0

# Versioning
packaging==23.2

# Configuration
pyyaml==6.0.1
python-dotenv==1.0.0

# Utilities
python-dateutil==2.8.2
tenacity==8.2.3
```

### requirements-dev.txt
```
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
responses==0.24.1
black==23.12.1
flake8==6.1.0
mypy==1.7.1
types-requests==2.31.0
```

## Evaluation Criteria

### Must Have
- [ ] GitHub authentication and API integration
- [ ] Repository creation and management
- [ ] Branch creation and PR automation
- [ ] Changelog generation from conventional commits
- [ ] Semantic versioning support
- [ ] Release creation
- [ ] Error handling and retry logic
- [ ] Type hints and PEP 8
- [ ] >70% test coverage

### Should Have
- [ ] Branch protection rules
- [ ] Merged branch cleanup
- [ ] GitHub Actions workflow triggers
- [ ] Multiple merge strategies
- [ ] Rate limit handling
- [ ] Rich CLI output
- [ ] Interactive confirmations

### Nice to Have
- [ ] Jenkins/CircleCI integration
- [ ] Multi-repository operations
- [ ] Webhook management
- [ ] CI config validation
- [ ] Pipeline status dashboard
- [ ] GitLab/Bitbucket support

## Bonus Features

1. **AI-Powered Changelog**
   - Use LLM to summarize changes
   - Generate user-friendly release notes

2. **Deployment Analytics**
   - Track deployment frequency
   - MTTR/MTTD metrics
   - Failure rate analysis

3. **GitOps Integration**
   - ArgoCD synchronization
   - Flux CD integration
   - Helm chart versioning

4. **Advanced Automation**
   - Auto-merge dependabot PRs
   - Automatic release notes
   - Smart version bumping

5. **Team Collaboration**
   - PR review assignment
   - Code ownership integration
   - Team performance metrics

## Deliverables

1. Source code with CLI commands
2. Comprehensive documentation
3. Unit and integration tests
4. Example workflows and scripts
5. Demo showing:
   - Repository creation
   - Branch and PR workflow
   - Release creation with changelog
   - Deployment trigger

## Success Metrics
- Successfully automates all core CI/CD tasks
- Generates accurate changelogs
- Handles GitHub API rate limits gracefully
- All tests pass
- Clean, maintainable code

## Learning Outcomes
- GitHub API integration
- CLI design best practices
- Conventional commits and semantic versioning
- CI/CD automation patterns
- Release management workflows
- API rate limiting strategies
- Building production DevOps tools
