# LAB 08: Google Cloud Platform Automation

## Learning Objectives
By the end of this lab, you will be able to:
- Set up and authenticate with Google Cloud Python SDK
- Automate Google Compute Engine (GCE) operations
- Manage Google Cloud Storage buckets and objects
- Automate Google Kubernetes Engine (GKE) cluster operations
- Implement infrastructure provisioning scripts
- Handle cloud resource lifecycle management
- Apply best practices for cloud automation

## Prerequisites
- Python 3.8+ installed
- Google Cloud account (free tier available)
- Basic understanding of cloud computing concepts
- Familiarity with GCP services

## Setup

### Install Google Cloud SDK

```bash
# Install the Google Cloud client libraries
pip install google-cloud-compute google-cloud-storage google-cloud-container
pip install google-auth google-auth-oauthlib google-auth-httplib2
```

### Authentication Setup

1. **Install gcloud CLI** (if not already installed):
```bash
# Follow instructions at: https://cloud.google.com/sdk/docs/install
```

2. **Authenticate with GCP**:
```bash
# Login to your Google Cloud account
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Create application default credentials
gcloud auth application-default login
```

3. **Service Account Method** (recommended for automation):
```bash
# Create a service account
gcloud iam service-accounts create devops-automation \
    --display-name "DevOps Automation"

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:devops-automation@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/compute.admin"

# Create and download key
gcloud iam service-accounts keys create ~/gcp-key.json \
    --iam-account devops-automation@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/gcp-key.json"
```

---

## Part 1: Google Compute Engine Automation

### Exercise 1.1: List and Manage VM Instances

Create `gce_manager.py`:

```python
from google.cloud import compute_v1
from typing import List, Dict
import time


class GCEManager:
    """Manage Google Compute Engine instances."""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.instances_client = compute_v1.InstancesClient()
        self.zones_client = compute_v1.ZonesClient()
    
    def list_instances(self, zone: str = None) -> List[Dict]:
        """List all instances in project or specific zone."""
        instances = []
        
        if zone:
            zones = [zone]
        else:
            # List all zones in project
            zones = self._get_all_zones()
        
        for zone_name in zones:
            request = compute_v1.ListInstancesRequest(
                project=self.project_id,
                zone=zone_name
            )
            
            try:
                page_result = self.instances_client.list(request=request)
                
                for instance in page_result:
                    instance_info = {
                        'name': instance.name,
                        'zone': zone_name,
                        'machine_type': instance.machine_type.split('/')[-1],
                        'status': instance.status,
                        'internal_ip': self._get_internal_ip(instance),
                        'external_ip': self._get_external_ip(instance)
                    }
                    instances.append(instance_info)
                    
            except Exception as e:
                print(f"Error listing instances in {zone_name}: {e}")
        
        return instances
    
    def _get_all_zones(self) -> List[str]:
        """Get all available zones in the project."""
        request = compute_v1.ListZonesRequest(project=self.project_id)
        zones = self.zones_client.list(request=request)
        return [zone.name for zone in zones]
    
    def _get_internal_ip(self, instance) -> str:
        """Extract internal IP from instance."""
        if instance.network_interfaces:
            return instance.network_interfaces[0].network_i_p
        return "N/A"
    
    def _get_external_ip(self, instance) -> str:
        """Extract external IP from instance."""
        if instance.network_interfaces:
            access_configs = instance.network_interfaces[0].access_configs
            if access_configs:
                return access_configs[0].nat_i_p
        return "N/A"
    
    def print_instances(self, zone: str = None):
        """Print formatted list of instances."""
        instances = self.list_instances(zone)
        
        if not instances:
            print("No instances found.")
            return
        
        print(f"\n{'='*80}")
        print(f"Google Compute Engine Instances (Project: {self.project_id})")
        print(f"{'='*80}\n")
        
        for instance in instances:
            status_symbol = '✓' if instance['status'] == 'RUNNING' else '○'
            
            print(f"{status_symbol} {instance['name']}")
            print(f"   Zone: {instance['zone']}")
            print(f"   Machine Type: {instance['machine_type']}")
            print(f"   Status: {instance['status']}")
            print(f"   Internal IP: {instance['internal_ip']}")
            print(f"   External IP: {instance['external_ip']}")
            print()
    
    def get_instance(self, instance_name: str, zone: str):
        """Get details of a specific instance."""
        request = compute_v1.GetInstanceRequest(
            project=self.project_id,
            zone=zone,
            instance=instance_name
        )
        
        try:
            instance = self.instances_client.get(request=request)
            
            print(f"\nInstance: {instance.name}")
            print(f"ID: {instance.id}")
            print(f"Status: {instance.status}")
            print(f"Machine Type: {instance.machine_type.split('/')[-1]}")
            print(f"Creation Time: {instance.creation_timestamp}")
            
            # Disks
            print(f"\nDisks:")
            for disk in instance.disks:
                print(f"  - {disk.device_name} ({disk.disk_size_gb}GB)")
            
            # Network
            print(f"\nNetwork Interfaces:")
            for interface in instance.network_interfaces:
                print(f"  - Network: {interface.network.split('/')[-1]}")
                print(f"    Internal IP: {interface.network_i_p}")
                if interface.access_configs:
                    print(f"    External IP: {interface.access_configs[0].nat_i_p}")
            
            # Metadata
            if instance.metadata and instance.metadata.items:
                print(f"\nMetadata:")
                for item in instance.metadata.items:
                    print(f"  {item.key}: {item.value[:50]}...")
            
            return instance
            
        except Exception as e:
            print(f"Error getting instance: {e}")
            return None


if __name__ == "__main__":
    import os
    
    project_id = os.getenv('GCP_PROJECT_ID', 'your-project-id')
    
    if project_id == 'your-project-id':
        print("Please set GCP_PROJECT_ID environment variable")
        print("export GCP_PROJECT_ID='your-gcp-project-id'")
    else:
        manager = GCEManager(project_id)
        manager.print_instances()
        
        # Get specific instance
        # manager.get_instance('my-instance', 'us-central1-a')
```

