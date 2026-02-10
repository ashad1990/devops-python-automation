# PROJECT 05: Cloud Cost Analyzer

## Problem Statement (User Story)
**As a DevOps engineer**, I need a Python script that pulls GCP billing data, analyzes costs by project/service, identifies cost anomalies, and generates weekly reports, so that I can optimize cloud spending, prevent budget overruns, and provide stakeholders with clear cost visibility and recommendations.

## Project Objectives
- Build a production-ready cloud cost analysis tool
- Integrate with GCP Billing API for cost data extraction
- Implement intelligent cost anomaly detection
- Generate comprehensive cost reports with visualizations
- Provide actionable cost optimization recommendations
- Demonstrate data analysis and FinOps best practices

## Requirements

### Functional Requirements
1. **Cost Data Collection**
   - Pull billing data from GCP Billing Export (BigQuery)
   - Support multiple billing accounts
   - Historical cost analysis (daily, weekly, monthly)
   - Real-time cost tracking
   - Multi-currency support

2. **Cost Analysis**
   - Cost breakdown by project
   - Cost breakdown by service/SKU
   - Cost breakdown by region/zone
   - Cost breakdown by labels/tags
   - Cost trends and forecasting
   - Budget vs. actual analysis

3. **Anomaly Detection**
   - Detect unusual spending spikes
   - Identify cost increases >X%
   - Alert on budget threshold breaches
   - Compare costs week-over-week, month-over-month
   - Machine learning-based anomaly detection

4. **Reporting**
   - Weekly/monthly cost reports
   - Cost visualization (charts, graphs)
   - Export to PDF, HTML, email
   - Interactive dashboards
   - Executive summaries

5. **Optimization Recommendations**
   - Identify idle resources
   - Right-sizing recommendations
   - Reserved instance opportunities
   - Commitment discount analysis
   - Unattached disk detection

### Non-Functional Requirements
- **Performance**: Process millions of billing records efficiently
- **Accuracy**: 99.9% accuracy in cost calculations
- **Scalability**: Handle multiple GCP organizations
- **Security**: Secure API credentials, audit logging
- **Maintainability**: Modular, testable code

## Technical Specification

### Features List
- [ ] GCP BigQuery billing export integration
- [ ] Multi-project cost aggregation
- [ ] Cost breakdown by multiple dimensions
- [ ] Trend analysis and forecasting
- [ ] Anomaly detection algorithms
- [ ] Budget tracking and alerts
- [ ] Weekly automated reports
- [ ] Cost visualization (charts/graphs)
- [ ] PDF/HTML report generation
- [ ] Email report delivery
- [ ] Slack/webhook notifications
- [ ] Cost optimization recommendations
- [ ] Idle resource detection
- [ ] Reserved instance analysis
- [ ] Interactive web dashboard
- [ ] Historical cost comparison

### Suggested Architecture

```
cloud-cost-analyzer/
├── src/
│   ├── __init__.py
│   ├── main.py                    # CLI entry point
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base.py                # Base collector
│   │   ├── gcp_billing.py         # GCP BigQuery billing
│   │   └── gcp_usage.py           # GCP resource usage
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── cost_analyzer.py       # Cost analysis
│   │   ├── trend_analyzer.py      # Trend analysis
│   │   ├── anomaly_detector.py    # Anomaly detection
│   │   └── budget_tracker.py      # Budget tracking
│   ├── optimizers/
│   │   ├── __init__.py
│   │   ├── base.py                # Base optimizer
│   │   ├── compute_optimizer.py   # Compute recommendations
│   │   ├── storage_optimizer.py   # Storage recommendations
│   │   └── commitment_optimizer.py # Commitment recommendations
│   ├── reporters/
│   │   ├── __init__.py
│   │   ├── report_generator.py    # Report generator
│   │   ├── visualizer.py          # Chart generation
│   │   ├── pdf_exporter.py        # PDF export
│   │   └── email_sender.py        # Email delivery
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cost_record.py         # Cost data models
│   │   ├── anomaly.py             # Anomaly models
│   │   └── recommendation.py      # Recommendation models
│   ├── dashboard/                 # Optional web dashboard
│   │   ├── app.py                 # Flask/FastAPI app
│   │   └── templates/
│   └── utils/
│       ├── __init__.py
│       ├── config.py              # Configuration
│       ├── logger.py              # Logging
│       └── bigquery.py            # BigQuery utils
├── config/
│   └── config.yaml                # Configuration
├── templates/
│   ├── email_template.html
│   └── report_template.html
├── tests/
│   ├── __init__.py
│   ├── test_collectors.py
│   ├── test_analyzers.py
│   └── fixtures/
├── requirements.txt
├── Dockerfile
└── README.md
```

