# PROJECT 03: Configuration Management Tool

## Problem Statement (User Story)
**As a DevOps engineer**, I need a Python tool that reads YAML configuration files, validates them against a schema, and applies configurations to multiple environments, so that I can maintain consistency across dev/staging/prod, reduce configuration errors, and implement infrastructure-as-code best practices.

## Project Objectives
- Build a production-ready configuration management CLI tool
- Implement robust YAML parsing and validation
- Support environment-specific overrides and templating
- Enable safe configuration deployment with rollback
- Demonstrate schema validation and error handling
- Create an auditable, version-controlled configuration system

## Requirements

### Functional Requirements
1. **Configuration Loading**
   - Parse YAML configuration files
   - Support nested configurations
   - Handle environment-specific overrides
   - Template variable substitution
   - Include/import other config files

2. **Schema Validation**
   - Define JSON Schema for configurations
   - Validate before applying changes
   - Provide clear error messages for violations
   - Support custom validation rules

3. **Multi-Environment Support**
   - Manage dev, staging, production environments
   - Environment-specific variable overrides
   - Secrets management integration
   - Environment promotion workflows

4. **Configuration Application**
   - Apply configs to remote systems (SSH)
   - Update application configuration files
   - Restart services after config changes
   - Database configuration updates
   - API configuration updates

5. **Safety & Rollback**
   - Dry-run mode (preview changes)
   - Backup before applying changes
   - Rollback to previous configuration
   - Change history and audit log

### Non-Functional Requirements
- **Reliability**: Atomic operations, rollback on failure
- **Security**: Encrypted secrets, secure SSH connections
- **Maintainability**: Modular design, extensive logging
- **Usability**: Intuitive CLI, clear error messages
- **Performance**: Handle large configs efficiently

## Technical Specification

### Features List
- [ ] YAML parsing with validation
- [ ] JSON Schema validation
- [ ] Jinja2 templating for variables
- [ ] Environment-specific overrides
- [ ] Secrets management (encrypted values)
- [ ] SSH-based remote configuration
- [ ] Dry-run mode
- [ ] Configuration backup and versioning
- [ ] Rollback capability
- [ ] Change diff display
- [ ] Service restart/reload
- [ ] Audit logging
- [ ] Git integration for version control
- [ ] Configuration drift detection
- [ ] Interactive mode for confirmations

### Suggested Architecture

```
config-management/
├── src/
│   ├── __init__.py
│   ├── main.py                    # CLI entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── loader.py              # YAML loader
│   │   ├── validator.py           # Schema validation
│   │   ├── templater.py           # Jinja2 templating
│   │   └── merger.py              # Environment merging
│   ├── deployer/
│   │   ├── __init__.py
│   │   ├── base.py                # Base deployer
│   │   ├── ssh_deployer.py        # SSH deployment
│   │   ├── local_deployer.py      # Local deployment
│   │   └── api_deployer.py        # API-based deployment
│   ├── secrets/
│   │   ├── __init__.py
│   │   ├── manager.py             # Secrets manager
│   │   └── encryption.py          # Encryption utils
│   ├── versioning/
│   │   ├── __init__.py
│   │   ├── backup.py              # Backup management
│   │   └── git_ops.py             # Git operations
│   └── utils/
│       ├── __init__.py
│       ├── ssh.py                 # SSH utilities
│       ├── diff.py                # Configuration diff
│       └── logger.py              # Logging setup
├── schemas/
│   ├── app_config.schema.json     # App config schema
│   ├── database.schema.json       # DB config schema
│   └── common.schema.json         # Common schema
├── configs/
│   ├── base/
│   │   └── app.yaml               # Base configuration
│   ├── environments/
│   │   ├── dev.yaml               # Dev overrides
│   │   ├── staging.yaml           # Staging overrides
│   │   └── prod.yaml              # Prod overrides
│   └── secrets/
│       └── .gitkeep               # Encrypted secrets
├── tests/
│   ├── __init__.py
│   ├── test_loader.py
│   ├── test_validator.py
│   ├── test_templater.py
│   └── fixtures/
├── requirements.txt
├── README.md
└── .env.example
```

### Data Models

