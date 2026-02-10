# LAB 12: Logging and CLI Tools

## Learning Objectives
By the end of this lab, you will be able to:
- Implement proper logging in DevOps scripts using the `logging` module
- Configure different log levels and formatters
- Create log handlers for files and streams
- Build command-line interfaces with `argparse`
- Use `click` for advanced CLI tools
- Implement subcommands and command groups
- Add progress bars and colored output
- Build production-ready DevOps CLI utilities

## Prerequisites
- Python 3.8+ installed
- Understanding of functions and classes
- Basic command-line experience

## Setup

### Install Required Packages

```bash
# Install CLI and utility packages
pip install click colorama rich tqdm
```

---

## Part 1: Python Logging Module

### Exercise 1.1: Basic Logging

Create `basic_logging.py`:

```python
"""Basic logging examples."""
import logging


# Configure basic logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def deploy_application(app_name, environment):
    """Deploy an application with logging."""
    logger.info(f"Starting deployment of {app_name} to {environment}")
    
    try:
        logger.debug(f"Validating deployment configuration...")
        # Validation logic here
        
        logger.info(f"Building application...")
        # Build logic here
        
        logger.info(f"Deploying to {environment}...")
        # Deployment logic here
        
        logger.info(f"Deployment of {app_name} completed successfully")
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}", exc_info=True)
        raise


def check_server_health(server_name):
    """Check server health with different log levels."""
    logger.debug(f"Checking health of server: {server_name}")
    
    # Simulated health check
    cpu_usage = 45
    memory_usage = 70
    disk_usage = 85
    
    logger.info(f"Server {server_name} health check:")
    logger.info(f"  CPU Usage: {cpu_usage}%")
    logger.info(f"  Memory Usage: {memory_usage}%")
    
    if disk_usage > 80:
        logger.warning(f"  Disk Usage is high: {disk_usage}%")
    else:
        logger.info(f"  Disk Usage: {disk_usage}%")
    
    if cpu_usage > 90:
        logger.critical(f"Server {server_name} CPU usage critical!")
    
    return {'cpu': cpu_usage, 'memory': memory_usage, 'disk': disk_usage}


if __name__ == "__main__":
    # Example usage
    logger.info("DevOps automation script started")
    
    check_server_health("web-server-01")
    
    try:
        deploy_application("my-app", "production")
    except Exception:
        logger.error("Script execution failed")
```

**Expected Output:**
```
2024-01-15 10:30:00,123 - __main__ - INFO - DevOps automation script started
2024-01-15 10:30:00,124 - __main__ - DEBUG - Checking health of server: web-server-01
2024-01-15 10:30:00,124 - __main__ - INFO - Server web-server-01 health check:
2024-01-15 10:30:00,124 - __main__ - INFO -   CPU Usage: 45%
2024-01-15 10:30:00,124 - __main__ - INFO -   Memory Usage: 70%
2024-01-15 10:30:00,124 - __main__ - WARNING -   Disk Usage is high: 85%
```

### Exercise 1.2: Advanced Logging Configuration

Create `advanced_logging.py`:

