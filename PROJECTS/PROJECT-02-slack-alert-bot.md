# PROJECT 02: Slack Alert Bot for System Monitoring

## Problem Statement (User Story)
**As an SRE**, I need a Python bot that monitors system metrics, checks API health endpoints, and sends alerts to Slack/webhook when issues are detected, so that I can proactively respond to incidents, reduce MTTR (Mean Time To Recovery), and maintain high system availability.

## Project Objectives
- Build a production-ready monitoring bot with pluggable checks
- Implement multiple alert channels (Slack, webhooks, email)
- Create configurable alerting rules and thresholds
- Support alert deduplication and rate limiting
- Demonstrate async programming and concurrent health checks
- Build a maintainable system suitable for production deployment

## Requirements

### Functional Requirements
1. **System Metrics Monitoring**
   - CPU usage (per core and aggregate)
   - Memory usage (used, available, swap)
   - Disk usage (per mount point)
   - Network I/O statistics
   - Process monitoring (specific services)

2. **API Health Checks**
   - HTTP/HTTPS endpoint monitoring
   - Response time tracking
   - Status code validation
   - Response body pattern matching
   - SSL certificate expiration checks
   - DNS resolution validation

3. **Alerting**
   - Slack webhook integration with rich formatting
   - Generic webhook support (PagerDuty, Discord, etc.)
   - Email notifications via SMTP
   - Alert severity levels (INFO, WARNING, CRITICAL)
   - Alert deduplication (no spam)
   - Rate limiting and cooldown periods

4. **Configuration**
   - YAML-based configuration
   - Define custom checks and thresholds
   - Schedule check intervals
   - Alert routing based on severity

### Non-Functional Requirements
- **Performance**: Handle 50+ concurrent health checks
- **Reliability**: Self-monitoring with dead man's switch
- **Maintainability**: Plugin architecture for extensibility
- **Security**: Secure credential management
- **Observability**: Comprehensive logging and metrics

## Technical Specification

### Features List
- [ ] System resource monitoring (CPU, memory, disk, network)
- [ ] HTTP/HTTPS endpoint health checks
- [ ] Custom script-based checks
- [ ] Slack notifications with rich formatting
- [ ] Generic webhook support
- [ ] Email notifications
- [ ] Alert deduplication
- [ ] Alert rate limiting
- [ ] Configurable check schedules
- [ ] Alert escalation policies
- [ ] Health check dependencies
- [ ] Historical metrics storage (SQLite)
- [ ] Status dashboard (web UI)
- [ ] Dead man's switch (heartbeat alerts)
- [ ] Docker containerization

### Suggested Architecture

```
slack-alert-bot/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── bot.py                  # Main bot orchestrator
│   ├── monitors/
│   │   ├── __init__.py
│   │   ├── base.py             # Base monitor class
│   │   ├── system_monitor.py   # System metrics
│   │   ├── http_monitor.py     # HTTP health checks
│   │   ├── process_monitor.py  # Process monitoring
│   │   └── custom_monitor.py   # Custom script checks
│   ├── alerters/
│   │   ├── __init__.py
│   │   ├── base.py             # Base alerter class
│   │   ├── slack_alerter.py    # Slack integration
│   │   ├── webhook_alerter.py  # Generic webhooks
│   │   └── email_alerter.py    # Email alerts
│   ├── models/
│   │   ├── __init__.py
│   │   ├── alert.py            # Alert dataclass
│   │   └── check_result.py     # Check result model
│   ├── scheduler/
│   │   ├── __init__.py
│   │   └── job_scheduler.py    # Task scheduling
│   ├── storage/
│   │   ├── __init__.py
│   │   └── metrics_store.py    # SQLite metrics storage
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # Config management
│       ├── logger.py           # Logging setup
│       └── deduplicator.py     # Alert deduplication
├── config/
│   ├── config.yaml             # Main configuration
│   └── checks.yaml             # Check definitions
├── tests/
│   ├── __init__.py
│   ├── test_monitors.py
│   ├── test_alerters.py
│   └── test_deduplication.py
├── dashboard/                  # Optional web dashboard
│   ├── app.py
│   └── templates/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Data Models

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any

class Severity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class CheckStatus(Enum):
    """Health check status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class CheckResult:
    """Result of a health check."""
    check_name: str
    status: CheckStatus
    severity: Severity
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metrics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def should_alert(self) -> bool:
        """Determine if this result should trigger an alert."""
        return self.status in [CheckStatus.DEGRADED, CheckStatus.UNHEALTHY]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'check_name': self.check_name,
            'status': self.status.value,
            'severity': self.severity.value,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'metrics': self.metrics,
            'metadata': self.metadata
        }

@dataclass
class Alert:
    """Alert to be sent to notification channels."""
    title: str
    message: str
    severity: Severity
    check_result: CheckResult
    alert_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)
    
    def get_color(self) -> str:
        """Get color for Slack attachment."""
        colors = {
            Severity.INFO: "#36a64f",
            Severity.WARNING: "#ff9900",
            Severity.CRITICAL: "#ff0000"
        }
        return colors.get(self.severity, "#808080")
```