### Data Models

```python
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from enum import Enum
from decimal import Decimal

class CostGranularity(Enum):
    """Cost data granularity."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class AnomalyType(Enum):
    """Type of cost anomaly."""
    SPIKE = "spike"
    DROP = "drop"
    TREND_CHANGE = "trend_change"
    BUDGET_BREACH = "budget_breach"

class RecommendationType(Enum):
    """Type of optimization recommendation."""
    RIGHT_SIZING = "right_sizing"
    IDLE_RESOURCE = "idle_resource"
    RESERVED_INSTANCE = "reserved_instance"
    COMMITMENT_DISCOUNT = "commitment_discount"
    STORAGE_CLASS = "storage_class"
    REGION_OPTIMIZATION = "region_optimization"

@dataclass
class CostRecord:
    """Individual cost record."""
    date: date
    project_id: str
    service: str
    sku: str
    region: str
    cost: Decimal
    currency: str = "USD"
    usage_amount: Optional[Decimal] = None
    usage_unit: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'date': self.date.isoformat(),
            'project_id': self.project_id,
            'service': self.service,
            'sku': self.sku,
            'region': self.region,
            'cost': float(self.cost),
            'currency': self.currency,
            'usage_amount': float(self.usage_amount) if self.usage_amount else None,
            'usage_unit': self.usage_unit,
            'labels': self.labels
        }

@dataclass
class CostSummary:
    """Aggregated cost summary."""
    period_start: date
    period_end: date
    total_cost: Decimal
    currency: str = "USD"
    by_project: Dict[str, Decimal] = field(default_factory=dict)
    by_service: Dict[str, Decimal] = field(default_factory=dict)
    by_region: Dict[str, Decimal] = field(default_factory=dict)
    
    def get_top_projects(self, n: int = 5) -> List[tuple[str, Decimal]]:
        """Get top N projects by cost."""
        return sorted(
            self.by_project.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n]
    
    def get_top_services(self, n: int = 5) -> List[tuple[str, Decimal]]:
        """Get top N services by cost."""
        return sorted(
            self.by_service.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n]

@dataclass
class CostAnomaly:
    """Detected cost anomaly."""
    anomaly_id: str
    anomaly_type: AnomalyType
    date: date
    project_id: str
    service: str
    expected_cost: Decimal
    actual_cost: Decimal
    deviation_percent: float
    severity: str  # "low", "medium", "high", "critical"
    description: str
    
    def get_cost_difference(self) -> Decimal:
        """Get absolute cost difference."""
        return abs(self.actual_cost - self.expected_cost)
    
    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"{self.severity.upper()} {self.anomaly_type.value}: "
            f"{self.service} in {self.project_id} - "
            f"${self.actual_cost:.2f} (expected ${self.expected_cost:.2f}, "
            f"{self.deviation_percent:+.1f}%)"
        )

@dataclass
class CostOptimization:
    """Cost optimization recommendation."""
    recommendation_id: str
    recommendation_type: RecommendationType
    resource_id: str
    resource_type: str
    project_id: str
    current_cost_monthly: Decimal
    potential_savings_monthly: Decimal
    confidence: float  # 0.0 to 1.0
    description: str
    action_items: List[str] = field(default_factory=list)
    
    def get_annual_savings(self) -> Decimal:
        """Calculate annual savings."""
        return self.potential_savings_monthly * 12
    
    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"{self.recommendation_type.value}: {self.description} - "
            f"Save ${self.potential_savings_monthly:.2f}/month "
            f"(${self.get_annual_savings():.2f}/year)"
        )

@dataclass
class CostReport:
    """Cost analysis report."""
    report_id: str
    generated_at: datetime
    period_start: date
    period_end: date
    summary: CostSummary
    anomalies: List[CostAnomaly] = field(default_factory=list)
    recommendations: List[CostOptimization] = field(default_factory=list)
    
    def get_total_savings_potential(self) -> Decimal:
        """Calculate total potential monthly savings."""
        return sum(r.potential_savings_monthly for r in self.recommendations)
```

## Implementation Guidelines

### Milestone 1: GCP Billing Integration (Week 1)
**Deliverables:**
- BigQuery billing export integration
- Cost data extraction
- Data transformation and aggregation
- Basic cost summary