```python
"""Advanced logging configuration."""
import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging(log_dir='logs', log_level=logging.INFO):
    """
    Set up comprehensive logging configuration.
    
    Creates:
    - Console handler with colored output
    - File handler for all logs
    - Rotating file handler for errors
    - JSON formatter for structured logging
    """
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('devops')
    logger.setLevel(log_level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with custom formatting
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # File handler for all logs
    log_file = os.path.join(log_dir, f'app_{datetime.now():%Y%m%d}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
    )
    file_handler.setFormatter(file_format)
    
    # Rotating file handler for errors
    error_file = os.path.join(log_dir, 'errors.log')
    error_handler = logging.handlers.RotatingFileHandler(
        error_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    return logger


class DeploymentLogger:
    """Logger for deployment operations."""
    
    def __init__(self, deployment_name):
        self.deployment_name = deployment_name
        self.logger = logging.getLogger(f'devops.deployment.{deployment_name}')
    
    def start(self):
        """Log deployment start."""
        self.logger.info("="*60)
        self.logger.info(f"DEPLOYMENT STARTED: {self.deployment_name}")
        self.logger.info("="*60)
    
    def step(self, step_name, status="in_progress"):
        """Log deployment step."""
        symbols = {
            'in_progress': '⏳',
            'success': '✅',
            'failed': '❌',
            'warning': '⚠️'
        }
        symbol = symbols.get(status, '▶️')
        
        if status == 'failed':
            self.logger.error(f"{symbol} {step_name}")
        elif status == 'warning':
            self.logger.warning(f"{symbol} {step_name}")
        else:
            self.logger.info(f"{symbol} {step_name}")
    
    def metric(self, name, value, unit=''):
        """Log a metric."""
        self.logger.info(f"📊 {name}: {value} {unit}")
    
    def complete(self, success=True):
        """Log deployment completion."""
        if success:
            self.logger.info("="*60)
            self.logger.info(f"DEPLOYMENT COMPLETED SUCCESSFULLY: {self.deployment_name}")
            self.logger.info("="*60)
        else:
            self.logger.error("="*60)
            self.logger.error(f"DEPLOYMENT FAILED: {self.deployment_name}")
            self.logger.error("="*60)


# Example usage
if __name__ == "__main__":
    # Setup logging
    logger = setup_logging(log_level=logging.DEBUG)
    
    # Create deployment logger
    deploy_log = DeploymentLogger("my-app-v1.2.3")
    
    deploy_log.start()
    deploy_log.step("Validating configuration", "in_progress")
    deploy_log.step("Validating configuration", "success")
    
    deploy_log.step("Building Docker image", "in_progress")
    deploy_log.metric("Build time", 45, "seconds")
    deploy_log.step("Building Docker image", "success")
    
    deploy_log.step("Pushing to registry", "in_progress")
    deploy_log.step("Pushing to registry", "success")
    
    deploy_log.step("Deploying to Kubernetes", "in_progress")
    deploy_log.step("Deploying to Kubernetes", "success")
    
    deploy_log.metric("Total pods", 3)
    deploy_log.metric("Memory usage", 512, "MB")
    
    deploy_log.complete(success=True)
```

---

## Part 2: Command-Line Interfaces with argparse

### Exercise 2.1: Basic argparse CLI

Create `server_cli.py`:

```python
"""Server management CLI using argparse."""
import argparse
import logging
import sys


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def start_server(name, port, environment):
    """Start a server."""
    logger.info(f"Starting server '{name}'")
    logger.info(f"  Port: {port}")
    logger.info(f"  Environment: {environment}")
    # Server start logic here
    logger.info(f"✓ Server '{name}' started successfully")


def stop_server(name, force=False):
    """Stop a server."""
    logger.info(f"Stopping server '{name}'")
    if force:
        logger.warning("  Force stop enabled")
    # Server stop logic here
    logger.info(f"✓ Server '{name}' stopped")


def restart_server(name):
    """Restart a server."""
    logger.info(f"Restarting server '{name}'")
    stop_server(name)
    start_server(name, 8080, "production")


def server_status(name, detailed=False):
    """Show server status."""
    logger.info(f"Server: {name}")
    logger.info(f"  Status: Running")
    logger.info(f"  Uptime: 3 days, 4 hours")
    
    if detailed:
        logger.info(f"  CPU: 45%")
        logger.info(f"  Memory: 2.5 GB / 8 GB")
        logger.info(f"  Connections: 125")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Server Management CLI',
        epilog='Example: %(prog)s start web-01 --port 8080'
    )
    
    # Add verbose flag
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )
    
    # Start command
    start_parser = subparsers.add_parser(
        'start',
        help='Start a server'
    )
    start_parser.add_argument('name', help='Server name')
    start_parser.add_argument(
        '-p', '--port',
        type=int,
        default=8080,
        help='Server port (default: 8080)'
    )
    start_parser.add_argument(
        '-e', '--environment',
        choices=['dev', 'staging', 'production'],
        default='dev',
        help='Environment (default: dev)'
    )
    
    # Stop command
    stop_parser = subparsers.add_parser(
        'stop',
        help='Stop a server'
    )
    stop_parser.add_argument('name', help='Server name')
    stop_parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='Force stop the server'
    )
    
    # Restart command
    restart_parser = subparsers.add_parser(
        'restart',
        help='Restart a server'
    )
    restart_parser.add_argument('name', help='Server name')
    
    # Status command
    status_parser = subparsers.add_parser(
        'status',
        help='Show server status'
    )
    status_parser.add_argument('name', help='Server name')
    status_parser.add_argument(
        '-d', '--detailed',
        action='store_true',
        help='Show detailed status'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set log level based on verbosity
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Execute command
    if args.command == 'start':
        start_server(args.name, args.port, args.environment)
    elif args.command == 'stop':
        stop_server(args.name, args.force)
    elif args.command == 'restart':
        restart_server(args.name)
    elif args.command == 'status':
        server_status(args.name, args.detailed)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
```