## Implementation Guidelines

### Milestone 1: Project Setup & System Monitoring (Week 1)
**Deliverables:**
- Project structure and dependencies
- Configuration management
- System metrics monitoring (CPU, memory, disk)
- Basic logging

**Key Code Example:**
```python
import psutil
from typing import Dict, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

class SystemMonitor:
    """Monitor system resources."""
    
    def __init__(self, thresholds: Dict[str, float]):
        """
        Initialize system monitor.
        
        Args:
            thresholds: Dictionary of metric thresholds
                {
                    'cpu_percent': 80.0,
                    'memory_percent': 85.0,
                    'disk_percent': 90.0
                }
        """
        self.thresholds = thresholds
    
    def check_cpu(self) -> CheckResult:
        """Check CPU usage."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            per_cpu = psutil.cpu_percent(interval=1, percpu=True)
            
            threshold = self.thresholds.get('cpu_percent', 80.0)
            
            if cpu_percent >= threshold:
                status = CheckStatus.UNHEALTHY
                severity = Severity.CRITICAL if cpu_percent >= 95 else Severity.WARNING
                message = f"CPU usage is {cpu_percent:.1f}% (threshold: {threshold}%)"
            else:
                status = CheckStatus.HEALTHY
                severity = Severity.INFO
                message = f"CPU usage is normal: {cpu_percent:.1f}%"
            
            return CheckResult(
                check_name="system.cpu",
                status=status,
                severity=severity,
                message=message,
                metrics={
                    'cpu_percent': cpu_percent,
                    'cpu_count': psutil.cpu_count(),
                    **{f'cpu{i}_percent': val for i, val in enumerate(per_cpu)}
                }
            )
        except Exception as e:
            logger.error(f"CPU check failed: {e}")
            return CheckResult(
                check_name="system.cpu",
                status=CheckStatus.UNKNOWN,
                severity=Severity.WARNING,
                message=f"Failed to check CPU: {str(e)}"
            )
    
    def check_memory(self) -> CheckResult:
        """Check memory usage."""
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            threshold = self.thresholds.get('memory_percent', 85.0)
            
            if mem.percent >= threshold:
                status = CheckStatus.UNHEALTHY
                severity = Severity.CRITICAL if mem.percent >= 95 else Severity.WARNING
                message = f"Memory usage is {mem.percent:.1f}% (threshold: {threshold}%)"
            else:
                status = CheckStatus.HEALTHY
                severity = Severity.INFO
                message = f"Memory usage is normal: {mem.percent:.1f}%"
            
            return CheckResult(
                check_name="system.memory",
                status=status,
                severity=severity,
                message=message,
                metrics={
                    'memory_percent': mem.percent,
                    'memory_used_gb': mem.used / (1024**3),
                    'memory_available_gb': mem.available / (1024**3),
                    'memory_total_gb': mem.total / (1024**3),
                    'swap_percent': swap.percent
                }
            )
        except Exception as e:
            logger.error(f"Memory check failed: {e}")
            return CheckResult(
                check_name="system.memory",
                status=CheckStatus.UNKNOWN,
                severity=Severity.WARNING,
                message=f"Failed to check memory: {str(e)}"
            )
    
    def check_disk(self, mount_points: List[str] = None) -> List[CheckResult]:
        """
        Check disk usage for mount points.
        
        Args:
            mount_points: List of mount points to check. If None, checks all.
        """
        results = []
        
        if mount_points is None:
            mount_points = [p.mountpoint for p in psutil.disk_partitions()]
        
        threshold = self.thresholds.get('disk_percent', 90.0)
        
        for mount in mount_points:
            try:
                usage = psutil.disk_usage(mount)
                
                if usage.percent >= threshold:
                    status = CheckStatus.UNHEALTHY
                    severity = Severity.CRITICAL if usage.percent >= 95 else Severity.WARNING
                    message = f"Disk {mount} usage is {usage.percent:.1f}% (threshold: {threshold}%)"
                else:
                    status = CheckStatus.HEALTHY
                    severity = Severity.INFO
                    message = f"Disk {mount} usage is normal: {usage.percent:.1f}%"
                
                results.append(CheckResult(
                    check_name=f"system.disk.{mount.replace('/', '_')}",
                    status=status,
                    severity=severity,
                    message=message,
                    metrics={
                        'disk_percent': usage.percent,
                        'disk_used_gb': usage.used / (1024**3),
                        'disk_free_gb': usage.free / (1024**3),
                        'disk_total_gb': usage.total / (1024**3)
                    },
                    metadata={'mount_point': mount}
                ))
            except Exception as e:
                logger.error(f"Disk check failed for {mount}: {e}")
                results.append(CheckResult(
                    check_name=f"system.disk.{mount.replace('/', '_')}",
                    status=CheckStatus.UNKNOWN,
                    severity=Severity.WARNING,
                    message=f"Failed to check disk {mount}: {str(e)}"
                ))
        
        return results
```