### Exercise 1.2: Create and Manage VM Instances

Create `create_vm.py`:

```python
from google.cloud import compute_v1
import time


def create_instance(
    project_id: str,
    zone: str,
    instance_name: str,
    machine_type: str = "e2-micro",
    disk_size_gb: int = 10,
    startup_script: str = None
) -> compute_v1.Instance:
    """
    Create a new Google Compute Engine instance.
    
    Args:
        project_id: GCP project ID
        zone: Zone to create instance in (e.g., 'us-central1-a')
        instance_name: Name for the new instance
        machine_type: Machine type (default: e2-micro for free tier)
        disk_size_gb: Boot disk size in GB
        startup_script: Optional startup script to run on boot
    """
    instances_client = compute_v1.InstancesClient()
    
    # Configure the machine type
    machine_type_path = f"zones/{zone}/machineTypes/{machine_type}"
    
    # Configure the boot disk
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-11"
    )
    initialize_params.disk_size_gb = disk_size_gb
    initialize_params.disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True
    
    # Configure network interface
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "global/networks/default"
    
    # Add external IP
    access_config = compute_v1.AccessConfig()
    access_config.name = "External NAT"
    access_config.type_ = "ONE_TO_ONE_NAT"
    network_interface.access_configs = [access_config]
    
    # Create instance configuration
    instance = compute_v1.Instance()
    instance.name = instance_name
    instance.machine_type = machine_type_path
    instance.disks = [disk]
    instance.network_interfaces = [network_interface]
    
    # Add startup script if provided
    if startup_script:
        metadata = compute_v1.Metadata()
        metadata.items = [
            compute_v1.Items(key="startup-script", value=startup_script)
        ]
        instance.metadata = metadata
    
    # Add labels
    instance.labels = {
        "environment": "dev",
        "managed-by": "python-automation"
    }
    
    # Create the instance
    print(f"\n🚀 Creating instance '{instance_name}' in {zone}...")
    
    request = compute_v1.InsertInstanceRequest()
    request.project = project_id
    request.zone = zone
    request.instance_resource = instance
    
    operation = instances_client.insert(request=request)
    
    # Wait for operation to complete
    print("⏳ Waiting for instance creation to complete...")
    wait_for_operation(project_id, zone, operation.name)
    
    print(f"✅ Instance '{instance_name}' created successfully!")
    
    # Get the created instance
    get_request = compute_v1.GetInstanceRequest(
        project=project_id,
        zone=zone,
        instance=instance_name
    )
    
    created_instance = instances_client.get(request=get_request)
    
    # Print instance details
    external_ip = created_instance.network_interfaces[0].access_configs[0].nat_i_p
    internal_ip = created_instance.network_interfaces[0].network_i_p
    
    print(f"\n📋 Instance Details:")
    print(f"   Name: {created_instance.name}")
    print(f"   Machine Type: {machine_type}")
    print(f"   Internal IP: {internal_ip}")
    print(f"   External IP: {external_ip}")
    print(f"   Status: {created_instance.status}")
    
    return created_instance


def wait_for_operation(project_id: str, zone: str, operation_name: str):
    """Wait for a zone operation to complete."""
    operations_client = compute_v1.ZoneOperationsClient()
    
    while True:
        request = compute_v1.GetZoneOperationRequest(
            project=project_id,
            zone=zone,
            operation=operation_name
        )
        
        operation = operations_client.get(request=request)
        
        if operation.status == compute_v1.Operation.Status.DONE:
            if operation.error:
                print(f"❌ Error: {operation.error}")
                raise Exception(operation.error)
            return operation
        
        time.sleep(2)


def stop_instance(project_id: str, zone: str, instance_name: str):
    """Stop a running instance."""
    instances_client = compute_v1.InstancesClient()
    
    print(f"⏸️  Stopping instance '{instance_name}'...")
    
    request = compute_v1.StopInstanceRequest(
        project=project_id,
        zone=zone,
        instance=instance_name
    )
    
    operation = instances_client.stop(request=request)
    wait_for_operation(project_id, zone, operation.name)
    
    print(f"✅ Instance '{instance_name}' stopped successfully!")


def start_instance(project_id: str, zone: str, instance_name: str):
    """Start a stopped instance."""
    instances_client = compute_v1.InstancesClient()
    
    print(f"▶️  Starting instance '{instance_name}'...")
    
    request = compute_v1.StartInstanceRequest(
        project=project_id,
        zone=zone,
        instance=instance_name
    )
    
    operation = instances_client.start(request=request)
    wait_for_operation(project_id, zone, operation.name)
    
    print(f"✅ Instance '{instance_name}' started successfully!")


def delete_instance(project_id: str, zone: str, instance_name: str):
    """Delete an instance."""
    instances_client = compute_v1.InstancesClient()
    
    print(f"🗑️  Deleting instance '{instance_name}'...")
    
    request = compute_v1.DeleteInstanceRequest(
        project=project_id,
        zone=zone,
        instance=instance_name
    )
    
    operation = instances_client.delete(request=request)
    wait_for_operation(project_id, zone, operation.name)
    
    print(f"✅ Instance '{instance_name}' deleted successfully!")


if __name__ == "__main__":
    import os
    
    project_id = os.getenv('GCP_PROJECT_ID', 'your-project-id')
    zone = "us-central1-a"
    instance_name = "test-vm-python"
    
    # Startup script to install nginx
    startup_script = """#!/bin/bash
    apt-get update
    apt-get install -y nginx
    systemctl start nginx
    echo "<h1>Hello from Python-created VM!</h1>" > /var/www/html/index.html
    """
    
    if project_id != 'your-project-id':
        # Create instance
        create_instance(
            project_id,
            zone,
            instance_name,
            machine_type="e2-micro",
            startup_script=startup_script
        )
        
        # Uncomment to test stop/start/delete
        # time.sleep(10)
        # stop_instance(project_id, zone, instance_name)
        # time.sleep(5)
        # start_instance(project_id, zone, instance_name)
        # time.sleep(5)
        # delete_instance(project_id, zone, instance_name)
    else:
        print("Please set GCP_PROJECT_ID environment variable")
```