**Usage examples:**
```bash
# Start a server
python server_cli.py start web-01 --port 8080 --environment production

# Stop a server
python server_cli.py stop web-01

# Force stop
python server_cli.py stop web-01 --force

# Restart
python server_cli.py restart web-01

# Status
python server_cli.py status web-01

# Detailed status
python server_cli.py status web-01 --detailed

# Verbose output
python server_cli.py -v start web-01
```

---

## Part 3: Advanced CLI with Click

### Exercise 3.1: Click-based CLI

Create `deploy_cli.py`:

```python
"""Deployment CLI using Click."""
import click
import time
from datetime import datetime


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--dry-run', is_flag=True, help='Perform a dry run')
@click.pass_context
def cli(ctx, verbose, dry_run):
    """
    DevOps Deployment Tool
    
    Manage application deployments across environments.
    """
    # Store context for subcommands
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['DRY_RUN'] = dry_run
    
    if verbose:
        click.echo("Verbose mode enabled")
    if dry_run:
        click.secho("DRY RUN MODE - No changes will be made", fg='yellow', bold=True)


@cli.command()
@click.argument('app_name')
@click.option('--environment', '-e', 
              type=click.Choice(['dev', 'staging', 'production']),
              required=True,
              help='Target environment')
@click.option('--version', '-V', help='Application version to deploy')
@click.option('--replicas', '-r', type=int, default=3, help='Number of replicas')
@click.option('--timeout', type=int, default=300, help='Deployment timeout in seconds')
@click.confirmation_option(
    prompt='Are you sure you want to deploy?'
)
@click.pass_context
def deploy(ctx, app_name, environment, version, replicas, timeout):
    """Deploy an application to an environment."""
    dry_run = ctx.obj['DRY_RUN']
    
    click.secho(f"\n{'='*60}", fg='cyan')
    click.secho(f"Deploying {app_name}", fg='cyan', bold=True)
    click.secho(f"{'='*60}\n", fg='cyan')
    
    click.echo(f"Application: {app_name}")
    click.echo(f"Environment: {environment}")
    click.echo(f"Version: {version or 'latest'}")
    click.echo(f"Replicas: {replicas}")
    
    if dry_run:
        click.secho("\n[DRY RUN] Deployment would proceed here", fg='yellow')
        return
    
    # Simulate deployment steps
    with click.progressbar(
        range(5),
        label='Deploying',
        show_eta=True
    ) as bar:
        for _ in bar:
            time.sleep(1)
    
    click.secho(f"\n✓ {app_name} deployed successfully!", fg='green', bold=True)


@cli.command()
@click.argument('app_name')
@click.option('--environment', '-e',
              type=click.Choice(['dev', 'staging', 'production']),
              required=True)
@click.pass_context
def rollback(ctx, app_name, environment):
    """Rollback an application to the previous version."""
    click.secho(f"\nRolling back {app_name} in {environment}...", fg='yellow')
    
    if click.confirm('This will rollback to the previous version. Continue?'):
        with click.progressbar(range(3), label='Rolling back') as bar:
            for _ in bar:
                time.sleep(1)
        
        click.secho(f"✓ Rollback completed", fg='green')
    else:
        click.echo("Rollback cancelled")


@cli.command()
@click.argument('app_name')
@click.option('--environment', '-e',
              type=click.Choice(['dev', 'staging', 'production']),
              required=True)
@click.option('--format', '-f',
              type=click.Choice(['text', 'json', 'yaml']),
              default='text')
def status(app_name, environment, format):
    """Show application status."""
    status_data = {
        'name': app_name,
        'environment': environment,
        'status': 'running',
        'version': '1.2.3',
        'replicas': {'desired': 3, 'ready': 3},
        'health': 'healthy'
    }
    
    if format == 'json':
        import json
        click.echo(json.dumps(status_data, indent=2))
    elif format == 'yaml':
        import yaml
        click.echo(yaml.dump(status_data, default_flow_style=False))
    else:
        click.secho(f"\nStatus for {app_name}", fg='cyan', bold=True)
        click.echo(f"Environment: {status_data['environment']}")
        click.echo(f"Status: {status_data['status']}")
        click.echo(f"Version: {status_data['version']}")
        click.echo(f"Replicas: {status_data['replicas']['ready']}/{status_data['replicas']['desired']}")
        
        if status_data['health'] == 'healthy':
            click.secho(f"Health: {status_data['health']}", fg='green')
        else:
            click.secho(f"Health: {status_data['health']}", fg='red')


@cli.command()
@click.argument('app_name')
@click.option('--environment', '-e',
              type=click.Choice(['dev', 'staging', 'production']),
              required=True)
@click.option('--replicas', '-r', type=int, required=True,
              help='Number of replicas')
def scale(app_name, environment, replicas):
    """Scale an application."""
    click.echo(f"\nScaling {app_name} in {environment} to {replicas} replicas...")
    
    with click.progressbar(range(replicas), label='Starting replicas') as bar:
        for _ in bar:
            time.sleep(0.5)
    
    click.secho(f"✓ Scaled to {replicas} replicas", fg='green')


@cli.group()
def config():
    """Manage configuration."""
    pass


@config.command('list')
@click.option('--environment', '-e',
              type=click.Choice(['dev', 'staging', 'production']),
              required=True)
def config_list(environment):
    """List configuration for an environment."""
    click.secho(f"\nConfiguration for {environment}:", fg='cyan')
    configs = {
        'DATABASE_URL': 'postgresql://localhost:5432/mydb',
        'REDIS_URL': 'redis://localhost:6379',
        'LOG_LEVEL': 'INFO'
    }
    
    for key, value in configs.items():
        click.echo(f"  {key}: {value}")


@config.command('set')
@click.argument('key')
@click.argument('value')
@click.option('--environment', '-e',
              type=click.Choice(['dev', 'staging', 'production']),
              required=True)
def config_set(key, value, environment):
    """Set a configuration value."""
    click.echo(f"Setting {key}={value} for {environment}")
    click.secho(f"✓ Configuration updated", fg='green')


@cli.command()
@click.argument('app_name')
@click.option('--follow', '-f', is_flag=True, help='Follow log output')
@click.option('--tail', type=int, default=50, help='Number of lines to show')
def logs(app_name, follow, tail):
    """View application logs."""
    click.secho(f"\nLogs for {app_name} (last {tail} lines):", fg='cyan')
    
    # Simulated log output
    sample_logs = [
        "2024-01-15 10:30:00 | INFO | Application started",
        "2024-01-15 10:30:01 | INFO | Connected to database",
        "2024-01-15 10:30:02 | INFO | Server listening on port 8080",
        "2024-01-15 10:30:05 | INFO | Received request: GET /",
        "2024-01-15 10:30:06 | INFO | Request completed in 15ms",
    ]
    
    for log_line in sample_logs[-tail:]:
        if "ERROR" in log_line:
            click.secho(log_line, fg='red')
        elif "WARNING" in log_line:
            click.secho(log_line, fg='yellow')
        else:
            click.echo(log_line)
    
    if follow:
        click.echo("\n[Following logs... Press Ctrl+C to stop]")
        try:
            while True:
                time.sleep(1)
                click.echo(f"{datetime.now():%Y-%m-%d %H:%M:%S} | INFO | Heartbeat")
        except KeyboardInterrupt:
            click.echo("\nStopped following logs")


if __name__ == '__main__':
    cli(obj={})
```