```python
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from enum import Enum

class Environment(Enum):
    """Deployment environment."""
    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"

class ChangeAction(Enum):
    """Type of configuration change."""
    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"
    UNCHANGED = "unchanged"

@dataclass
class ConfigChange:
    """Represents a configuration change."""
    path: str  # Dot-notation path (e.g., "database.host")
    action: ChangeAction
    old_value: Any = None
    new_value: Any = None
    
    def __str__(self) -> str:
        """Human-readable representation."""
        if self.action == ChangeAction.ADD:
            return f"+ {self.path} = {self.new_value}"
        elif self.action == ChangeAction.DELETE:
            return f"- {self.path} = {self.old_value}"
        elif self.action == ChangeAction.MODIFY:
            return f"~ {self.path}: {self.old_value} → {self.new_value}"
        else:
            return f"  {self.path} = {self.new_value}"

@dataclass
class Configuration:
    """Configuration object."""
    data: Dict[str, Any]
    environment: Environment
    version: str = field(default_factory=lambda: datetime.utcnow().strftime("%Y%m%d_%H%M%S"))
    source_files: List[Path] = field(default_factory=list)
    validated: bool = False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key."""
        keys = key.split('.')
        value = self.data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot-notation key."""
        keys = key.split('.')
        data = self.data
        
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        
        data[keys[-1]] = value

@dataclass
class DeploymentResult:
    """Result of a configuration deployment."""
    success: bool
    environment: Environment
    changes: List[ConfigChange]
    backup_path: Optional[Path] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    
    def summary(self) -> str:
        """Generate summary string."""
        status = "✓ SUCCESS" if self.success else "✗ FAILED"
        
        change_counts = {
            ChangeAction.ADD: sum(1 for c in self.changes if c.action == ChangeAction.ADD),
            ChangeAction.MODIFY: sum(1 for c in self.changes if c.action == ChangeAction.MODIFY),
            ChangeAction.DELETE: sum(1 for c in self.changes if c.action == ChangeAction.DELETE),
        }
        
        summary = [
            f"{status}",
            f"Environment: {self.environment.value}",
            f"Changes: +{change_counts[ChangeAction.ADD]} ~{change_counts[ChangeAction.MODIFY]} -{change_counts[ChangeAction.DELETE]}",
            f"Duration: {self.duration_seconds:.2f}s"
        ]
        
        if self.backup_path:
            summary.append(f"Backup: {self.backup_path}")
        
        if self.errors:
            summary.append(f"Errors: {len(self.errors)}")
        
        return "\n".join(summary)
```

## Implementation Guidelines

### Milestone 1: Configuration Loading & Parsing (Week 1)
**Deliverables:**
- YAML parser with error handling
- Environment merging logic
- Basic templating with Jinja2
- Unit tests for loader

**Key Code Example:**
```python
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from jinja2 import Environment as JinjaEnv, FileSystemLoader, TemplateError
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Load and merge configuration files."""
    
    def __init__(self, config_dir: Path, template_vars: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration loader.
        
        Args:
            config_dir: Root directory for configurations
            template_vars: Variables for Jinja2 templating
        """
        self.config_dir = config_dir
        self.template_vars = template_vars or {}
        
        # Setup Jinja2
        self.jinja_env = JinjaEnv(
            loader=FileSystemLoader(str(config_dir)),
            autoescape=False
        )
    
    def load(
        self,
        base_config: str,
        environment: Environment,
        additional_vars: Optional[Dict[str, Any]] = None
    ) -> Configuration:
        """
        Load configuration for an environment.
        
        Args:
            base_config: Base configuration file name
            environment: Target environment
            additional_vars: Additional template variables
            
        Returns:
            Merged and templated configuration
        """
        logger.info(f"Loading configuration for environment: {environment.value}")
        
        # Merge template variables
        template_vars = {**self.template_vars, **(additional_vars or {})}
        template_vars['env'] = environment.value
        
        # Load base configuration
        base_path = self.config_dir / "base" / base_config
        base_data = self._load_yaml(base_path, template_vars)
        
        # Load environment-specific overrides
        env_path = self.config_dir / "environments" / f"{environment.value}.yaml"
        env_data = {}
        
        if env_path.exists():
            env_data = self._load_yaml(env_path, template_vars)
        
        # Merge configurations (environment overrides base)
        merged_data = self._deep_merge(base_data, env_data)
        
        return Configuration(
            data=merged_data,
            environment=environment,
            source_files=[base_path, env_path] if env_path.exists() else [base_path]
        )
    
    def _load_yaml(self, path: Path, template_vars: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load and template a YAML file.
        
        Args:
            path: Path to YAML file
            template_vars: Variables for templating
            
        Returns:
            Parsed YAML data
        """
        try:
            # Read file
            with path.open('r') as f:
                content = f.read()
            
            # Apply Jinja2 templating
            template = self.jinja_env.from_string(content)
            templated_content = template.render(**template_vars)
            
            # Parse YAML
            data = yaml.safe_load(templated_content)
            
            logger.debug(f"Loaded configuration from {path}")
            return data or {}
            
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {path}: {e}")
            raise
        except TemplateError as e:
            logger.error(f"Template error in {path}: {e}")
            raise
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries.
        
        Args:
            base: Base dictionary
            override: Override dictionary
            
        Returns:
            Merged dictionary
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dicts
                result[key] = self._deep_merge(result[key], value)
            else:
                # Override value
                result[key] = value
        
        return result
```