---

## Part 2: Google Cloud Storage Automation

### Exercise 2.1: Manage Storage Buckets and Objects

Create `gcs_manager.py`:

```python
from google.cloud import storage
from typing import List
import os


class GCSManager:
    """Manage Google Cloud Storage buckets and objects."""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = storage.Client(project=project_id)
    
    def create_bucket(self, bucket_name: str, location: str = "US") -> storage.Bucket:
        """Create a new storage bucket."""
        try:
            bucket = self.client.create_bucket(bucket_name, location=location)
            print(f"✅ Bucket '{bucket_name}' created in {location}")
            return bucket
        except Exception as e:
            print(f"❌ Error creating bucket: {e}")
            return None
    
    def list_buckets(self) -> List[storage.Bucket]:
        """List all buckets in the project."""
        buckets = list(self.client.list_buckets())
        
        print(f"\n{'='*60}")
        print(f"Storage Buckets (Project: {self.project_id})")
        print(f"{'='*60}\n")
        
        if not buckets:
            print("No buckets found.")
            return buckets
        
        for bucket in buckets:
            print(f"🪣 {bucket.name}")
            print(f"   Location: {bucket.location}")
            print(f"   Storage Class: {bucket.storage_class}")
            print(f"   Created: {bucket.time_created}")
            print()
        
        return buckets
    
    def upload_file(self, bucket_name: str, source_file: str, destination_blob: str):
        """Upload a file to a bucket."""
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(destination_blob)
            
            print(f"⬆️  Uploading {source_file} to gs://{bucket_name}/{destination_blob}...")
            blob.upload_from_filename(source_file)
            
            print(f"✅ File uploaded successfully!")
            print(f"   URL: {blob.public_url}")
            
            return blob
            
        except Exception as e:
            print(f"❌ Error uploading file: {e}")
            return None
    
    def download_file(self, bucket_name: str, source_blob: str, destination_file: str):
        """Download a file from a bucket."""
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(source_blob)
            
            print(f"⬇️  Downloading gs://{bucket_name}/{source_blob} to {destination_file}...")
            blob.download_to_filename(destination_file)
            
            print(f"✅ File downloaded successfully!")
            
        except Exception as e:
            print(f"❌ Error downloading file: {e}")
    
    def list_blobs(self, bucket_name: str, prefix: str = None):
        """List all blobs in a bucket."""
        try:
            bucket = self.client.bucket(bucket_name)
            blobs = list(bucket.list_blobs(prefix=prefix))
            
            print(f"\n📦 Contents of gs://{bucket_name}/{prefix or ''}")
            print(f"{'='*60}\n")
            
            if not blobs:
                print("No files found.")
                return blobs
            
            total_size = 0
            for blob in blobs:
                size_mb = blob.size / (1024 * 1024)
                total_size += blob.size
                
                print(f"📄 {blob.name}")
                print(f"   Size: {size_mb:.2f} MB")
                print(f"   Content Type: {blob.content_type}")
                print(f"   Updated: {blob.updated}")
                print()
            
            print(f"Total: {len(blobs)} files, {total_size / (1024 * 1024):.2f} MB")
            
            return blobs
            
        except Exception as e:
            print(f"❌ Error listing blobs: {e}")
            return []
    
    def delete_blob(self, bucket_name: str, blob_name: str):
        """Delete a blob from a bucket."""
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            blob.delete()
            print(f"✅ Deleted gs://{bucket_name}/{blob_name}")
            
        except Exception as e:
            print(f"❌ Error deleting blob: {e}")
    
    def delete_bucket(self, bucket_name: str, force: bool = False):
        """Delete a bucket."""
        try:
            bucket = self.client.bucket(bucket_name)
            
            if force:
                # Delete all blobs first
                blobs = list(bucket.list_blobs())
                for blob in blobs:
                    blob.delete()
                print(f"Deleted {len(blobs)} blobs")
            
            bucket.delete()
            print(f"✅ Bucket '{bucket_name}' deleted")
            
        except Exception as e:
            print(f"❌ Error deleting bucket: {e}")
    
    def make_blob_public(self, bucket_name: str, blob_name: str):
        """Make a blob publicly accessible."""
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            blob.make_public()
            
            print(f"✅ {blob_name} is now public")
            print(f"   URL: {blob.public_url}")
            
        except Exception as e:
            print(f"❌ Error making blob public: {e}")
    
    def sync_directory(self, bucket_name: str, local_dir: str, prefix: str = ""):
        """Sync a local directory to a bucket."""
        uploaded = 0
        
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_dir)
                blob_path = os.path.join(prefix, relative_path).replace('\\', '/')
                
                self.upload_file(bucket_name, local_path, blob_path)
                uploaded += 1
        
        print(f"\n✅ Synced {uploaded} files to gs://{bucket_name}/{prefix}")


if __name__ == "__main__":
    import os
    
    project_id = os.getenv('GCP_PROJECT_ID', 'your-project-id')
    
    if project_id != 'your-project-id':
        manager = GCSManager(project_id)
        
        # List buckets
        manager.list_buckets()
        
        # Example operations (uncomment to use)
        # bucket_name = "my-devops-bucket-" + project_id
        # manager.create_bucket(bucket_name)
        # manager.upload_file(bucket_name, "README.md", "docs/README.md")
        # manager.list_blobs(bucket_name)
        # manager.download_file(bucket_name, "docs/README.md", "downloaded_README.md")
    else:
        print("Please set GCP_PROJECT_ID environment variable")
```