### Milestone 2: HTTP Health Checks (Week 2)
**Deliverables:**
- HTTP/HTTPS endpoint monitoring
- Response time tracking
- SSL certificate validation
- Async concurrent checks

**Key Code Example:**
```python
import aiohttp
import asyncio
from typing import Dict, Optional
from datetime import datetime, timedelta
import ssl
import socket
from urllib.parse import urlparse

class HTTPMonitor:
    """Monitor HTTP/HTTPS endpoints."""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize HTTP monitor.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
    
    async def check_endpoint(
        self,
        url: str,
        expected_status: int = 200,
        expected_pattern: Optional[str] = None,
        check_ssl: bool = True
    ) -> CheckResult:
        """
        Check HTTP endpoint health.
        
        Args:
            url: URL to check
            expected_status: Expected HTTP status code
            expected_pattern: Optional regex pattern to match in response
            check_ssl: Whether to validate SSL certificate
        """
        start_time = datetime.utcnow()
        
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, ssl=check_ssl) as response:
                    response_time = (datetime.utcnow() - start_time).total_seconds()
                    
                    # Check status code
                    status_ok = response.status == expected_status
                    
                    # Check response pattern if specified
                    pattern_ok = True
                    if expected_pattern:
                        body = await response.text()
                        import re
                        pattern_ok = bool(re.search(expected_pattern, body))
                    
                    # Determine overall health
                    if status_ok and pattern_ok:
                        status = CheckStatus.HEALTHY
                        severity = Severity.INFO
                        message = f"{url} is healthy (status: {response.status}, response_time: {response_time:.2f}s)"
                    else:
                        status = CheckStatus.UNHEALTHY
                        severity = Severity.CRITICAL
                        reasons = []
                        if not status_ok:
                            reasons.append(f"status {response.status} != {expected_status}")
                        if not pattern_ok:
                            reasons.append("pattern not found")
                        message = f"{url} is unhealthy: {', '.join(reasons)}"
                    
                    # Check SSL certificate expiration if HTTPS
                    ssl_days_remaining = None
                    if url.startswith('https://') and check_ssl:
                        ssl_days_remaining = await self._check_ssl_expiry(url)
                    
                    return CheckResult(
                        check_name=f"http.{urlparse(url).netloc}",
                        status=status,
                        severity=severity,
                        message=message,
                        metrics={
                            'response_time_seconds': response_time,
                            'status_code': response.status,
                            'ssl_days_remaining': ssl_days_remaining
                        },
                        metadata={
                            'url': url,
                            'expected_status': expected_status
                        }
                    )
        
        except asyncio.TimeoutError:
            return CheckResult(
                check_name=f"http.{urlparse(url).netloc}",
                status=CheckStatus.UNHEALTHY,
                severity=Severity.CRITICAL,
                message=f"{url} timeout after {self.timeout}s",
                metadata={'url': url}
            )
        except Exception as e:
            return CheckResult(
                check_name=f"http.{urlparse(url).netloc}",
                status=CheckStatus.UNHEALTHY,
                severity=Severity.CRITICAL,
                message=f"{url} check failed: {str(e)}",
                metadata={'url': url, 'error': str(e)}
            )
    
    async def _check_ssl_expiry(self, url: str) -> Optional[int]:
        """Check SSL certificate expiration."""
        try:
            hostname = urlparse(url).netloc
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
            # Parse expiration date
            expires = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_remaining = (expires - datetime.utcnow()).days
            
            return days_remaining
        except Exception as e:
            logger.warning(f"SSL check failed for {url}: {e}")
            return None
```