**Usage examples:**
```bash
# Deploy application
python deploy_cli.py deploy my-app -e production -V 1.2.3 -r 5

# Check status
python deploy_cli.py status my-app -e production

# Status in JSON format
python deploy_cli.py status my-app -e production -f json

# Scale application
python deploy_cli.py scale my-app -e production -r 10

# View logs
python deploy_cli.py logs my-app --tail 100

# Follow logs
python deploy_cli.py logs my-app --follow

# List configuration
python deploy_cli.py config list -e production

# Set configuration
python deploy_cli.py config set DATABASE_URL postgresql://... -e production

# Rollback
python deploy_cli.py rollback my-app -e production

# Dry run
python deploy_cli.py --dry-run deploy my-app -e production

# Verbose mode
python deploy_cli.py -v deploy my-app -e production
```

---

## Part 4: Rich Output and Progress Bars

### Exercise 4.1: Rich CLI with Progress

Create `rich_cli.py`:

```python
"""CLI with rich output formatting."""
import time
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.tree import Tree
from rich import print as rprint
from rich.prompt import Confirm


console = Console()


def show_server_status():
    """Display server status in a formatted table."""
    table = Table(title="Server Status", show_header=True, header_style="bold magenta")
    
    table.add_column("Server", style="cyan", width=15)
    table.add_column("Status", width=10)
    table.add_column("CPU", justify="right", width=10)
    table.add_column("Memory", justify="right", width=10)
    table.add_column("Uptime", width=15)
    
    servers = [
        ("web-01", "🟢 Running", "45%", "2.5GB", "3d 4h 15m"),
        ("web-02", "🟢 Running", "52%", "3.1GB", "3d 4h 15m"),
        ("db-01", "🟢 Running", "78%", "6.2GB", "15d 2h 30m"),
        ("cache-01", "🟡 Warning", "15%", "0.8GB", "1d 8h 45m"),
        ("worker-01", "🔴 Stopped", "0%", "0GB", "-"),
    ]
    
    for server in servers:
        name, status, cpu, memory, uptime = server
        
        # Color based on status
        if "Running" in status:
            table.add_row(name, status, cpu, memory, uptime, style="green")
        elif "Warning" in status:
            table.add_row(name, status, cpu, memory, uptime, style="yellow")
        else:
            table.add_row(name, status, cpu, memory, uptime, style="red")
    
    console.print(table)


def deploy_with_progress(app_name, environment):
    """Deploy with a progress bar."""
    console.print(Panel.fit(
        f"[bold cyan]Deploying {app_name} to {environment}[/bold cyan]",
        border_style="cyan"
    ))
    
    tasks = [
        "Validating configuration",
        "Building Docker image",
        "Pushing to registry",
        "Updating Kubernetes deployment",
        "Waiting for pods to be ready",
        "Running health checks"
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        
        for task_name in tasks:
            task = progress.add_task(f"[cyan]{task_name}", total=100)
            
            # Simulate work
            for _ in range(100):
                time.sleep(0.02)
                progress.update(task, advance=1)
    
    console.print("\n[bold green]✓ Deployment completed successfully![/bold green]")


def show_deployment_tree():
    """Show deployment structure as a tree."""
    tree = Tree("🚀 [bold cyan]Deployment Architecture[/bold cyan]")
    
    prod = tree.add("🏭 [yellow]Production[/yellow]")
    
    web_tier = prod.add("🌐 Web Tier")
    web_tier.add("📦 web-01 (nginx)")
    web_tier.add("📦 web-02 (nginx)")
    
    app_tier = prod.add("⚙️  Application Tier")
    app_tier.add("📦 app-01 (python:3.9)")
    app_tier.add("📦 app-02 (python:3.9)")
    app_tier.add("📦 app-03 (python:3.9)")
    
    data_tier = prod.add("💾 Data Tier")
    data_tier.add("📦 db-01 (postgresql)")
    data_tier.add("📦 redis-01 (redis)")
    
    console.print(tree)


def interactive_deploy():
    """Interactive deployment with prompts."""
    console.print("\n[bold cyan]Interactive Deployment Wizard[/bold cyan]\n")
    
    app_name = console.input("[yellow]Application name:[/yellow] ")
    environment = console.input("[yellow]Environment (dev/staging/prod):[/yellow] ")
    version = console.input("[yellow]Version:[/yellow] ")
    
    console.print(f"\n[cyan]Configuration:[/cyan]")
    console.print(f"  App: {app_name}")
    console.print(f"  Environment: {environment}")
    console.print(f"  Version: {version}")
    
    if Confirm.ask("\n[yellow]Proceed with deployment?[/yellow]"):
        deploy_with_progress(app_name, environment)
    else:
        console.print("[red]Deployment cancelled[/red]")


def show_metrics():
    """Display metrics with visual indicators."""
    console.print("\n[bold cyan]System Metrics[/bold cyan]\n")
    
    metrics = {
        "CPU Usage": 45,
        "Memory Usage": 72,
        "Disk Usage": 85,
        "Network I/O": 35
    }
    
    for name, value in metrics.items():
        # Determine color based on value
        if value < 50:
            color = "green"
        elif value < 80:
            color = "yellow"
        else:
            color = "red"
        
        # Create visual bar
        bar_length = 30
        filled = int((value / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        console.print(f"{name:15s} [{color}]{bar}[/{color}] {value}%")


if __name__ == "__main__":
    # Show server status table
    show_server_status()
    
    console.print("\n")
    
    # Show deployment tree
    show_deployment_tree()
    
    console.print("\n")
    
    # Show metrics
    show_metrics()
    
    console.print("\n")
    
    # Deploy with progress
    if Confirm.ask("[yellow]Run deployment demo?[/yellow]"):
        deploy_with_progress("my-app", "production")
    
    # Interactive deployment
    # interactive_deploy()
```