---

## Part 3: Google Kubernetes Engine Automation

### Exercise 3.1: Manage GKE Clusters

Create `gke_manager.py`:

```python
from google.cloud import container_v1
from typing import List


class GKEManager:
    """Manage Google Kubernetes Engine clusters."""
    
    def __init__(self, project_id: str, location: str = "us-central1-a"):
        self.project_id = project_id
        self.location = location
        self.client = container_v1.ClusterManagerClient()
        self.parent = f"projects/{project_id}/locations/{location}"
    
    def list_clusters(self) -> List:
        """List all GKE clusters in the location."""
        try:
            request = container_v1.ListClustersRequest(parent=self.parent)
            response = self.client.list_clusters(request=request)
            
            clusters = response.clusters
            
            print(f"\n{'='*70}")
            print(f"GKE Clusters in {self.location}")
            print(f"{'='*70}\n")
            
            if not clusters:
                print("No clusters found.")
                return clusters
            
            for cluster in clusters:
                print(f"☸️  {cluster.name}")
                print(f"   Status: {cluster.status.name}")
                print(f"   Location: {cluster.location}")
                print(f"   Node Count: {cluster.current_node_count}")
                print(f"   K8s Version: {cluster.current_master_version}")
                print(f"   Endpoint: {cluster.endpoint}")
                print()
            
            return clusters
            
        except Exception as e:
            print(f"❌ Error listing clusters: {e}")
            return []
    
    def create_cluster(self, cluster_name: str, node_count: int = 3):
        """Create a new GKE cluster."""
        print(f"🚀 Creating GKE cluster '{cluster_name}'...")
        
        # Define node pool configuration
        node_config = container_v1.NodeConfig(
            machine_type="e2-medium",
            disk_size_gb=100,
            oauth_scopes=[
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/logging.write",
                "https://www.googleapis.com/auth/monitoring",
            ]
        )
        
        node_pool = container_v1.NodePool(
            name="default-pool",
            initial_node_count=node_count,
            config=node_config
        )
        
        # Define cluster configuration
        cluster = container_v1.Cluster(
            name=cluster_name,
            initial_node_count=node_count,
            node_pools=[node_pool],
            network="default",
            logging_service="logging.googleapis.com/kubernetes",
            monitoring_service="monitoring.googleapis.com/kubernetes"
        )
        
        request = container_v1.CreateClusterRequest(
            parent=self.parent,
            cluster=cluster
        )
        
        try:
            operation = self.client.create_cluster(request=request)
            print(f"⏳ Cluster creation started. Operation: {operation.name}")
            print(f"   This may take several minutes...")
            return operation
        except Exception as e:
            print(f"❌ Error creating cluster: {e}")
            return None
    
    def delete_cluster(self, cluster_name: str):
        """Delete a GKE cluster."""
        cluster_path = f"{self.parent}/clusters/{cluster_name}"
        
        print(f"🗑️  Deleting cluster '{cluster_name}'...")
        
        request = container_v1.DeleteClusterRequest(name=cluster_path)
        
        try:
            operation = self.client.delete_cluster(request=request)
            print(f"⏳ Cluster deletion started. Operation: {operation.name}")
            return operation
        except Exception as e:
            print(f"❌ Error deleting cluster: {e}")
            return None
    
    def get_cluster(self, cluster_name: str):
        """Get details of a specific cluster."""
        cluster_path = f"{self.parent}/clusters/{cluster_name}"
        
        request = container_v1.GetClusterRequest(name=cluster_path)
        
        try:
            cluster = self.client.get_cluster(request=request)
            
            print(f"\n☸️  Cluster: {cluster.name}")
            print(f"{'='*70}")
            print(f"Status: {cluster.status.name}")
            print(f"Location: {cluster.location}")
            print(f"Zone: {cluster.zone if cluster.zone else 'Regional'}")
            print(f"Endpoint: {cluster.endpoint}")
            print(f"K8s Version: {cluster.current_master_version}")
            print(f"Current Node Count: {cluster.current_node_count}")
            print(f"Created: {cluster.create_time}")
            
            print(f"\nNode Pools:")
            for pool in cluster.node_pools:
                print(f"  - {pool.name}")
                print(f"    Node Count: {pool.initial_node_count}")
                print(f"    Machine Type: {pool.config.machine_type}")
                print(f"    Disk Size: {pool.config.disk_size_gb}GB")
            
            return cluster
            
        except Exception as e:
            print(f"❌ Error getting cluster: {e}")
            return None


if __name__ == "__main__":
    import os
    
    project_id = os.getenv('GCP_PROJECT_ID', 'your-project-id')
    location = os.getenv('GCP_LOCATION', 'us-central1-a')
    
    if project_id != 'your-project-id':
        manager = GKEManager(project_id, location)
        
        # List clusters
        manager.list_clusters()
        
        # Example operations (uncomment to use)
        # manager.create_cluster("my-test-cluster", node_count=3)
        # manager.get_cluster("my-test-cluster")
        # manager.delete_cluster("my-test-cluster")
    else:
        print("Please set GCP_PROJECT_ID environment variable")
        print("export GCP_PROJECT_ID='your-gcp-project-id'")
```