**Key Code Example:**
```python
from google.cloud import bigquery
from google.oauth2 import service_account
from typing import List, Optional
from datetime import date, datetime, timedelta
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class GCPBillingCollector:
    """Collect billing data from GCP BigQuery."""
    
    def __init__(
        self,
        credentials_path: str,
        billing_project_id: str,
        billing_dataset: str,
        billing_table: str
    ):
        """
        Initialize GCP billing collector.
        
        Args:
            credentials_path: Path to service account JSON
            billing_project_id: Project containing billing export
            billing_dataset: BigQuery dataset name
            billing_table: BigQuery table name
        """
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        
        self.client = bigquery.Client(
            credentials=credentials,
            project=billing_project_id
        )
        
        self.table_id = f"{billing_project_id}.{billing_dataset}.{billing_table}"
    
    def get_cost_records(
        self,
        start_date: date,
        end_date: date,
        project_filter: Optional[List[str]] = None
    ) -> List[CostRecord]:
        """
        Fetch cost records for a date range.
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            project_filter: Optional list of project IDs to filter
            
        Returns:
            List of cost records
        """
        logger.info(f"Fetching costs from {start_date} to {end_date}")
        
        query = f"""
        SELECT
            DATE(usage_start_time) as date,
            project.id as project_id,
            service.description as service,
            sku.description as sku,
            location.region as region,
            SUM(cost) as cost,
            currency,
            SUM(usage.amount) as usage_amount,
            usage.unit as usage_unit,
            labels
        FROM
            `{self.table_id}`
        WHERE
            DATE(usage_start_time) BETWEEN @start_date AND @end_date
            AND cost > 0
        """
        
        if project_filter:
            projects_str = "', '".join(project_filter)
            query += f" AND project.id IN ('{projects_str}')"
        
        query += """
        GROUP BY
            date, project_id, service, sku, region, currency, usage_unit, labels
        ORDER BY
            date DESC, cost DESC
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
                bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
            ]
        )
        
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()
        
        cost_records = []
        
        for row in results:
            # Parse labels
            labels = {}
            if row.labels:
                for label in row.labels:
                    labels[label['key']] = label['value']
            
            record = CostRecord(
                date=row.date,
                project_id=row.project_id,
                service=row.service,
                sku=row.sku,
                region=row.region or "global",
                cost=Decimal(str(row.cost)),
                currency=row.currency,
                usage_amount=Decimal(str(row.usage_amount)) if row.usage_amount else None,
                usage_unit=row.usage_unit,
                labels=labels
            )
            
            cost_records.append(record)
        
        logger.info(f"Fetched {len(cost_records)} cost records")
        
        return cost_records
    
    def get_cost_summary(
        self,
        start_date: date,
        end_date: date,
        project_filter: Optional[List[str]] = None
    ) -> CostSummary:
        """
        Get aggregated cost summary.
        
        Args:
            start_date: Start date
            end_date: End date
            project_filter: Optional project filter
            
        Returns:
            Cost summary
        """
        records = self.get_cost_records(start_date, end_date, project_filter)
        
        summary = CostSummary(
            period_start=start_date,
            period_end=end_date,
            total_cost=Decimal(0)
        )
        
        for record in records:
            # Total cost
            summary.total_cost += record.cost
            
            # By project
            if record.project_id not in summary.by_project:
                summary.by_project[record.project_id] = Decimal(0)
            summary.by_project[record.project_id] += record.cost
            
            # By service
            if record.service not in summary.by_service:
                summary.by_service[record.service] = Decimal(0)
            summary.by_service[record.service] += record.cost
            
            # By region
            if record.region not in summary.by_region:
                summary.by_region[record.region] = Decimal(0)
            summary.by_region[record.region] += record.cost
        
        return summary
    
    def get_daily_costs(
        self,
        start_date: date,
        end_date: date,
        project_id: Optional[str] = None,
        service: Optional[str] = None
    ) -> Dict[date, Decimal]:
        """
        Get daily cost totals.
        
        Args:
            start_date: Start date
            end_date: End date
            project_id: Optional project filter
            service: Optional service filter
            
        Returns:
            Dictionary mapping dates to costs
        """
        query = f"""
        SELECT
            DATE(usage_start_time) as date,
            SUM(cost) as daily_cost
        FROM
            `{self.table_id}`
        WHERE
            DATE(usage_start_time) BETWEEN @start_date AND @end_date
            AND cost > 0
        """
        
        params = [
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
        
        if project_id:
            query += " AND project.id = @project_id"
            params.append(bigquery.ScalarQueryParameter("project_id", "STRING", project_id))
        
        if service:
            query += " AND service.description = @service"
            params.append(bigquery.ScalarQueryParameter("service", "STRING", service))
        
        query += " GROUP BY date ORDER BY date"
        
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()
        
        daily_costs = {}
        for row in results:
            daily_costs[row.date] = Decimal(str(row.daily_cost))
        
        return daily_costs
```