---

## Part 5: Complete DevOps CLI Tool

### Exercise 5.1: Production-Ready CLI Tool

Create `devops_tool.py`:

```python
#!/usr/bin/env python3
"""
DevOps Management Tool

A comprehensive CLI tool for managing DevOps operations.
"""
import click
import logging
import sys
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler


# Configure logging with Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("devops")
console = Console()


# Context object
class Context:
    """Application context."""
    
    def __init__(self):
        self.verbose = False
        self.config_file = None
        self.dry_run = False


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--config', type=click.Path(exists=True), help='Config file path')
@click.option('--dry-run', is_flag=True, help='Perform a dry run')
@click.version_option(version='1.0.0', prog_name='DevOps Tool')
@click.pass_context
def cli(ctx, verbose, config, dry_run):
    """
    DevOps Management Tool
    
    Comprehensive CLI for managing infrastructure, deployments, and operations.
    """
    ctx.obj = Context()
    ctx.obj.verbose = verbose
    ctx.obj.config_file = config
    ctx.obj.dry_run = dry_run
    
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
    
    if dry_run:
        console.print("[yellow]DRY RUN MODE - No changes will be made[/yellow]")


# Server management commands
@cli.group()
def server():
    """Manage servers."""
    pass


@server.command('list')
@click.option('--status', type=click.Choice(['all', 'running', 'stopped']),
              default='all')
@click.pass_context
def server_list(ctx, status):
    """List servers."""
    from rich.table import Table
    
    logger.info(f"Listing servers with status: {status}")
    
    table = Table(title="Servers")
    table.add_column("Name", style="cyan")
    table.add_column("IP", style="green")
    table.add_column("Status")
    table.add_column("Uptime")
    
    # Mock data
    servers = [
        ("web-01", "192.168.1.10", "🟢 Running", "3d"),
        ("web-02", "192.168.1.11", "🟢 Running", "3d"),
        ("db-01", "192.168.1.20", "🔴 Stopped", "-"),
    ]
    
    for server_data in servers:
        table.add_row(*server_data)
    
    console.print(table)


@server.command('start')
@click.argument('name')
@click.pass_context
def server_start(ctx, name):
    """Start a server."""
    if ctx.obj.dry_run:
        console.print(f"[yellow]Would start server: {name}[/yellow]")
        return
    
    logger.info(f"Starting server: {name}")
    console.print(f"[green]✓ Server {name} started[/green]")


# Deployment commands
@cli.group()
def deploy():
    """Manage deployments."""
    pass


@deploy.command('app')
@click.argument('app_name')
@click.option('-e', '--env', type=click.Choice(['dev', 'staging', 'prod']),
              required=True)
@click.option('-v', '--version', help='Version to deploy')
@click.pass_context
def deploy_app(ctx, app_name, env, version):
    """Deploy an application."""
    from rich.progress import Progress
    
    logger.info(f"Deploying {app_name} v{version or 'latest'} to {env}")
    
    if ctx.obj.dry_run:
        console.print("[yellow]Dry run - deployment skipped[/yellow]")
        return
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Deploying...", total=100)
        
        for i in range(100):
            import time
            time.sleep(0.02)
            progress.update(task, advance=1)
    
    console.print(f"[green]✓ {app_name} deployed successfully[/green]")


# Monitoring commands
@cli.group()
def monitor():
    """Monitoring and metrics."""
    pass


@monitor.command('health')
@click.argument('service')
def monitor_health(service):
    """Check service health."""
    from rich.panel import Panel
    
    health_status = {
        'status': 'healthy',
        'uptime': '3 days',
        'response_time': '45ms',
        'error_rate': '0.01%'
    }
    
    status_text = f"""
[green]Status:[/green] {health_status['status']}
[cyan]Uptime:[/cyan] {health_status['uptime']}
[cyan]Response Time:[/cyan] {health_status['response_time']}
[cyan]Error Rate:[/cyan] {health_status['error_rate']}
    """
    
    console.print(Panel(status_text, title=f"Health Check: {service}",
                       border_style="green"))


# Configuration commands
@cli.group()
def config():
    """Manage configuration."""
    pass


@config.command('show')
@click.option('--env', type=click.Choice(['dev', 'staging', 'prod']),
              required=True)
def config_show(env):
    """Show configuration."""
    logger.info(f"Configuration for {env}")
    
    config_data = {
        'DATABASE_URL': 'postgresql://localhost:5432/mydb',
        'REDIS_URL': 'redis://localhost:6379',
        'LOG_LEVEL': 'INFO',
        'MAX_WORKERS': '4'
    }
    
    for key, value in config_data.items():
        console.print(f"[cyan]{key}[/cyan]: {value}")


# Backup commands
@cli.group()
def backup():
    """Backup and restore operations."""
    pass


@backup.command('create')
@click.argument('target')
@click.option('--compress', is_flag=True, help='Compress backup')
def backup_create(target, compress):
    """Create a backup."""
    from rich.progress import Progress
    
    logger.info(f"Creating backup of {target}")
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Backing up...", total=100)
        
        for i in range(100):
            import time
            time.sleep(0.01)
            progress.update(task, advance=1)
    
    backup_file = f"{target}_backup_20240115.tar"
    if compress:
        backup_file += ".gz"
    
    console.print(f"[green]✓ Backup created: {backup_file}[/green]")


@backup.command('list')
def backup_list():
    """List available backups."""
    from rich.table import Table
    
    table = Table(title="Available Backups")
    table.add_column("Name", style="cyan")
    table.add_column("Date", style="green")
    table.add_column("Size")
    
    backups = [
        ("database_backup_20240115.tar.gz", "2024-01-15 10:00", "2.5 GB"),
        ("database_backup_20240114.tar.gz", "2024-01-14 10:00", "2.4 GB"),
        ("database_backup_20240113.tar.gz", "2024-01-13 10:00", "2.3 GB"),
    ]
    
    for backup_data in backups:
        table.add_row(*backup_data)
    
    console.print(table)


if __name__ == '__main__':
    try:
        cli(obj=None)
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled[/yellow]")
        sys.exit(130)
    except Exception as e:
        logger.exception("An error occurred")
        sys.exit(1)
```