---

## Part 4: Infrastructure Automation Script

### Exercise 4.1: Complete Infrastructure Provisioning

Create `provision_infrastructure.py`:

```python
"""
Complete infrastructure provisioning script.
Creates VMs, storage buckets, and sets up networking.
"""

from google.cloud import compute_v1, storage
import time
import os


class InfrastructureProvisioner:
    """Provision complete GCP infrastructure."""
    
    def __init__(self, project_id: str, environment: str = "dev"):
        self.project_id = project_id
        self.environment = environment
        self.compute_client = compute_v1.InstancesClient()
        self.storage_client = storage.Client(project=project_id)
    
    def provision_web_tier(self, zone: str = "us-central1-a"):
        """Provision web tier infrastructure."""
        print(f"\n{'='*70}")
        print(f"Provisioning {self.environment} Web Tier Infrastructure")
        print(f"{'='*70}\n")
        
        # 1. Create storage bucket for static assets
        bucket_name = f"{self.project_id}-{self.environment}-web-assets"
        print(f"1️⃣  Creating storage bucket: {bucket_name}")
        
        try:
            bucket = self.storage_client.create_bucket(bucket_name)
            print(f"✅ Bucket created: gs://{bucket_name}")
        except Exception as e:
            print(f"⚠️  Bucket may already exist: {e}")
        
        # 2. Create web servers
        web_servers = []
        for i in range(1, 3):
            instance_name = f"{self.environment}-web-{i:02d}"
            print(f"\n2️⃣  Creating web server: {instance_name}")
            
            startup_script = f"""#!/bin/bash
            apt-get update
            apt-get install -y nginx
            
            cat > /var/www/html/index.html << EOF
            <html>
            <head><title>{self.environment.upper()} Web {i}</title></head>
            <body>
                <h1>{self.environment.upper()} Web Server {i}</h1>
                <p>Environment: {self.environment}</p>
                <p>Hostname: $(hostname)</p>
            </body>
            </html>
            EOF
            
            systemctl start nginx
            systemctl enable nginx
            """
            
            try:
                instance = self._create_instance(
                    instance_name,
                    zone,
                    "e2-micro",
                    startup_script
                )
                web_servers.append(instance)
                print(f"✅ Web server created: {instance_name}")
            except Exception as e:
                print(f"❌ Error creating web server: {e}")
        
        print(f"\n{'='*70}")
        print(f"✅ Web Tier Provisioning Complete!")
        print(f"{'='*70}")
        
        return {
            'bucket': bucket_name,
            'web_servers': web_servers
        }
    
    def provision_app_tier(self, zone: str = "us-central1-a"):
        """Provision application tier infrastructure."""
        print(f"\n{'='*70}")
        print(f"Provisioning {self.environment} Application Tier")
        print(f"{'='*70}\n")
        
        # Create application servers
        app_servers = []
        for i in range(1, 3):
            instance_name = f"{self.environment}-app-{i:02d}"
            print(f"Creating application server: {instance_name}")
            
            startup_script = """#!/bin/bash
            apt-get update
            apt-get install -y python3 python3-pip
            pip3 install flask gunicorn
            
            cat > /opt/app.py << 'EOF'
            from flask import Flask, jsonify
            import socket
            
            app = Flask(__name__)
            
            @app.route('/health')
            def health():
                return jsonify({'status': 'healthy', 'hostname': socket.gethostname()})
            
            @app.route('/')
            def home():
                return jsonify({'message': 'Application Server', 'hostname': socket.gethostname()})
            
            if __name__ == '__main__':
                app.run(host='0.0.0.0', port=8080)
            EOF
            
            # Run as systemd service
            cat > /etc/systemd/system/app.service << 'EOF'
            [Unit]
            Description=Flask Application
            After=network.target
            
            [Service]
            User=root
            WorkingDirectory=/opt
            ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8080 app:app
            Restart=always
            
            [Install]
            WantedBy=multi-user.target
            EOF
            
            systemctl daemon-reload
            systemctl start app
            systemctl enable app
            """
            
            try:
                instance = self._create_instance(
                    instance_name,
                    zone,
                    "e2-small",
                    startup_script
                )
                app_servers.append(instance)
                print(f"✅ App server created: {instance_name}")
            except Exception as e:
                print(f"❌ Error creating app server: {e}")
        
        return {'app_servers': app_servers}
    
    def _create_instance(self, name, zone, machine_type, startup_script):
        """Helper to create a compute instance."""
        machine_type_path = f"zones/{zone}/machineTypes/{machine_type}"
        
        # Boot disk
        disk = compute_v1.AttachedDisk()
        initialize_params = compute_v1.AttachedDiskInitializeParams()
        initialize_params.source_image = (
            "projects/debian-cloud/global/images/family/debian-11"
        )
        initialize_params.disk_size_gb = 10
        disk.initialize_params = initialize_params
        disk.auto_delete = True
        disk.boot = True
        
        # Network
        network_interface = compute_v1.NetworkInterface()
        network_interface.name = "global/networks/default"
        access_config = compute_v1.AccessConfig()
        access_config.name = "External NAT"
        access_config.type_ = "ONE_TO_ONE_NAT"
        network_interface.access_configs = [access_config]
        
        # Instance
        instance = compute_v1.Instance()
        instance.name = name
        instance.machine_type = machine_type_path
        instance.disks = [disk]
        instance.network_interfaces = [network_interface]
        
        # Metadata
        metadata = compute_v1.Metadata()
        metadata.items = [
            compute_v1.Items(key="startup-script", value=startup_script)
        ]
        instance.metadata = metadata
        
        # Labels
        instance.labels = {
            "environment": self.environment,
            "managed-by": "python-automation",
            "tier": name.split('-')[1]  # web or app
        }
        
        # Create
        request = compute_v1.InsertInstanceRequest()
        request.project = self.project_id
        request.zone = zone
        request.instance_resource = instance
        
        operation = self.compute_client.insert(request=request)
        self._wait_for_operation(self.project_id, zone, operation.name)
        
        return instance
    
    def _wait_for_operation(self, project_id, zone, operation_name):
        """Wait for operation to complete."""
        operations_client = compute_v1.ZoneOperationsClient()
        
        while True:
            request = compute_v1.GetZoneOperationRequest(
                project=project_id,
                zone=zone,
                operation=operation_name
            )
            
            operation = operations_client.get(request=request)
            
            if operation.status == compute_v1.Operation.Status.DONE:
                if operation.error:
                    raise Exception(operation.error)
                return operation
            
            time.sleep(2)
    
    def teardown_environment(self, zone: str = "us-central1-a"):
        """Teardown all resources for the environment."""
        print(f"\n{'='*70}")
        print(f"Tearing Down {self.environment} Environment")
        print(f"{'='*70}\n")
        
        # Delete instances
        instances_client = compute_v1.InstancesClient()
        request = compute_v1.ListInstancesRequest(
            project=self.project_id,
            zone=zone
        )
        
        instances = instances_client.list(request=request)
        
        for instance in instances:
            if instance.labels.get('environment') == self.environment:
                print(f"Deleting instance: {instance.name}")
                delete_request = compute_v1.DeleteInstanceRequest(
                    project=self.project_id,
                    zone=zone,
                    instance=instance.name
                )
                operation = instances_client.delete(request=delete_request)
                self._wait_for_operation(self.project_id, zone, operation.name)
                print(f"✅ Deleted: {instance.name}")
        
        # Delete buckets
        buckets = self.storage_client.list_buckets()
        for bucket in buckets:
            if self.environment in bucket.name:
                print(f"Deleting bucket: {bucket.name}")
                blobs = list(bucket.list_blobs())
                for blob in blobs:
                    blob.delete()
                bucket.delete()
                print(f"✅ Deleted: {bucket.name}")
        
        print(f"\n✅ {self.environment} environment teardown complete!")


if __name__ == "__main__":
    project_id = os.getenv('GCP_PROJECT_ID', 'your-project-id')
    
    if project_id != 'your-project-id':
        provisioner = InfrastructureProvisioner(project_id, environment="dev")
        
        # Provision infrastructure
        # web_tier = provisioner.provision_web_tier()
        # app_tier = provisioner.provision_app_tier()
        
        # Teardown when done
        # provisioner.teardown_environment()
        
        print("Infrastructure provisioner ready.")
        print("Uncomment lines in main to provision/teardown infrastructure.")
    else:
        print("Please set GCP_PROJECT_ID environment variable")
```