### Milestone 2: Cost Analysis & Anomaly Detection (Week 2)
**Deliverables:**
- Trend analysis
- Week-over-week/month-over-month comparison
- Anomaly detection algorithms
- Budget tracking

**Key Code Example:**
```python
from typing import Dict, List, Optional
from datetime import date, timedelta
from decimal import Decimal
import numpy as np
from scipy import stats
import uuid

class CostAnalyzer:
    """Analyze cost data and trends."""
    
    def __init__(self, collector: GCPBillingCollector):
        self.collector = collector
    
    def analyze_trends(
        self,
        start_date: date,
        end_date: date,
        granularity: CostGranularity = CostGranularity.DAILY
    ) -> Dict[str, Any]:
        """
        Analyze cost trends over time.
        
        Args:
            start_date: Start date
            end_date: End date
            granularity: Data granularity
            
        Returns:
            Trend analysis results
        """
        daily_costs = self.collector.get_daily_costs(start_date, end_date)
        
        # Convert to sorted arrays
        dates = sorted(daily_costs.keys())
        costs = [float(daily_costs[d]) for d in dates]
        
        if len(costs) < 2:
            return {"error": "Insufficient data for trend analysis"}
        
        # Calculate statistics
        mean_cost = np.mean(costs)
        std_cost = np.std(costs)
        
        # Linear regression for trend
        x = np.arange(len(costs))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, costs)
        
        # Determine trend direction
        if slope > mean_cost * 0.05:  # >5% increase
            trend = "increasing"
        elif slope < -mean_cost * 0.05:  # >5% decrease
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            'mean_daily_cost': mean_cost,
            'std_daily_cost': std_cost,
            'trend': trend,
            'trend_slope': slope,
            'r_squared': r_value ** 2,
            'total_cost': sum(costs),
            'min_cost': min(costs),
            'max_cost': max(costs),
            'days_analyzed': len(costs)
        }
    
    def compare_periods(
        self,
        current_start: date,
        current_end: date,
        comparison_start: date,
        comparison_end: date
    ) -> Dict[str, Any]:
        """
        Compare costs between two periods.
        
        Args:
            current_start: Current period start
            current_end: Current period end
            comparison_start: Comparison period start
            comparison_end: Comparison period end
            
        Returns:
            Period comparison results
        """
        current_summary = self.collector.get_cost_summary(current_start, current_end)
        comparison_summary = self.collector.get_cost_summary(comparison_start, comparison_end)
        
        # Calculate differences
        cost_diff = current_summary.total_cost - comparison_summary.total_cost
        percent_change = (
            float(cost_diff / comparison_summary.total_cost * 100)
            if comparison_summary.total_cost > 0 else 0
        )
        
        # Project-level changes
        project_changes = {}
        all_projects = set(current_summary.by_project.keys()) | set(comparison_summary.by_project.keys())
        
        for project in all_projects:
            current_cost = current_summary.by_project.get(project, Decimal(0))
            comparison_cost = comparison_summary.by_project.get(project, Decimal(0))
            
            if comparison_cost > 0:
                change_pct = float((current_cost - comparison_cost) / comparison_cost * 100)
            else:
                change_pct = 100.0 if current_cost > 0 else 0.0
            
            project_changes[project] = {
                'current': float(current_cost),
                'comparison': float(comparison_cost),
                'change': float(current_cost - comparison_cost),
                'change_percent': change_pct
            }
        
        return {
            'current_total': float(current_summary.total_cost),
            'comparison_total': float(comparison_summary.total_cost),
            'difference': float(cost_diff),
            'percent_change': percent_change,
            'project_changes': project_changes
        }


class AnomalyDetector:
    """Detect cost anomalies."""
    
    def __init__(
        self,
        collector: GCPBillingCollector,
        spike_threshold: float = 2.0,  # Standard deviations
        drop_threshold: float = -1.5
    ):
        """
        Initialize anomaly detector.
        
        Args:
            collector: Billing data collector
            spike_threshold: Threshold for spike detection (std devs)
            drop_threshold: Threshold for drop detection (std devs)
        """
        self.collector = collector
        self.spike_threshold = spike_threshold
        self.drop_threshold = drop_threshold
    
    def detect_anomalies(
        self,
        analysis_date: date,
        lookback_days: int = 30
    ) -> List[CostAnomaly]:
        """
        Detect cost anomalies on a specific date.
        
        Args:
            analysis_date: Date to analyze
            lookback_days: Days of historical data to use
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        # Get historical costs
        start_date = analysis_date - timedelta(days=lookback_days)
        end_date = analysis_date
        
        daily_costs = self.collector.get_daily_costs(start_date, end_date)
        
        if len(daily_costs) < 7:  # Need at least a week of data
            logger.warning("Insufficient data for anomaly detection")
            return anomalies
        
        # Get costs by project for the analysis date
        records = self.collector.get_cost_records(analysis_date, analysis_date)
        
        # Group by project and service
        project_service_costs = {}
        for record in records:
            key = (record.project_id, record.service)
            if key not in project_service_costs:
                project_service_costs[key] = Decimal(0)
            project_service_costs[key] += record.cost
        
        # Analyze each project-service combination
        for (project_id, service), actual_cost in project_service_costs.items():
            # Get historical costs for this project-service
            historical = self._get_historical_costs(
                project_id, service, start_date, analysis_date - timedelta(days=1)
            )
            
            if len(historical) < 3:  # Need minimum history
                continue
            
            # Calculate baseline (mean and std)
            costs_array = np.array([float(c) for c in historical])
            mean_cost = np.mean(costs_array)
            std_cost = np.std(costs_array)
            
            if std_cost == 0:  # Constant cost
                std_cost = mean_cost * 0.1  # Use 10% as std
            
            # Calculate z-score
            z_score = (float(actual_cost) - mean_cost) / std_cost
            
            # Detect anomalies
            if z_score > self.spike_threshold:
                anomaly_type = AnomalyType.SPIKE
                severity = self._get_severity(z_score)
                
                anomaly = CostAnomaly(
                    anomaly_id=str(uuid.uuid4()),
                    anomaly_type=anomaly_type,
                    date=analysis_date,
                    project_id=project_id,
                    service=service,
                    expected_cost=Decimal(str(mean_cost)),
                    actual_cost=actual_cost,
                    deviation_percent=(float(actual_cost) / mean_cost - 1) * 100,
                    severity=severity,
                    description=f"Unusual cost spike detected in {service}"
                )
                
                anomalies.append(anomaly)
            
            elif z_score < self.drop_threshold:
                anomaly_type = AnomalyType.DROP
                severity = "low"  # Drops are usually good
                
                anomaly = CostAnomaly(
                    anomaly_id=str(uuid.uuid4()),
                    anomaly_type=anomaly_type,
                    date=analysis_date,
                    project_id=project_id,
                    service=service,
                    expected_cost=Decimal(str(mean_cost)),
                    actual_cost=actual_cost,
                    deviation_percent=(float(actual_cost) / mean_cost - 1) * 100,
                    severity=severity,
                    description=f"Unusual cost drop detected in {service}"
                )
                
                anomalies.append(anomaly)
        
        logger.info(f"Detected {len(anomalies)} anomalies on {analysis_date}")
        
        return anomalies
    
    def _get_historical_costs(
        self,
        project_id: str,
        service: str,
        start_date: date,
        end_date: date
    ) -> List[Decimal]:
        """Get historical costs for a project-service combination."""
        daily_costs = self.collector.get_daily_costs(
            start_date, end_date, project_id=project_id, service=service
        )
        
        return list(daily_costs.values())
    
    def _get_severity(self, z_score: float) -> str:
        """Determine anomaly severity from z-score."""
        abs_z = abs(z_score)
        
        if abs_z >= 4:
            return "critical"
        elif abs_z >= 3:
            return "high"
        elif abs_z >= 2.5:
            return "medium"
        else:
            return "low"
```