### Milestone 2: Schema Validation (Week 2)
**Deliverables:**
- JSON Schema validator
- Custom validation rules
- Clear error reporting
- Schema examples

**Key Code Example:**
```python
from jsonschema import validate, ValidationError, Draft7Validator
from typing import Dict, Any, List, Optional
import json
from pathlib import Path

class ConfigValidator:
    """Validate configurations against JSON schemas."""
    
    def __init__(self, schema_dir: Path):
        """
        Initialize validator.
        
        Args:
            schema_dir: Directory containing JSON schemas
        """
        self.schema_dir = schema_dir
        self.schemas: Dict[str, Dict] = {}
    
    def load_schema(self, schema_name: str) -> Dict:
        """
        Load a JSON schema.
        
        Args:
            schema_name: Schema file name (without .json)
            
        Returns:
            Schema dictionary
        """
        if schema_name in self.schemas:
            return self.schemas[schema_name]
        
        schema_path = self.schema_dir / f"{schema_name}.schema.json"
        
        with schema_path.open('r') as f:
            schema = json.load(f)
        
        self.schemas[schema_name] = schema
        logger.debug(f"Loaded schema: {schema_name}")
        
        return schema
    
    def validate(
        self,
        config: Configuration,
        schema_name: str
    ) -> tuple[bool, List[str]]:
        """
        Validate configuration against schema.
        
        Args:
            config: Configuration to validate
            schema_name: Name of schema to validate against
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        schema = self.load_schema(schema_name)
        errors: List[str] = []
        
        try:
            # Create validator
            validator = Draft7Validator(schema)
            
            # Validate
            validation_errors = sorted(
                validator.iter_errors(config.data),
                key=lambda e: e.path
            )
            
            for error in validation_errors:
                # Build path string
                path = '.'.join(str(p) for p in error.path)
                
                # Format error message
                if path:
                    msg = f"Validation error at '{path}': {error.message}"
                else:
                    msg = f"Validation error: {error.message}"
                
                errors.append(msg)
                logger.warning(msg)
            
            if not errors:
                logger.info(f"Configuration validation passed: {schema_name}")
                config.validated = True
                return True, []
            else:
                return False, errors
                
        except Exception as e:
            error_msg = f"Validation failed: {str(e)}"
            logger.error(error_msg)
            return False, [error_msg]
    
    def validate_with_custom_rules(
        self,
        config: Configuration,
        custom_rules: List[callable]
    ) -> tuple[bool, List[str]]:
        """
        Apply custom validation rules.
        
        Args:
            config: Configuration to validate
            custom_rules: List of validation functions
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors: List[str] = []
        
        for rule in custom_rules:
            try:
                is_valid, error_msg = rule(config)
                if not is_valid:
                    errors.append(error_msg)
            except Exception as e:
                errors.append(f"Custom rule error: {str(e)}")
        
        return len(errors) == 0, errors


# Example custom validation rule
def validate_database_config(config: Configuration) -> tuple[bool, str]:
    """
    Custom validation: ensure database config is complete.
    
    Args:
        config: Configuration to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    db_config = config.get('database', {})
    
    required_fields = ['host', 'port', 'database', 'username']
    missing = [f for f in required_fields if f not in db_config]
    
    if missing:
        return False, f"Database config missing required fields: {', '.join(missing)}"
    
    # Validate port is numeric
    if not isinstance(db_config.get('port'), int):
        return False, "Database port must be an integer"
    
    # Validate port range
    port = db_config['port']
    if not (1 <= port <= 65535):
        return False, f"Database port {port} out of valid range (1-65535)"
    
    return True, ""
```

