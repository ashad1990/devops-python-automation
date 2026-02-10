# PROJECT 01: Infrastructure Inventory Tool

## Problem Statement (User Story)
**As a DevOps engineer**, I need a Python tool that connects to GCP, inventories all resources (VMs, disks, networks, buckets), and generates a report in CSV/JSON format, so that I can maintain visibility over infrastructure, track resource sprawl, and support audit compliance requirements.

## Project Objectives
- Build a production-ready Python CLI tool for GCP infrastructure inventory
- Implement multi-project and multi-region resource discovery
- Generate structured reports in multiple formats (CSV, JSON, HTML)
- Support filtering, tagging, and cost estimation
- Demonstrate enterprise-grade error handling and logging
- Create a maintainable, testable codebase suitable for portfolio presentation

## Requirements

### Functional Requirements
1. **Authentication & Authorization**
   - Support GCP service account authentication
   - Handle multiple GCP projects
   - Validate permissions before inventory operations

2. **Resource Discovery**
   - Compute Engine instances (VMs)
   - Persistent disks and snapshots
   - VPC networks and subnets
   - Cloud Storage buckets
   - Load balancers
   - Cloud SQL instances

3. **Reporting**
   - Export to CSV, JSON, and HTML formats
   - Include resource metadata (name, region, status, creation date, labels)
   - Generate summary statistics
   - Support custom filtering (by project, region, resource type)

4. **Data Enrichment**
   - Calculate estimated monthly costs
   - Identify unattached resources (orphaned disks)
   - Flag resources without proper labels/tags
   - Show last modification timestamps

### Non-Functional Requirements
- **Performance**: Handle 1000+ resources within 60 seconds
- **Reliability**: Retry failed API calls with exponential backoff
- **Maintainability**: Follow PEP 8, include type hints, 80%+ test coverage
- **Security**: Never log credentials, support encrypted credential storage
- **Usability**: Clear CLI interface with progress indicators

## Technical Specification

### Features List
- [ ] GCP authentication using service account JSON
- [ ] Multi-project resource enumeration
- [ ] Parallel API calls for performance
- [ ] Multiple output formats (CSV, JSON, HTML)
- [ ] Configurable filters (project, region, resource type, labels)
- [ ] Cost estimation based on resource SKUs
- [ ] Orphaned resource detection
- [ ] Label compliance checking
- [ ] Incremental inventory (only changes since last run)
- [ ] Email/Slack notification support
- [ ] Scheduling support (cron-friendly)
- [ ] Comprehensive logging with rotation

### Suggested Architecture

```
infrastructure-inventory/
├── src/
│   ├── __init__.py
│   ├── main.py                 # CLI entry point
│   ├── inventory/
│   │   ├── __init__.py
│   │   ├── gcp_client.py       # GCP API wrapper
│   │   ├── collectors.py       # Resource collectors
│   │   └── enrichment.py       # Data enrichment logic
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── formatters.py       # CSV/JSON/HTML formatters
│   │   └── templates/          # HTML templates
│   ├── models/
│   │   ├── __init__.py
│   │   └── resources.py        # Dataclasses for resources
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # Configuration management
│       ├── logger.py           # Logging setup
│       └── validators.py       # Input validation
├── tests/
│   ├── __init__.py
│   ├── test_collectors.py
│   ├── test_formatters.py
│   └── fixtures/               # Test data
├── config/
│   └── config.yaml             # Default configuration
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── README.md
└── .env.example
```

### Data Models (Example)

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class ResourceType(Enum):
    COMPUTE_INSTANCE = "compute.instance"
    PERSISTENT_DISK = "compute.disk"
    STORAGE_BUCKET = "storage.bucket"
    VPC_NETWORK = "compute.network"
    CLOUD_SQL = "sql.instance"