### Milestone 3: Optimization Recommendations (Week 3)
**Deliverables:**
- Idle resource detection
- Right-sizing recommendations
- Reserved instance analysis
- Storage optimization

**Key Code Example:**
```python
from google.cloud import compute_v1, monitoring_v3
from typing import List

class ComputeOptimizer:
    """Generate compute optimization recommendations."""
    
    def __init__(self, credentials_path: str):
        from google.oauth2 import service_account
        
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        
        self.compute_client = compute_v1.InstancesClient(credentials=credentials)
        self.monitoring_client = monitoring_v3.MetricServiceClient(credentials=credentials)
    
    def find_idle_instances(
        self,
        project_id: str,
        cpu_threshold: float = 5.0,  # % CPU
        lookback_days: int = 7
    ) -> List[CostOptimization]:
        """
        Find idle compute instances.
        
        Args:
            project_id: GCP project ID
            cpu_threshold: CPU usage threshold (%)
            lookback_days: Days to analyze
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        # Get all instances
        instances = self._list_all_instances(project_id)
        
        for instance in instances:
            # Get CPU utilization
            avg_cpu = self._get_avg_cpu_utilization(
                project_id, instance['name'], instance['zone'], lookback_days
            )
            
            if avg_cpu < cpu_threshold:
                # Estimate cost (simplified)
                machine_type = instance['machineType'].split('/')[-1]
                monthly_cost = self._estimate_instance_cost(machine_type)
                
                recommendation = CostOptimization(
                    recommendation_id=str(uuid.uuid4()),
                    recommendation_type=RecommendationType.IDLE_RESOURCE,
                    resource_id=instance['name'],
                    resource_type="compute.instance",
                    project_id=project_id,
                    current_cost_monthly=monthly_cost,
                    potential_savings_monthly=monthly_cost,  # Full cost if deleted
                    confidence=0.9 if avg_cpu < 2.0 else 0.7,
                    description=f"Instance '{instance['name']}' is idle (avg CPU: {avg_cpu:.1f}%)",
                    action_items=[
                        "Consider deleting this instance",
                        "Or downgrade to a smaller machine type",
                        "Or use auto-scaling"
                    ]
                )
                
                recommendations.append(recommendation)
        
        return recommendations
    
    def find_rightsizing_opportunities(
        self,
        project_id: str
    ) -> List[CostOptimization]:
        """
        Find instances that can be downsized.
        
        Args:
            project_id: GCP project ID
            
        Returns:
            List of right-sizing recommendations
        """
        recommendations = []
        
        instances = self._list_all_instances(project_id)
        
        for instance in instances:
            avg_cpu = self._get_avg_cpu_utilization(project_id, instance['name'], instance['zone'], 30)
            avg_memory = self._get_avg_memory_utilization(project_id, instance['name'], 30)
            
            machine_type = instance['machineType'].split('/')[-1]
            current_cost = self._estimate_instance_cost(machine_type)
            
            # Simple right-sizing logic
            if avg_cpu < 20 and avg_memory < 40:
                # Suggest smaller instance
                suggested_type = self._suggest_smaller_instance(machine_type)
                new_cost = self._estimate_instance_cost(suggested_type)
                savings = current_cost - new_cost
                
                if savings > Decimal("10"):  # Only if saves >$10/month
                    recommendation = CostOptimization(
                        recommendation_id=str(uuid.uuid4()),
                        recommendation_type=RecommendationType.RIGHT_SIZING,
                        resource_id=instance['name'],
                        resource_type="compute.instance",
                        project_id=project_id,
                        current_cost_monthly=current_cost,
                        potential_savings_monthly=savings,
                        confidence=0.8,
                        description=(
                            f"Instance '{instance['name']}' is underutilized "
                            f"(CPU: {avg_cpu:.1f}%, Memory: {avg_memory:.1f}%)"
                        ),
                        action_items=[
                            f"Downsize from {machine_type} to {suggested_type}",
                            "Test application performance after change",
                            "Monitor metrics for a week"
                        ]
                    )
                    
                    recommendations.append(recommendation)
        
        return recommendations
    
    def _list_all_instances(self, project_id: str) -> List[Dict]:
        """List all compute instances in a project."""
        instances = []
        
        # This is simplified - in reality, need to iterate through all zones
        zones = ['us-central1-a', 'us-east1-b', 'europe-west1-b']  # Example
        
        for zone in zones:
            try:
                request = compute_v1.ListInstancesRequest(
                    project=project_id,
                    zone=zone
                )
                
                for instance in self.compute_client.list(request=request):
                    instances.append({
                        'name': instance.name,
                        'zone': zone,
                        'machineType': instance.machine_type,
                        'status': instance.status
                    })
            except Exception as e:
                logger.debug(f"No instances in {zone}: {e}")
                continue
        
        return instances
    
    def _get_avg_cpu_utilization(
        self,
        project_id: str,
        instance_name: str,
        zone: str,
        days: int
    ) -> float:
        """Get average CPU utilization (simplified)."""
        # This is a placeholder - actual implementation would use Cloud Monitoring API
        import random
        return random.uniform(0, 100)
    
    def _get_avg_memory_utilization(
        self,
        project_id: str,
        instance_name: str,
        days: int
    ) -> float:
        """Get average memory utilization (simplified)."""
        import random
        return random.uniform(0, 100)
    
    def _estimate_instance_cost(self, machine_type: str) -> Decimal:
        """Estimate monthly cost (simplified pricing)."""
        # Simplified cost estimation
        pricing = {
            'n1-standard-1': Decimal("24.27"),
            'n1-standard-2': Decimal("48.54"),
            'n1-standard-4': Decimal("97.09"),
            'e2-micro': Decimal("6.11"),
            'e2-small': Decimal("12.22"),
            'e2-medium': Decimal("24.45"),
        }
        
        return pricing.get(machine_type, Decimal("50.00"))
    
    def _suggest_smaller_instance(self, current_type: str) -> str:
        """Suggest a smaller instance type."""
        downsizing_map = {
            'n1-standard-4': 'n1-standard-2',
            'n1-standard-2': 'n1-standard-1',
            'n1-standard-1': 'e2-medium',
            'e2-medium': 'e2-small',
        }
        
        return downsizing_map.get(current_type, current_type)
```