### Milestone 3: Deployment & SSH Integration (Week 3)
**Deliverables:**
- SSH-based deployment
- Service restart capability
- Backup before deployment
- Rollback mechanism

**Key Code Example:**
```python
import paramiko
from pathlib import Path
from typing import Dict, Any, List, Optional
import shutil
from datetime import datetime

class SSHDeployer:
    """Deploy configurations via SSH."""
    
    def __init__(
        self,
        host: str,
        username: str,
        key_file: Optional[str] = None,
        password: Optional[str] = None,
        port: int = 22
    ):
        """
        Initialize SSH deployer.
        
        Args:
            host: Remote host
            username: SSH username
            key_file: Path to SSH private key
            password: SSH password (if not using key)
            port: SSH port
        """
        self.host = host
        self.username = username
        self.key_file = key_file
        self.password = password
        self.port = port
        self.client: Optional[paramiko.SSHClient] = None
    
    def connect(self) -> None:
        """Establish SSH connection."""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            if self.key_file:
                self.client.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    key_filename=self.key_file
                )
            else:
                self.client.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password
                )
            
            logger.info(f"Connected to {self.host}")
        except Exception as e:
            logger.error(f"SSH connection failed: {e}")
            raise
    
    def disconnect(self) -> None:
        """Close SSH connection."""
        if self.client:
            self.client.close()
            logger.info("SSH connection closed")
    
    def deploy_config(
        self,
        config: Configuration,
        remote_path: str,
        backup: bool = True,
        restart_service: Optional[str] = None
    ) -> DeploymentResult:
        """
        Deploy configuration to remote host.
        
        Args:
            config: Configuration to deploy
            remote_path: Remote file path
            backup: Whether to backup existing file
            restart_service: Service name to restart after deployment
            
        Returns:
            Deployment result
        """
        start_time = datetime.utcnow()
        changes: List[ConfigChange] = []
        backup_path: Optional[Path] = None
        errors: List[str] = []
        
        try:
            if not self.client:
                self.connect()
            
            sftp = self.client.open_sftp()
            
            # Backup existing file
            if backup:
                try:
                    backup_path = self._backup_remote_file(sftp, remote_path)
                    logger.info(f"Backed up {remote_path} to {backup_path}")
                except Exception as e:
                    logger.warning(f"Backup failed: {e}")
            
            # Get current config for diff
            current_config = self._read_remote_yaml(sftp, remote_path)
            
            # Calculate changes
            changes = self._calculate_changes(current_config, config.data)
            
            # Write new configuration
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
                yaml.dump(config.data, tmp, default_flow_style=False)
                tmp_path = tmp.name
            
            sftp.put(tmp_path, remote_path)
            Path(tmp_path).unlink()
            
            logger.info(f"Deployed configuration to {remote_path}")
            
            # Restart service if specified
            if restart_service:
                self._restart_service(restart_service)
            
            sftp.close()
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            return DeploymentResult(
                success=True,
                environment=config.environment,
                changes=changes,
                backup_path=backup_path,
                duration_seconds=duration
            )
            
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            errors.append(str(e))
            
            # Attempt rollback if backup exists
            if backup_path:
                try:
                    self._rollback(remote_path, backup_path)
                except Exception as rollback_error:
                    errors.append(f"Rollback failed: {rollback_error}")
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            return DeploymentResult(
                success=False,
                environment=config.environment,
                changes=changes,
                backup_path=backup_path,
                errors=errors,
                duration_seconds=duration
            )
    
    def _backup_remote_file(self, sftp, remote_path: str) -> Path:
        """Create backup of remote file."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{remote_path}.backup.{timestamp}"
        
        # Copy file
        stdin, stdout, stderr = self.client.exec_command(
            f"cp {remote_path} {backup_path}"
        )
        
        exit_code = stdout.channel.recv_exit_status()
        if exit_code != 0:
            raise Exception(f"Backup failed: {stderr.read().decode()}")
        
        return Path(backup_path)
    
    def _read_remote_yaml(self, sftp, remote_path: str) -> Dict[str, Any]:
        """Read YAML file from remote host."""
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp_path = tmp.name
            
            sftp.get(remote_path, tmp_path)
            
            with open(tmp_path, 'r') as f:
                data = yaml.safe_load(f)
            
            Path(tmp_path).unlink()
            return data or {}
            
        except FileNotFoundError:
            return {}
    
    def _calculate_changes(
        self,
        old_config: Dict[str, Any],
        new_config: Dict[str, Any],
        prefix: str = ""
    ) -> List[ConfigChange]:
        """Calculate differences between configurations."""
        changes: List[ConfigChange] = []
        
        # Find modified and deleted keys
        for key in old_config:
            path = f"{prefix}.{key}" if prefix else key
            
            if key not in new_config:
                changes.append(ConfigChange(
                    path=path,
                    action=ChangeAction.DELETE,
                    old_value=old_config[key]
                ))
            elif old_config[key] != new_config[key]:
                if isinstance(old_config[key], dict) and isinstance(new_config[key], dict):
                    # Recursively check nested dicts
                    changes.extend(self._calculate_changes(
                        old_config[key],
                        new_config[key],
                        path
                    ))
                else:
                    changes.append(ConfigChange(
                        path=path,
                        action=ChangeAction.MODIFY,
                        old_value=old_config[key],
                        new_value=new_config[key]
                    ))
        
        # Find added keys
        for key in new_config:
            if key not in old_config:
                path = f"{prefix}.{key}" if prefix else key
                changes.append(ConfigChange(
                    path=path,
                    action=ChangeAction.ADD,
                    new_value=new_config[key]
                ))
        
        return changes
    
    def _restart_service(self, service_name: str) -> None:
        """Restart a systemd service."""
        command = f"sudo systemctl restart {service_name}"
        
        stdin, stdout, stderr = self.client.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        
        if exit_code == 0:
            logger.info(f"Service {service_name} restarted successfully")
        else:
            error = stderr.read().decode()
            raise Exception(f"Service restart failed: {error}")
    
    def _rollback(self, remote_path: str, backup_path: Path) -> None:
        """Rollback to backup configuration."""
        logger.warning(f"Rolling back {remote_path} from {backup_path}")
        
        stdin, stdout, stderr = self.client.exec_command(
            f"cp {backup_path} {remote_path}"
        )
        
        exit_code = stdout.channel.recv_exit_status()
        if exit_code != 0:
            raise Exception(f"Rollback failed: {stderr.read().decode()}")
        
        logger.info("Rollback completed")
```