### Milestone 3: Slack Integration & Alerting (Week 3)
**Deliverables:**
- Slack webhook integration with rich formatting
- Alert deduplication logic
- Rate limiting
- Multiple alert channels

**Key Code Example:**
```python
import aiohttp
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import hashlib
import json

class SlackAlerter:
    """Send alerts to Slack."""
    
    def __init__(self, webhook_url: str, channel: Optional[str] = None):
        """
        Initialize Slack alerter.
        
        Args:
            webhook_url: Slack webhook URL
            channel: Optional channel override
        """
        self.webhook_url = webhook_url
        self.channel = channel
    
    async def send_alert(self, alert: Alert) -> bool:
        """
        Send alert to Slack.
        
        Args:
            alert: Alert object to send
            
        Returns:
            True if sent successfully
        """
        payload = self._build_payload(alert)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 200:
                        logger.info(f"Alert sent to Slack: {alert.title}")
                        return True
                    else:
                        logger.error(f"Slack returned {response.status}: {await response.text()}")
                        return False
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            return False
    
    def _build_payload(self, alert: Alert) -> Dict:
        """Build Slack message payload."""
        # Emoji based on severity
        emoji_map = {
            Severity.INFO: ":information_source:",
            Severity.WARNING: ":warning:",
            Severity.CRITICAL: ":rotating_light:"
        }
        
        emoji = emoji_map.get(alert.severity, ":grey_question:")
        
        # Build rich attachment
        attachment = {
            "color": alert.get_color(),
            "title": f"{emoji} {alert.title}",
            "text": alert.message,
            "fields": [
                {
                    "title": "Severity",
                    "value": alert.severity.value.upper(),
                    "short": True
                },
                {
                    "title": "Check",
                    "value": alert.check_result.check_name,
                    "short": True
                },
                {
                    "title": "Status",
                    "value": alert.check_result.status.value.upper(),
                    "short": True
                },
                {
                    "title": "Timestamp",
                    "value": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "short": True
                }
            ],
            "footer": "Monitoring Bot",
            "ts": int(alert.timestamp.timestamp())
        }
        
        # Add metrics if present
        if alert.check_result.metrics:
            metrics_str = "\n".join([
                f"• *{k}*: {v:.2f}" if isinstance(v, float) else f"• *{k}*: {v}"
                for k, v in alert.check_result.metrics.items()
            ])
            attachment["fields"].append({
                "title": "Metrics",
                "value": metrics_str,
                "short": False
            })
        
        payload = {
            "attachments": [attachment]
        }
        
        if self.channel:
            payload["channel"] = self.channel
        
        return payload


class AlertDeduplicator:
    """Prevent duplicate alerts."""
    
    def __init__(self, window_minutes: int = 60):
        """
        Initialize deduplicator.
        
        Args:
            window_minutes: Time window for deduplication
        """
        self.window = timedelta(minutes=window_minutes)
        self.seen_alerts: Dict[str, datetime] = {}
    
    def should_send(self, alert: Alert) -> bool:
        """
        Check if alert should be sent.
        
        Args:
            alert: Alert to check
            
        Returns:
            True if alert should be sent
        """
        # Generate fingerprint for alert
        fingerprint = self._generate_fingerprint(alert)
        
        now = datetime.utcnow()
        
        # Check if we've seen this alert recently
        if fingerprint in self.seen_alerts:
            last_sent = self.seen_alerts[fingerprint]
            if now - last_sent < self.window:
                logger.debug(f"Suppressing duplicate alert: {alert.title}")
                return False
        
        # Update last sent time
        self.seen_alerts[fingerprint] = now
        
        # Cleanup old entries
        self._cleanup_old_entries(now)
        
        return True
    
    def _generate_fingerprint(self, alert: Alert) -> str:
        """Generate unique fingerprint for alert."""
        # Use check name and severity for fingerprint
        data = f"{alert.check_result.check_name}:{alert.severity.value}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def _cleanup_old_entries(self, now: datetime) -> None:
        """Remove old entries from seen_alerts."""
        cutoff = now - self.window * 2  # Keep 2x window for safety
        
        to_remove = [
            fp for fp, ts in self.seen_alerts.items()
            if ts < cutoff
        ]
        
        for fp in to_remove:
            del self.seen_alerts[fp]
```