### Milestone 4: Reporting & Visualization (Week 4)
**Deliverables:**
- Report generator
- Charts and visualizations
- PDF export
- Email delivery
- Automated scheduling

**Key Code Example:**
```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import io
from typing import List
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class CostVisualizer:
    """Generate cost visualizations."""
    
    @staticmethod
    def create_cost_trend_chart(
        daily_costs: Dict[date, Decimal],
        title: str = "Cost Trend"
    ) -> Figure:
        """Create cost trend line chart."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        dates = sorted(daily_costs.keys())
        costs = [float(daily_costs[d]) for d in dates]
        
        ax.plot(dates, costs, marker='o', linewidth=2, markersize=4)
        ax.set_xlabel('Date')
        ax.set_ylabel('Cost (USD)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def create_service_breakdown_chart(
        by_service: Dict[str, Decimal],
        top_n: int = 10
    ) -> Figure:
        """Create service cost breakdown pie chart."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get top N services
        sorted_services = sorted(
            by_service.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        services = [s[0] for s in sorted_services]
        costs = [float(s[1]) for s in sorted_services]
        
        # Create pie chart
        ax.pie(costs, labels=services, autopct='%1.1f%%', startangle=90)
        ax.set_title(f'Top {top_n} Services by Cost')
        
        return fig
    
    @staticmethod
    def create_project_comparison_chart(
        by_project: Dict[str, Decimal]
    ) -> Figure:
        """Create project cost comparison bar chart."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        projects = list(by_project.keys())
        costs = [float(by_project[p]) for p in projects]
        
        ax.barh(projects, costs)
        ax.set_xlabel('Cost (USD)')
        ax.set_ylabel('Project')
        ax.set_title('Cost by Project')
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        return fig


class ReportGenerator:
    """Generate cost reports."""
    
    def __init__(self, template_dir: str):
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        self.visualizer = CostVisualizer()
    
    def generate_weekly_report(
        self,
        report: CostReport,
        output_format: str = "html"
    ) -> str:
        """
        Generate weekly cost report.
        
        Args:
            report: Cost report data
            output_format: "html" or "pdf"
            
        Returns:
            Path to generated report file
        """
        # Generate charts
        charts = self._generate_charts(report)
        
        # Render HTML
        template = self.jinja_env.get_template('weekly_report.html')
        
        html_content = template.render(
            report=report,
            charts=charts,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        if output_format == "html":
            output_path = f"reports/weekly_report_{report.report_id}.html"
            with open(output_path, 'w') as f:
                f.write(html_content)
            return output_path
        
        elif output_format == "pdf":
            output_path = f"reports/weekly_report_{report.report_id}.pdf"
            HTML(string=html_content).write_pdf(output_path)
            return output_path
    
    def _generate_charts(self, report: CostReport) -> Dict[str, str]:
        """Generate charts and return as base64 encoded images."""
        charts = {}
        
        # Cost trend chart
        # (In reality, would get daily costs from collector)
        # charts['trend'] = self._fig_to_base64(trend_fig)
        
        # Service breakdown
        service_fig = self.visualizer.create_service_breakdown_chart(
            report.summary.by_service
        )
        charts['service_breakdown'] = self._fig_to_base64(service_fig)
        
        # Project comparison
        project_fig = self.visualizer.create_project_comparison_chart(
            report.summary.by_project
        )
        charts['project_comparison'] = self._fig_to_base64(project_fig)
        
        return charts
    
    def _fig_to_base64(self, fig: Figure) -> str:
        """Convert matplotlib figure to base64 string."""
        import base64
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        
        img_str = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{img_str}"


class EmailReportSender:
    """Send reports via email."""
    
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        from_addr: str
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_addr = from_addr
    
    def send_report(
        self,
        to_addrs: List[str],
        subject: str,
        html_body: str,
        attachments: Optional[List[str]] = None
    ) -> None:
        """
        Send cost report via email.
        
        Args:
            to_addrs: List of recipient email addresses
            subject: Email subject
            html_body: HTML email body
            attachments: List of file paths to attach
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = ', '.join(to_addrs)
        
        # Add HTML body
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Add attachments
        if attachments:
            for filepath in attachments:
                with open(filepath, 'rb') as f:
                    attachment = MIMEApplication(f.read(), _subtype="pdf")
                    attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=filepath.split('/')[-1]
                    )
                    msg.attach(attachment)
        
        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.from_addr, to_addrs, msg.as_string())
        
        logger.info(f"Report sent to {', '.join(to_addrs)}")
```