### Milestone 4: CLI & Advanced Features (Week 4)
**Deliverables:**
- Complete CLI with all options
- Dry-run mode
- Interactive confirmations
- Change diff display
- Audit logging

**Key Code Example:**
```python
import click
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

console = Console()

@click.group()
def cli():
    """Configuration Management Tool"""
    pass

@cli.command()
@click.option('--config', '-c', required=True, help='Base configuration file')
@click.option('--environment', '-e', type=click.Choice(['dev', 'staging', 'prod']),
              required=True, help='Target environment')
@click.option('--schema', '-s', help='Schema to validate against')
@click.option('--var', '-v', multiple=True, help='Template variables (key=value)')
@click.option('--dry-run', is_flag=True, help='Preview changes without applying')
@click.option('--no-backup', is_flag=True, help='Skip backup before deployment')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation prompts')
def deploy(
    config: str,
    environment: str,
    schema: Optional[str],
    var: tuple,
    dry_run: bool,
    no_backup: bool,
    force: bool
):
    """Deploy configuration to an environment."""
    
    # Parse template variables
    template_vars = {}
    for v in var:
        key, value = v.split('=', 1)
        template_vars[key] = value
    
    try:
        # Load configuration
        loader = ConfigLoader(Path('configs'), template_vars)
        config_obj = loader.load(config, Environment(environment))
        
        console.print(f"[bold]Loaded configuration for {environment}[/bold]")
        
        # Validate if schema provided
        if schema:
            validator = ConfigValidator(Path('schemas'))
            is_valid, errors = validator.validate(config_obj, schema)
            
            if not is_valid:
                console.print("[red]✗ Validation failed:[/red]")
                for error in errors:
                    console.print(f"  • {error}")
                raise click.Abort()
            
            console.print("[green]✓ Validation passed[/green]")
        
        # Deploy
        deployer = SSHDeployer(
            host=config_obj.get('deploy.host'),
            username=config_obj.get('deploy.username'),
            key_file=config_obj.get('deploy.ssh_key')
        )
        
        # Show changes preview
        if not force:
            # Display configuration diff
            _display_config_preview(config_obj)
            
            if not click.confirm('Proceed with deployment?'):
                console.print("[yellow]Deployment cancelled[/yellow]")
                return
        
        if dry_run:
            console.print("[yellow]DRY RUN: No changes will be applied[/yellow]")
            return
        
        # Execute deployment
        result = deployer.deploy_config(
            config_obj,
            remote_path=config_obj.get('deploy.remote_path'),
            backup=not no_backup,
            restart_service=config_obj.get('deploy.restart_service')
        )
        
        # Display results
        _display_deployment_result(result)
        
    except Exception as e:
        console.print(f"[red]✗ Deployment failed: {e}[/red]")
        raise click.Abort()

@cli.command()
@click.option('--environment', '-e', type=click.Choice(['dev', 'staging', 'prod']),
              required=True)
@click.option('--backup-id', '-b', required=True, help='Backup ID to rollback to')
def rollback(environment: str, backup_id: str):
    """Rollback to a previous configuration."""
    console.print(f"[yellow]Rolling back {environment} to backup {backup_id}[/yellow]")
    
    if not click.confirm('Are you sure? This will overwrite current configuration.'):
        console.print("Rollback cancelled")
        return
    
    # Implement rollback logic
    # ...

def _display_config_preview(config: Configuration):
    """Display configuration preview."""
    console.print("\n[bold]Configuration Preview:[/bold]")
    
    # Pretty-print YAML
    yaml_str = yaml.dump(config.data, default_flow_style=False)
    syntax = Syntax(yaml_str, "yaml", theme="monokai", line_numbers=True)
    console.print(syntax)

def _display_deployment_result(result: DeploymentResult):
    """Display deployment results."""
    console.print()
    
    if result.success:
        console.print("[green]✓ Deployment successful![/green]")
    else:
        console.print("[red]✗ Deployment failed[/red]")
    
    # Changes table
    if result.changes:
        table = Table(title="Configuration Changes")
        table.add_column("Action", style="cyan")
        table.add_column("Path", style="white")
        table.add_column("Details")
        
        for change in result.changes[:20]:  # Limit display
            action_style = {
                ChangeAction.ADD: "green",
                ChangeAction.MODIFY: "yellow",
                ChangeAction.DELETE: "red"
            }.get(change.action, "white")
            
            details = ""
            if change.action == ChangeAction.MODIFY:
                details = f"{change.old_value} → {change.new_value}"
            elif change.action == ChangeAction.ADD:
                details = str(change.new_value)
            elif change.action == ChangeAction.DELETE:
                details = str(change.old_value)
            
            table.add_row(
                f"[{action_style}]{change.action.value.upper()}[/{action_style}]",
                change.path,
                details
            )
        
        console.print(table)
    
    console.print(f"\nDuration: {result.duration_seconds:.2f}s")
    
    if result.backup_path:
        console.print(f"Backup: {result.backup_path}")

if __name__ == '__main__':
    cli()
```