### Milestone 4: Orchestration & Configuration (Week 4)
**Deliverables:**
- Main bot orchestrator
- YAML configuration
- Scheduling system
- Complete CLI

**Key Code Example:**
```python
import asyncio
from typing import List, Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import yaml

class MonitoringBot:
    """Main monitoring bot orchestrator."""
    
    def __init__(self, config_path: str):
        """
        Initialize monitoring bot.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.scheduler = AsyncIOScheduler()
        self.monitors: Dict[str, Any] = {}
        self.alerters: List[BaseAlerter] = []
        self.deduplicator = AlertDeduplicator(
            window_minutes=self.config.get('alert_dedup_window', 60)
        )
        
        self._setup_monitors()
        self._setup_alerters()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _setup_monitors(self) -> None:
        """Initialize monitors based on config."""
        # System monitor
        if 'system' in self.config.get('monitors', {}):
            self.monitors['system'] = SystemMonitor(
                thresholds=self.config['monitors']['system'].get('thresholds', {})
            )
        
        # HTTP monitor
        if 'http' in self.config.get('monitors', {}):
            self.monitors['http'] = HTTPMonitor(
                timeout=self.config['monitors']['http'].get('timeout', 10)
            )
    
    def _setup_alerters(self) -> None:
        """Initialize alerters based on config."""
        alerters_config = self.config.get('alerters', {})
        
        # Slack
        if 'slack' in alerters_config:
            self.alerters.append(SlackAlerter(
                webhook_url=alerters_config['slack']['webhook_url'],
                channel=alerters_config['slack'].get('channel')
            ))
        
        # Email
        if 'email' in alerters_config:
            self.alerters.append(EmailAlerter(
                smtp_server=alerters_config['email']['smtp_server'],
                from_addr=alerters_config['email']['from'],
                to_addrs=alerters_config['email']['to']
            ))
    
    async def run_checks(self) -> None:
        """Run all configured checks."""
        logger.info("Running health checks...")
        
        results: List[CheckResult] = []
        
        # System checks
        if 'system' in self.monitors:
            results.append(self.monitors['system'].check_cpu())
            results.append(self.monitors['system'].check_memory())
            results.extend(self.monitors['system'].check_disk())
        
        # HTTP checks
        if 'http' in self.monitors:
            http_checks = self.config['monitors']['http'].get('endpoints', [])
            http_tasks = [
                self.monitors['http'].check_endpoint(**check)
                for check in http_checks
            ]
            results.extend(await asyncio.gather(*http_tasks))
        
        # Process results and send alerts
        await self._process_results(results)
    
    async def _process_results(self, results: List[CheckResult]) -> None:
        """Process check results and send alerts."""
        for result in results:
            if result.should_alert():
                alert = Alert(
                    title=f"Alert: {result.check_name}",
                    message=result.message,
                    severity=result.severity,
                    check_result=result
                )
                
                # Check deduplication
                if self.deduplicator.should_send(alert):
                    # Send to all alerters
                    await self._send_alert(alert)
    
    async def _send_alert(self, alert: Alert) -> None:
        """Send alert to all configured channels."""
        tasks = [alerter.send_alert(alert) for alerter in self.alerters]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def start(self) -> None:
        """Start the monitoring bot."""
        logger.info("Starting monitoring bot...")
        
        # Schedule periodic checks
        check_interval = self.config.get('check_interval_seconds', 60)
        self.scheduler.add_job(
            self.run_checks,
            'interval',
            seconds=check_interval,
            id='health_checks'
        )
        
        # Start scheduler
        self.scheduler.start()
        
        logger.info(f"Bot started. Checks running every {check_interval}s")
        
        # Keep running
        try:
            asyncio.get_event_loop().run_forever()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Shutting down...")
            self.scheduler.shutdown()


# CLI entry point
import click

@click.command()
@click.option('--config', '-c', default='config/config.yaml',
              help='Path to configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(config: str, verbose: bool) -> None:
    """
    Start the monitoring bot.
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    setup_logging(log_level)
    
    bot = MonitoringBot(config)
    bot.start()

if __name__ == '__main__':
    main()
```