**CLI Entry Point:**
```python
import click
from datetime import date, timedelta

@click.group()
def cli():
    """Cloud Cost Analyzer - GCP cost analysis and optimization"""
    pass

@cli.command()
@click.option('--days', '-d', default=7, help='Days to analyze')
@click.option('--output', '-o', type=click.Choice(['html', 'pdf']), default='html')
def report(days, output):
    """Generate cost report"""
    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=days)
    
    # Initialize components
    collector = GCPBillingCollector(
        credentials_path='credentials.json',
        billing_project_id='my-project',
        billing_dataset='billing_export',
        billing_table='gcp_billing_export'
    )
    
    analyzer = CostAnalyzer(collector)
    anomaly_detector = AnomalyDetector(collector)
    optimizer = ComputeOptimizer('credentials.json')
    
    # Generate report
    console.print(f"[bold]Generating cost report for {start_date} to {end_date}[/bold]")
    
    summary = collector.get_cost_summary(start_date, end_date)
    anomalies = anomaly_detector.detect_anomalies(end_date)
    recommendations = optimizer.find_idle_instances('my-project')
    
    report = CostReport(
        report_id=str(uuid.uuid4()),
        generated_at=datetime.now(),
        period_start=start_date,
        period_end=end_date,
        summary=summary,
        anomalies=anomalies,
        recommendations=recommendations
    )
    
    generator = ReportGenerator('templates')
    report_path = generator.generate_weekly_report(report, output_format=output)
    
    console.print(f"[green]✓[/green] Report generated: {report_path}")

if __name__ == '__main__':
    cli()
```