---

## Practice Challenges

### Challenge 1: Auto-Scaling Infrastructure Manager
Create a script that monitors VM CPU usage and automatically scales the number of instances.

**Requirements:**
- Monitor instance metrics
- Scale up when CPU > 70%
- Scale down when CPU < 30%
- Minimum 2, maximum 10 instances

### Challenge 2: Multi-Region Backup System
Build an automated backup system that:
- Backs up GCS buckets to multiple regions
- Verifies backup integrity
- Implements retention policies
- Sends notifications on completion

### Challenge 3: GKE Cluster Manager
Create a comprehensive GKE management tool that:
- Creates clusters with custom node pools
- Deploys applications
- Manages cluster upgrades
- Implements backup/restore

### Challenge 4: Cost Optimization Tool
Build a tool that:
- Identifies unused resources
- Stops idle VMs
- Deletes old snapshots
- Generates cost reports

---

## What You Learned

In this lab, you learned:

✅ **GCP Python SDK Setup**
- Installing and configuring google-cloud libraries
- Authentication methods (gcloud CLI, service accounts)
- Project and credential management

✅ **Compute Engine Automation**
- Listing and managing VM instances
- Creating instances programmatically
- Lifecycle management (start, stop, delete)
- Using startup scripts

✅ **Cloud Storage Automation**
- Managing buckets and objects
- Uploading and downloading files
- Setting permissions and access control
- Directory synchronization

✅ **GKE Automation**
- Listing and managing clusters
- Creating GKE clusters programmatically
- Node pool configuration
- Cluster operations

✅ **Infrastructure as Code**
- Provisioning complete environments
- Managing multi-tier architectures
- Resource labeling and tagging
- Environment teardown

✅ **Best Practices**
- Error handling for cloud operations
- Waiting for long-running operations
- Resource cleanup
- Security with service accounts

## Next Steps

- Explore other GCP services (Cloud Functions, Cloud Run, etc.)
- Implement infrastructure monitoring and alerting
- Build CI/CD pipelines with Cloud Build
- Learn Terraform for declarative infrastructure
- Implement disaster recovery strategies

## Additional Resources

- [Google Cloud Python Client Libraries](https://cloud.google.com/python/docs/reference)
- [Google Cloud Compute API](https://cloud.google.com/compute/docs/api)
- [Google Cloud Storage API](https://cloud.google.com/storage/docs/apis)
- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [GCP Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)