## Project-Specific Requirements

### requirements.txt
```
# YAML & Config
pyyaml==6.0.1
jinja2==3.1.2

# Schema Validation
jsonschema==4.20.0

# SSH & Deployment
paramiko==3.4.0

# CLI & Display
click==8.1.7
rich==13.7.0

# Secrets Management
cryptography==41.0.7
python-dotenv==1.0.0

# Utilities
python-dateutil==2.8.2
```

### requirements-dev.txt
```
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
black==23.12.1
flake8==6.1.0
mypy==1.7.1
types-pyyaml==6.0.12.12
```

### Example Schema (schemas/app_config.schema.json)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Application Configuration",
  "type": "object",
  "required": ["app", "database"],
  "properties": {
    "app": {
      "type": "object",
      "required": ["name", "port"],
      "properties": {
        "name": {"type": "string"},
        "port": {"type": "integer", "minimum": 1, "maximum": 65535},
        "debug": {"type": "boolean"},
        "log_level": {"type": "string", "enum": ["DEBUG", "INFO", "WARNING", "ERROR"]}
      }
    },
    "database": {
      "type": "object",
      "required": ["host", "port", "database"],
      "properties": {
        "host": {"type": "string"},
        "port": {"type": "integer"},
        "database": {"type": "string"},
        "username": {"type": "string"},
        "password": {"type": "string"},
        "pool_size": {"type": "integer", "minimum": 1}
      }
    }
  }
}
```

### Example Configuration (configs/base/app.yaml)
```yaml
app:
  name: my-application
  port: {{ port | default(8000) }}
  debug: false
  log_level: INFO