## Project-Specific Requirements

### requirements.txt
```
# HTTP & Async
aiohttp==3.9.1
aiohttp-retry==2.8.3

# System Monitoring
psutil==5.9.6

# Scheduling
apscheduler==3.10.4

# Configuration
pyyaml==6.0.1
python-dotenv==1.0.0

# Email (optional)
aiosmtplib==3.0.1

# CLI
click==8.1.7

# Utilities
tenacity==8.2.3
```

### requirements-dev.txt
```
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
aioresponses==0.7.6

# Code Quality
black==23.12.1
flake8==6.1.0
mypy==1.7.1
pylint==3.0.3
```

### Example Configuration (config/config.yaml)
```yaml
# Monitoring Bot Configuration

# Check interval (seconds)
check_interval_seconds: 60

# Alert deduplication window (minutes)
alert_dedup_window: 60

# Monitors
monitors:
  system:
    enabled: true
    thresholds:
      cpu_percent: 80.0
      memory_percent: 85.0
      disk_percent: 90.0
    
  http:
    enabled: true
    timeout: 10
    endpoints:
      - url: https://api.example.com/health
        expected_status: 200
        expected_pattern: '"status":\s*"ok"'
        check_ssl: true
      
      - url: https://www.google.com
        expected_status: 200
        check_ssl: true

# Alerters
alerters:
  slack:
    enabled: true
    webhook_url: ${SLACK_WEBHOOK_URL}
    channel: "#alerts"
  
  email:
    enabled: false
    smtp_server: smtp.gmail.com:587
    from: alerts@example.com
    to:
      - devops@example.com

# Logging
logging:
  level: INFO
  file: /var/log/monitoring-bot.log
```