**Usage examples:**
```bash
# List servers
python devops_tool.py server list
python devops_tool.py server list --status running

# Start server
python devops_tool.py server start web-01

# Deploy application
python devops_tool.py deploy app my-app -e prod -v 1.2.3

# Check health
python devops_tool.py monitor health my-service

# Show configuration
python devops_tool.py config show --env prod

# Create backup
python devops_tool.py backup create database --compress

# List backups
python devops_tool.py backup list

# Dry run mode
python devops_tool.py --dry-run server start web-01

# Verbose mode
python devops_tool.py -v deploy app my-app -e prod

# Show help
python devops_tool.py --help
python devops_tool.py server --help
python devops_tool.py deploy --help
```

---

## Practice Challenges

### Challenge 1: Log Aggregation Tool
Build a tool that:
- Parses logs from multiple sources
- Aggregates and filters logs
- Generates summary reports
- Exports to different formats

### Challenge 2: Infrastructure CLI
Create a comprehensive CLI for:
- Managing cloud resources
- Deploying applications
- Monitoring services
- Managing backups

### Challenge 3: GitOps Tool
Build a GitOps CLI that:
- Syncs deployments with Git
- Validates configurations
- Manages releases
- Handles rollbacks

### Challenge 4: Monitoring Dashboard
Create a CLI dashboard that:
- Shows real-time metrics
- Displays service health
- Shows resource usage
- Sends alerts

---

## What You Learned

In this lab, you learned:

✅ **Python Logging**
- Using the logging module
- Configuring log levels and formatters
- File and stream handlers
- Rotating log files
- Structured logging

✅ **argparse CLI**
- Creating command-line parsers
- Adding arguments and options
- Implementing subcommands
- Handling user input
- Validation and error handling

✅ **Click Framework**
- Building advanced CLIs
- Command groups and nesting
- Options and arguments
- Confirmation prompts
- Context passing

✅ **Rich Output**
- Formatted tables
- Progress bars
- Panels and trees
- Colored output
- Interactive prompts

✅ **Production Best Practices**
- Error handling
- Logging standards
- User-friendly output
- Configuration management
- Help documentation

## Next Steps

- Build a complete DevOps toolchain
- Integrate with CI/CD pipelines
- Add configuration file support
- Implement plugin architecture
- Create installable packages with setuptools

## Additional Resources

- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [argparse Documentation](https://docs.python.org/3/library/argparse.html)
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Building CLI Tools in Python](https://realpython.com/command-line-interfaces-python-argparse/)