## Project-Specific Requirements

### requirements.txt
```
# GCP
google-cloud-bigquery==3.14.0
google-cloud-compute==1.14.1
google-cloud-monitoring==2.18.0

# Data Analysis
numpy==1.26.2
scipy==1.11.4
pandas==2.1.4

# Visualization
matplotlib==3.8.2
seaborn==0.13.0

# Reporting
jinja2==3.1.2
weasyprint==60.2

# CLI
click==8.1.7
rich==13.7.0

# Utilities
pyyaml==6.0.1
python-dotenv==1.0.0
```

### requirements-dev.txt
```
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
black==23.12.1
flake8==6.1.0
mypy==1.7.1
```

## Evaluation Criteria

### Must Have
- [ ] Pulls billing data from BigQuery
- [ ] Generates cost summaries by project/service
- [ ] Detects cost anomalies
- [ ] Produces cost visualizations
- [ ] Generates HTML/PDF reports
- [ ] Type hints and PEP 8
- [ ] >70% test coverage

### Should Have
- [ ] Week-over-week comparison
- [ ] Budget tracking
- [ ] Idle resource detection
- [ ] Email report delivery
- [ ] Automated scheduling
- [ ] Cost forecasting

### Nice to Have
- [ ] Web dashboard
- [ ] Machine learning anomaly detection
- [ ] Multi-cloud support (AWS, Azure)
- [ ] Reserved instance recommendations
- [ ] Real-time cost alerts

## Bonus Features

1. **Predictive Analytics**
   - Forecast future costs
   - Budget burn-rate prediction
   - Seasonal trend analysis

2. **Advanced Optimization**
   - Commitment discount modeling
   - Multi-year cost projections
   - TCO analysis

3. **Integration**
   - Jira ticket creation for recommendations
   - ServiceNow integration
   - Terraform cost estimation

4. **FinOps Dashboard**
   - Real-time cost tracking
   - Team cost allocation
   - Chargeback reports

## Deliverables

1. Source code with modular design
2. Documentation
3. Example reports (HTML/PDF)
4. Automated report scheduling
5. Demo showing:
   - Cost data collection
   - Anomaly detection
   - Report generation
   - Optimization recommendations

## Success Metrics
- Accurately pulls and analyzes billing data
- Detects anomalies with <10% false positive rate
- Generates professional reports
- Recommendations lead to >10% cost savings
- All tests pass

## Learning Outcomes
- BigQuery and GCP APIs
- Data analysis with NumPy/Pandas
- Anomaly detection techniques
- Data visualization
- FinOps best practices
- Building cost optimization tools
- Production data pipelines