class ResourceStatus(Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    TERMINATED = "TERMINATED"
    UNKNOWN = "UNKNOWN"

@dataclass
class GCPResource:
    """Base class for all GCP resources."""
    resource_id: str
    resource_type: ResourceType
    name: str
    project_id: str
    region: str
    zone: Optional[str] = None
    status: ResourceStatus = ResourceStatus.UNKNOWN
    created_at: Optional[datetime] = None
    labels: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)
    estimated_monthly_cost: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert resource to dictionary."""
        return {
            'resource_id': self.resource_id,
            'type': self.resource_type.value,
            'name': self.name,
            'project': self.project_id,
            'region': self.region,
            'zone': self.zone,
            'status': self.status.value,
            'created': self.created_at.isoformat() if self.created_at else None,
            'labels': self.labels,
            'estimated_cost_usd': self.estimated_monthly_cost
        }

@dataclass
class ComputeInstance(GCPResource):
    """Compute Engine instance details."""
    machine_type: str = ""
    disk_size_gb: int = 0
    network_interfaces: List[str] = field(default_factory=list)
    external_ip: Optional[str] = None
    internal_ip: Optional[str] = None
```

## Implementation Guidelines

### Milestone 1: Project Setup & Authentication (Week 1)
**Deliverables:**
- Project structure and virtual environment
- GCP service account authentication
- Basic logging configuration
- CLI framework with argparse/click

**Key Code Example:**
```python
from google.cloud import compute_v1
from google.oauth2 import service_account
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class GCPClient:
    """Wrapper for GCP API clients with authentication."""
    
    def __init__(self, credentials_path: str, project_id: str):
        """
        Initialize GCP client.
        
        Args:
            credentials_path: Path to service account JSON
            project_id: GCP project ID
        """
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        self._compute_client: Optional[compute_v1.InstancesClient] = None
        
    @property
    def compute_client(self) -> compute_v1.InstancesClient:
        """Lazy-load compute client."""
        if not self._compute_client:
            self._compute_client = compute_v1.InstancesClient(
                credentials=self.credentials
            )
        return self._compute_client
    
    def test_connection(self) -> bool:
        """Test GCP API connectivity."""
        try:
            # Try to list zones as connectivity test
            zones_client = compute_v1.ZonesClient(credentials=self.credentials)
            list(zones_client.list(project=self.project_id, max_results=1))
            logger.info(f"Successfully connected to GCP project: {self.project_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to GCP: {e}")
            return False
```

### Milestone 2: Resource Collectors (Week 2)
**Deliverables:**
- Compute instance collector
- Disk and snapshot collector
- Storage bucket collector
- Unit tests with mocked GCP APIs

**Key Code Example:**
```python
from typing import List, Generator
from google.cloud import compute_v1
import logging

logger = logging.getLogger(__name__)

class ComputeInstanceCollector:
    """Collect Compute Engine instances."""
    
    def __init__(self, client: GCPClient):
        self.client = client
        
    def collect_all(self, zones: List[str]) -> Generator[ComputeInstance, None, None]:
        """
        Collect all compute instances across zones.
        
        Args:
            zones: List of zone names to scan
            
        Yields:
            ComputeInstance objects
        """
        for zone in zones:
            try:
                yield from self._collect_zone(zone)
            except Exception as e:
                logger.error(f"Error collecting instances in {zone}: {e}")
                
    def _collect_zone(self, zone: str) -> Generator[ComputeInstance, None, None]:
        """Collect instances from a single zone."""
        logger.info(f"Collecting instances from zone: {zone}")
        
        request = compute_v1.ListInstancesRequest(
            project=self.client.project_id,
            zone=zone
        )
        
        for instance in self.client.compute_client.list(request=request):
            yield self._parse_instance(instance, zone)
            
    def _parse_instance(self, instance: compute_v1.Instance, zone: str) -> ComputeInstance:
        """Parse GCP instance to internal model."""
        # Extract external IP
        external_ip = None
        internal_ip = None
        network_interfaces = []
        
        for iface in instance.network_interfaces:
            if iface.network_i_p:
                internal_ip = iface.network_i_p
            if iface.access_configs:
                for access_config in iface.access_configs:
                    if access_config.nat_i_p:
                        external_ip = access_config.nat_i_p
            network_interfaces.append(iface.network)
        
        return ComputeInstance(
            resource_id=str(instance.id),
            resource_type=ResourceType.COMPUTE_INSTANCE,
            name=instance.name,
            project_id=self.client.project_id,
            region=zone.rsplit('-', 1)[0],
            zone=zone,
            status=ResourceStatus(instance.status),
            created_at=datetime.fromisoformat(instance.creation_timestamp),
            labels=dict(instance.labels) if instance.labels else {},
            machine_type=instance.machine_type.split('/')[-1],
            external_ip=external_ip,
            internal_ip=internal_ip,
            network_interfaces=network_interfaces
        )
```

### Milestone 3: Report Generation (Week 3)
**Deliverables:**
- CSV formatter with proper escaping
- JSON formatter with pretty printing
- HTML formatter with templates
- Summary statistics calculator

**Key Code Example:**
```python
import csv
import json
from typing import List, Dict, Any
from pathlib import Path
from jinja2 import Template

class ReportFormatter:
    """Generate reports in multiple formats."""
    
    @staticmethod
    def to_csv(resources: List[GCPResource], output_path: Path) -> None:
        """Export resources to CSV."""
        if not resources:
            logger.warning("No resources to export")
            return
            
        with output_path.open('w', newline='', encoding='utf-8') as f:
            # Use first resource to determine fields
            fieldnames = list(resources[0].to_dict().keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for resource in resources:
                writer.writerow(resource.to_dict())
                
        logger.info(f"CSV report saved to {output_path}")
    
    @staticmethod
    def to_json(resources: List[GCPResource], output_path: Path, 
                include_summary: bool = True) -> None:
        """Export resources to JSON with optional summary."""
        data: Dict[str, Any] = {
            'total_resources': len(resources),
            'generated_at': datetime.utcnow().isoformat(),
            'resources': [r.to_dict() for r in resources]
        }
        
        if include_summary:
            data['summary'] = ReportFormatter._generate_summary(resources)
        
        with output_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
            
        logger.info(f"JSON report saved to {output_path}")
    
    @staticmethod
    def _generate_summary(resources: List[GCPResource]) -> Dict[str, Any]:
        """Generate summary statistics."""
        from collections import Counter
        
        return {
            'by_type': dict(Counter(r.resource_type.value for r in resources)),
            'by_region': dict(Counter(r.region for r in resources)),
            'by_status': dict(Counter(r.status.value for r in resources)),
            'total_estimated_cost': sum(r.estimated_monthly_cost for r in resources),
            'resources_without_labels': sum(1 for r in resources if not r.labels)
        }
```

### Milestone 4: Advanced Features (Week 4)
**Deliverables:**
- Cost estimation integration
- Orphaned resource detection
- Label compliance checking
- CLI with filtering options

**Key Code Example:**
```python
import click
from pathlib import Path

@click.command()
@click.option('--project', '-p', required=True, help='GCP project ID')
@click.option('--credentials', '-c', type=click.Path(exists=True), 
              required=True, help='Service account JSON path')
@click.option('--output', '-o', type=click.Path(), default='inventory.json',
              help='Output file path')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'html']),
              default='json', help='Output format')
@click.option('--regions', '-r', multiple=True, 
              help='Regions to scan (default: all)')
@click.option('--resource-types', '-t', multiple=True,
              help='Resource types to collect (default: all)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(project: str, credentials: str, output: str, format: str,
         regions: tuple, resource_types: tuple, verbose: bool) -> None:
    """
    GCP Infrastructure Inventory Tool.
    
    Collects and reports on GCP resources across projects and regions.
    """
    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    setup_logging(log_level)
    
    logger.info(f"Starting inventory for project: {project}")
    
    try:
        # Initialize client
        client = GCPClient(credentials, project)
        
        if not client.test_connection():
            raise click.ClickException("Failed to connect to GCP")
        
        # Collect resources
        collector = InventoryCollector(client)
        resources = collector.collect_all(
            regions=list(regions) if regions else None,
            resource_types=list(resource_types) if resource_types else None
        )
        
        # Generate report
        output_path = Path(output)
        if format == 'json':
            ReportFormatter.to_json(resources, output_path)
        elif format == 'csv':
            ReportFormatter.to_csv(resources, output_path)
        elif format == 'html':
            ReportFormatter.to_html(resources, output_path)
        
        click.echo(f"✓ Inventory complete: {len(resources)} resources found")
        click.echo(f"✓ Report saved to: {output_path}")
        
    except Exception as e:
        logger.exception("Inventory failed")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    main()
```

## Project-Specific Requirements

### requirements.txt
```
# GCP SDK
google-cloud-compute==1.14.1
google-cloud-storage==2.10.0
google-cloud-resource-manager==1.10.3

# CLI & Configuration
click==8.1.7
pyyaml==6.0.1
python-dotenv==1.0.0

# Reporting
jinja2==3.1.2
tabulate==0.9.0

# Utilities
tenacity==8.2.3  # Retry logic
tqdm==4.66.1     # Progress bars
```

### requirements-dev.txt
```
# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0

# Code Quality
black==23.12.1
flake8==6.1.0
mypy==1.7.1
pylint==3.0.3

# Type stubs
types-pyyaml==6.0.12.12
```

## Testing Strategy

### Unit Tests
```python
import pytest
from unittest.mock import Mock, patch
from src.inventory.collectors import ComputeInstanceCollector

class TestComputeInstanceCollector:
    """Test compute instance collection."""
    
    @pytest.fixture
    def mock_client(self):
        """Create mock GCP client."""
        client = Mock()
        client.project_id = "test-project"
        return client
    
    @pytest.fixture
    def collector(self, mock_client):
        """Create collector with mock client."""
        return ComputeInstanceCollector(mock_client)
    
    def test_collect_zone_success(self, collector, mock_client):
        """Test successful zone collection."""
        # Mock instance data
        mock_instance = Mock()
        mock_instance.id = "12345"
        mock_instance.name = "test-vm"
        mock_instance.status = "RUNNING"
        
        mock_client.compute_client.list.return_value = [mock_instance]
        
        # Collect
        instances = list(collector._collect_zone("us-central1-a"))
        
        # Assert
        assert len(instances) == 1
        assert instances[0].name == "test-vm"
    
    def test_collect_zone_api_error(self, collector, mock_client):
        """Test handling of API errors."""
        mock_client.compute_client.list.side_effect = Exception("API Error")
        
        # Should not raise, but log error
        instances = list(collector.collect_all(["us-central1-a"]))
        assert len(instances) == 0
```

## Evaluation Criteria

### Must Have (Core Requirements)
- [ ] Authenticates with GCP using service accounts
- [ ] Collects at least 3 resource types (VMs, disks, buckets)
- [ ] Exports to CSV and JSON formats
- [ ] Includes proper error handling and logging
- [ ] Follows PEP 8 style guidelines
- [ ] Includes type hints on all functions
- [ ] Has README with setup and usage instructions
- [ ] Includes at least 10 unit tests with >70% coverage

### Should Have (Enhanced Functionality)
- [ ] Multi-project support
- [ ] Parallel API calls for performance
- [ ] HTML report with dashboard
- [ ] Cost estimation
- [ ] Orphaned resource detection
- [ ] CLI with filtering options
- [ ] Configuration file support
- [ ] Progress indicators

### Nice to Have (Advanced Features)
- [ ] Integration tests with GCP emulator
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Incremental inventory (delta detection)
- [ ] Email/Slack notifications
- [ ] Scheduled execution support
- [ ] Multi-cloud support (AWS/Azure)

## Bonus Features (For Advanced Learners)

1. **Real-time Monitoring Mode**
   - Watch mode that detects new/deleted resources
   - WebSocket-based dashboard for live updates

2. **Cost Optimization Recommendations**
   - Identify idle resources (low CPU/network usage)
   - Suggest right-sizing opportunities
   - Detect unutilized reserved instances

3. **Compliance Scanning**
   - Check against CIS benchmarks
   - Validate security group rules
   - Detect unencrypted resources

4. **Terraform Integration**
   - Generate Terraform import statements
   - Compare live infrastructure vs. Terraform state
   - Detect drift

5. **API Server Mode**
   - REST API for on-demand inventory
   - Authentication with API keys
   - Rate limiting and caching

## Deliverables

### Required Files
1. **Source Code**
   - `src/` directory with modular code
   - Type-hinted functions and classes
   - Comprehensive docstrings (Google or NumPy style)

2. **Documentation**
   - `README.md` with installation, configuration, usage
   - `ARCHITECTURE.md` explaining design decisions
   - Inline code comments where necessary

3. **Tests**
   - Unit tests for all core modules
   - Test fixtures and mocks
   - Coverage report (>70%)

4. **Configuration**
   - `config.yaml.example` with all options documented
   - `.env.example` for credentials
   - `requirements.txt` and `requirements-dev.txt`

5. **Examples**
   - Sample output files (CSV, JSON, HTML)
   - Example service account setup instructions
   - Common usage scenarios

### Presentation/Demo Requirements
- 5-minute video demonstrating:
  - Installation and setup
  - Running inventory against real/demo GCP project
  - Generating reports in multiple formats
  - Filtering and advanced features
  - Code walkthrough of key components

## Success Metrics
- Successfully inventories 100+ resources in <30 seconds
- Generates accurate reports with no data loss
- Handles API failures gracefully (retries, logging)
- Code passes all linters (black, flake8, mypy)
- All tests pass with >70% coverage
- Documentation is clear and complete

## Learning Outcomes
After completing this project, you will be able to:
- Authenticate and interact with GCP APIs using Python
- Design modular, maintainable Python applications
- Implement proper error handling and retry logic
- Generate structured reports in multiple formats
- Write testable code with mocks and fixtures
- Create production-ready CLI tools
- Apply DevOps best practices (logging, configuration management)
- Build portfolio-worthy projects demonstrating cloud automation skills