database:
  host: {{ db_host | default('localhost') }}
  port: 5432
  database: {{ env }}_database
  username: app_user
  pool_size: 10

cache:
  enabled: true
  host: redis
  port: 6379

deploy:
  host: {{ deploy_host }}
  username: deployer
  ssh_key: ~/.ssh/id_rsa
  remote_path: /etc/myapp/config.yaml
  restart_service: myapp
```

## Evaluation Criteria

### Must Have
- [ ] Loads and parses YAML configurations
- [ ] Validates against JSON schemas
- [ ] Supports environment-specific overrides
- [ ] Jinja2 templating works correctly
- [ ] Deploys configs via SSH
- [ ] Creates backups before deployment
- [ ] Shows configuration diff
- [ ] Dry-run mode
- [ ] Type hints and PEP 8
- [ ] >70% test coverage

### Should Have
- [ ] Secrets encryption
- [ ] Rollback capability
- [ ] Service restart integration
- [ ] Custom validation rules
- [ ] Interactive confirmations
- [ ] Rich CLI output
- [ ] Audit logging
- [ ] Git integration

### Nice to Have
- [ ] Configuration drift detection
- [ ] Web UI for management
- [ ] Kubernetes ConfigMap/Secret deployment
- [ ] Multi-host parallel deployment
- [ ] Configuration templates library
- [ ] Integration tests with Docker

## Bonus Features

1. **Configuration Drift Detection**
   - Compare deployed vs. desired state
   - Alert on unauthorized changes
   - Auto-remediation

2. **Advanced Secrets Management**
   - Integration with HashiCorp Vault
   - AWS Secrets Manager
   - Azure Key Vault

3. **Multi-Cloud Support**
   - AWS Systems Manager Parameter Store
   - GCP Secret Manager
   - Terraform variable files

4. **GitOps Integration**
   - Auto-deploy on git push
   - Pull request validation
   - Change approval workflow

5. **Configuration As Code**
   - Generate configs from Python
   - Type-safe configuration builders
   - IDE autocomplete support

## Deliverables

1. Source code with modular architecture
2. Comprehensive documentation
3. JSON schemas for common configurations
4. Example configurations for multiple environments
5. Unit and integration tests
6. Demo showing:
   - Loading and validating configs
   - Environment-specific overrides
   - Deployment with dry-run
   - Rollback procedure

## Success Metrics
- Successfully deploys configs to 3 environments
- Zero configuration errors in production
- Rollback works within 30 seconds
- All tests pass
- No secrets leaked in logs or code

## Learning Outcomes
- YAML parsing and manipulation
- Schema validation techniques
- Templating with Jinja2
- SSH automation with Paramiko
- Configuration management patterns
- Secrets management best practices
- Building robust CLI tools
- Production deployment strategies