## Testing Strategy

### Unit Tests
```python
import pytest
from aioresponses import aioresponses
from src.monitors.http_monitor import HTTPMonitor
from src.models.check_result import CheckStatus, Severity

@pytest.mark.asyncio
async def test_http_check_success():
    """Test successful HTTP check."""
    monitor = HTTPMonitor(timeout=5)
    
    with aioresponses() as mock:
        mock.get('https://api.example.com/health', status=200, body='OK')
        
        result = await monitor.check_endpoint(
            url='https://api.example.com/health',
            expected_status=200
        )
        
        assert result.status == CheckStatus.HEALTHY
        assert result.severity == Severity.INFO
        assert 'response_time_seconds' in result.metrics

@pytest.mark.asyncio
async def test_http_check_failure():
    """Test failed HTTP check."""
    monitor = HTTPMonitor(timeout=5)
    
    with aioresponses() as mock:
        mock.get('https://api.example.com/health', status=500)
        
        result = await monitor.check_endpoint(
            url='https://api.example.com/health',
            expected_status=200
        )
        
        assert result.status == CheckStatus.UNHEALTHY
        assert result.severity == Severity.CRITICAL
```

## Evaluation Criteria

### Must Have
- [ ] Monitors CPU, memory, disk usage
- [ ] Performs HTTP health checks with async
- [ ] Sends alerts to Slack with rich formatting
- [ ] Implements alert deduplication
- [ ] YAML configuration support
- [ ] Proper error handling and logging
- [ ] Type hints and PEP 8 compliance
- [ ] >70% test coverage
- [ ] README with setup instructions

### Should Have
- [ ] Multiple alert channels (Slack + email/webhook)
- [ ] Configurable check schedules
- [ ] SSL certificate expiration checks
- [ ] Rate limiting for alerts
- [ ] Metrics storage (SQLite)
- [ ] Docker containerization
- [ ] Dead man's switch feature

### Nice to Have
- [ ] Web dashboard for status
- [ ] Alert escalation policies
- [ ] Custom script-based checks
- [ ] Process monitoring
- [ ] Integration tests
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment manifests

## Bonus Features

1. **Web Dashboard**
   - Real-time status display
   - Historical metrics charts
   - Alert history

2. **Advanced Alerting**
   - Alert escalation (if not acknowledged)
   - On-call rotation integration
   - Incident grouping

3. **Machine Learning**
   - Anomaly detection
   - Predictive alerting
   - Auto-tuning thresholds

4. **Multi-Cloud**
   - AWS CloudWatch integration
   - Azure Monitor integration
   - Datadog/Prometheus exporters

5. **ChatOps**
   - Slash commands in Slack
   - Acknowledge alerts from chat
   - Query metrics from chat

## Deliverables

1. Source code with modular architecture
2. Comprehensive documentation
3. Unit and integration tests
4. Docker container and docker-compose setup
5. Example configurations
6. Demo video showing:
   - Bot startup and configuration
   - Triggering alerts (high CPU, failed endpoint)
   - Slack notifications
   - Deduplication in action

## Success Metrics
- Detects and alerts on issues within check interval
- Zero false negatives (catches all actual issues)
- Minimal false positives (<5%)
- Handles 50+ concurrent checks
- Alert deduplication works correctly
- No crashes under normal operation

## Learning Outcomes
- Async programming with asyncio
- System monitoring with psutil
- Slack integration and webhooks
- Alert management patterns
- Scheduling and orchestration
- Production monitoring best practices
- Building resilient distributed systems
