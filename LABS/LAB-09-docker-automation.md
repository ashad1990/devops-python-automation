# LAB 09: Docker Automation with Python

## Learning Objectives
By the end of this lab, you will be able to:
- Use Docker SDK for Python to manage containers programmatically
- Build and manage Docker images using Python
- Automate container lifecycle operations
- Work with Docker networks and volumes
- Implement container health monitoring
- Build automated deployment scripts
- Handle Docker events and logs
- Apply DevOps automation patterns with containers

## Prerequisites
- Python 3.8+ installed
- Docker installed and running
- Basic understanding of Docker concepts (containers, images, volumes)
- Docker daemon accessible

## Setup

### Install Docker SDK

```bash
# Install Docker SDK for Python
pip install docker

# Verify Docker is running
docker --version
docker ps
```

### Test Docker Connection

Create `test_docker.py`:

```python
import docker

try:
    client = docker.from_env()
    print(f"✅ Docker connected successfully!")
    print(f"   Docker version: {client.version()['Version']}")
    print(f"   API version: {client.version()['ApiVersion']}")
except Exception as e:
    print(f"❌ Error connecting to Docker: {e}")
    print("   Make sure Docker daemon is running")
```

---

## Part 1: Container Management

### Exercise 1.1: List and Inspect Containers

Create `list_containers.py`:

```python
import docker
from datetime import datetime


class DockerManager:
    """Manage Docker containers."""
    
    def __init__(self):
        self.client = docker.from_env()
    
    def list_containers(self, all_containers=True):
        """List all containers."""
        containers = self.client.containers.list(all=all_containers)
        
        print(f"\n{'='*80}")
        print(f"Docker Containers ({len(containers)} total)")
        print(f"{'='*80}\n")
        
        if not containers:
            print("No containers found.")
            return containers
        
        for container in containers:
            # Status emoji
            status_emoji = {
                'running': '🟢',
                'exited': '🔴',
                'paused': '⏸️',
                'created': '⚪'
            }.get(container.status, '❓')
            
            print(f"{status_emoji} {container.name}")
            print(f"   ID: {container.short_id}")
            print(f"   Image: {container.image.tags[0] if container.image.tags else 'N/A'}")
            print(f"   Status: {container.status}")
            print(f"   Created: {container.attrs['Created'][:19]}")
            
            if container.status == 'running':
                # Get ports
                ports = container.attrs['NetworkSettings']['Ports']
                if ports:
                    print(f"   Ports:")
                    for container_port, host_bindings in ports.items():
                        if host_bindings:
                            for binding in host_bindings:
                                print(f"     {binding['HostPort']} -> {container_port}")
            
            print()
        
        return containers
    
    def inspect_container(self, container_name):
        """Get detailed information about a container."""
        try:
            container = self.client.containers.get(container_name)
            
            print(f"\n{'='*80}")
            print(f"Container: {container.name}")
            print(f"{'='*80}\n")
            
            print(f"ID: {container.id}")
            print(f"Short ID: {container.short_id}")
            print(f"Status: {container.status}")
            print(f"Image: {container.image.tags[0] if container.image.tags else 'N/A'}")
            
            # Network info
            print(f"\nNetwork:")
            networks = container.attrs['NetworkSettings']['Networks']
            for network_name, network_info in networks.items():
                print(f"  {network_name}:")
                print(f"    IP: {network_info.get('IPAddress', 'N/A')}")
                print(f"    Gateway: {network_info.get('Gateway', 'N/A')}")
            
            # Environment variables
            print(f"\nEnvironment Variables:")
            env_vars = container.attrs['Config']['Env']
            for env in env_vars[:10]:  # Show first 10
                print(f"  {env}")
            
            # Mounts
            print(f"\nMounts:")
            mounts = container.attrs['Mounts']
            if mounts:
                for mount in mounts:
                    print(f"  {mount['Source']} -> {mount['Destination']}")
            else:
                print("  No mounts")
            
            # Resource limits
            print(f"\nResource Limits:")
            host_config = container.attrs['HostConfig']
            print(f"  Memory: {host_config.get('Memory', 'unlimited')}")
            print(f"  CPU Shares: {host_config.get('CpuShares', 'default')}")
            
            return container
            
        except docker.errors.NotFound:
            print(f"❌ Container '{container_name}' not found")
            return None
        except Exception as e:
            print(f"❌ Error inspecting container: {e}")
            return None
    
    def get_container_stats(self, container_name):
        """Get real-time stats for a container."""
        try:
            container = self.client.containers.get(container_name)
            
            if container.status != 'running':
                print(f"❌ Container '{container_name}' is not running")
                return None
            
            print(f"\n📊 Real-time stats for {container_name}:")
            print(f"{'='*60}\n")
            
            stats = container.stats(stream=False)
            
            # CPU usage
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            cpu_percent = (cpu_delta / system_delta) * 100.0
            
            print(f"CPU Usage: {cpu_percent:.2f}%")
            
            # Memory usage
            mem_usage = stats['memory_stats']['usage'] / (1024 * 1024)  # MB
            mem_limit = stats['memory_stats']['limit'] / (1024 * 1024)  # MB
            mem_percent = (stats['memory_stats']['usage'] / stats['memory_stats']['limit']) * 100
            
            print(f"Memory: {mem_usage:.2f}MB / {mem_limit:.2f}MB ({mem_percent:.2f}%)")
            
            # Network I/O
            networks = stats['networks']
            for network_name, network_stats in networks.items():
                rx_mb = network_stats['rx_bytes'] / (1024 * 1024)
                tx_mb = network_stats['tx_bytes'] / (1024 * 1024)
                print(f"\nNetwork ({network_name}):")
                print(f"  RX: {rx_mb:.2f}MB")
                print(f"  TX: {tx_mb:.2f}MB")
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return None


if __name__ == "__main__":
    manager = DockerManager()
    
    # List all containers
    manager.list_containers(all_containers=True)
    
    # Inspect specific container (uncomment and replace with your container name)
    # manager.inspect_container("my_container")
    
    # Get stats (uncomment and replace with running container name)
    # manager.get_container_stats("my_container")
```

### Exercise 1.2: Run and Manage Containers

Create `run_containers.py`:

```python
import docker
import time


class ContainerRunner:
    """Run and manage Docker containers."""
    
    def __init__(self):
        self.client = docker.from_env()
    
    def run_nginx(self, container_name="my-nginx", port=8080):
        """Run an nginx container."""
        try:
            print(f"🚀 Starting nginx container '{container_name}'...")
            
            container = self.client.containers.run(
                "nginx:latest",
                name=container_name,
                ports={'80/tcp': port},
                detach=True,
                remove=False,
                environment={
                    'NGINX_HOST': 'localhost',
                    'NGINX_PORT': '80'
                }
            )
            
            print(f"✅ Container started successfully!")
            print(f"   Container ID: {container.short_id}")
            print(f"   Access at: http://localhost:{port}")
            
            return container
            
        except docker.errors.APIError as e:
            if "Conflict" in str(e):
                print(f"⚠️  Container '{container_name}' already exists")
                return self.client.containers.get(container_name)
            else:
                print(f"❌ Error running container: {e}")
                return None
    
    def run_redis(self, container_name="my-redis", port=6379):
        """Run a Redis container."""
        try:
            print(f"🚀 Starting Redis container '{container_name}'...")
            
            container = self.client.containers.run(
                "redis:latest",
                name=container_name,
                ports={'6379/tcp': port},
                detach=True,
                remove=False,
                command="redis-server --appendonly yes"
            )
            
            print(f"✅ Redis container started!")
            print(f"   Container ID: {container.short_id}")
            print(f"   Connect at: localhost:{port}")
            
            return container
            
        except docker.errors.APIError as e:
            if "Conflict" in str(e):
                print(f"⚠️  Container '{container_name}' already exists")
                return self.client.containers.get(container_name)
            else:
                print(f"❌ Error running container: {e}")
                return None
    
    def run_mysql(self, container_name="my-mysql", port=3306, root_password="rootpass"):
        """Run a MySQL container."""
        try:
            print(f"🚀 Starting MySQL container '{container_name}'...")
            
            container = self.client.containers.run(
                "mysql:8.0",
                name=container_name,
                ports={'3306/tcp': port},
                detach=True,
                remove=False,
                environment={
                    'MYSQL_ROOT_PASSWORD': root_password,
                    'MYSQL_DATABASE': 'devops_db'
                }
            )
            
            print(f"✅ MySQL container started!")
            print(f"   Container ID: {container.short_id}")
            print(f"   Root password: {root_password}")
            print(f"   Database: devops_db")
            print(f"   Connect at: localhost:{port}")
            print(f"\n   Waiting for MySQL to be ready...")
            
            # Wait for MySQL to be ready
            time.sleep(10)
            
            return container
            
        except docker.errors.APIError as e:
            if "Conflict" in str(e):
                print(f"⚠️  Container '{container_name}' already exists")
                return self.client.containers.get(container_name)
            else:
                print(f"❌ Error running container: {e}")
                return None
    
    def stop_container(self, container_name, timeout=10):
        """Stop a running container."""
        try:
            container = self.client.containers.get(container_name)
            
            print(f"⏹️  Stopping container '{container_name}'...")
            container.stop(timeout=timeout)
            print(f"✅ Container stopped")
            
        except docker.errors.NotFound:
            print(f"❌ Container '{container_name}' not found")
        except Exception as e:
            print(f"❌ Error stopping container: {e}")
    
    def start_container(self, container_name):
        """Start a stopped container."""
        try:
            container = self.client.containers.get(container_name)
            
            print(f"▶️  Starting container '{container_name}'...")
            container.start()
            print(f"✅ Container started")
            
        except docker.errors.NotFound:
            print(f"❌ Container '{container_name}' not found")
        except Exception as e:
            print(f"❌ Error starting container: {e}")
    
    def restart_container(self, container_name, timeout=10):
        """Restart a container."""
        try:
            container = self.client.containers.get(container_name)
            
            print(f"🔄 Restarting container '{container_name}'...")
            container.restart(timeout=timeout)
            print(f"✅ Container restarted")
            
        except docker.errors.NotFound:
            print(f"❌ Container '{container_name}' not found")
        except Exception as e:
            print(f"❌ Error restarting container: {e}")
    
    def remove_container(self, container_name, force=False):
        """Remove a container."""
        try:
            container = self.client.containers.get(container_name)
            
            print(f"🗑️  Removing container '{container_name}'...")
            container.remove(force=force)
            print(f"✅ Container removed")
            
        except docker.errors.NotFound:
            print(f"❌ Container '{container_name}' not found")
        except Exception as e:
            print(f"❌ Error removing container: {e}")
    
    def exec_command(self, container_name, command):
        """Execute a command in a running container."""
        try:
            container = self.client.containers.get(container_name)
            
            if container.status != 'running':
                print(f"❌ Container '{container_name}' is not running")
                return None
            
            print(f"🔧 Executing in {container_name}: {command}")
            
            result = container.exec_run(command)
            output = result.output.decode('utf-8')
            
            print(f"\nOutput:")
            print(output)
            print(f"\nExit Code: {result.exit_code}")
            
            return output
            
        except Exception as e:
            print(f"❌ Error executing command: {e}")
            return None
    
    def get_logs(self, container_name, tail=50):
        """Get container logs."""
        try:
            container = self.client.containers.get(container_name)
            
            print(f"\n📋 Logs for {container_name} (last {tail} lines):")
            print(f"{'='*60}\n")
            
            logs = container.logs(tail=tail).decode('utf-8')
            print(logs)
            
            return logs
            
        except Exception as e:
            print(f"❌ Error getting logs: {e}")
            return None


if __name__ == "__main__":
    runner = ContainerRunner()
    
    # Example: Run nginx
    container = runner.run_nginx("test-nginx", port=8080)
    
    if container:
        # Wait a bit
        time.sleep(2)
        
        # Get logs
        runner.get_logs("test-nginx", tail=20)
        
        # Execute command
        runner.exec_command("test-nginx", "nginx -v")
        
        # Cleanup (uncomment to remove)
        # runner.stop_container("test-nginx")
        # runner.remove_container("test-nginx")
```

---

## Part 2: Image Management

### Exercise 2.1: Build and Manage Images

Create `image_manager.py`:

```python
import docker
import io
import os


class ImageManager:
    """Manage Docker images."""
    
    def __init__(self):
        self.client = docker.from_env()
    
    def list_images(self):
        """List all Docker images."""
        images = self.client.images.list()
        
        print(f"\n{'='*80}")
        print(f"Docker Images ({len(images)} total)")
        print(f"{'='*80}\n")
        
        if not images:
            print("No images found.")
            return images
        
        for image in images:
            tags = image.tags if image.tags else ['<none>']
            size_mb = image.attrs['Size'] / (1024 * 1024)
            
            print(f"🐳 {tags[0]}")
            print(f"   ID: {image.short_id}")
            print(f"   Size: {size_mb:.2f} MB")
            print(f"   Created: {image.attrs['Created'][:19]}")
            
            if len(tags) > 1:
                print(f"   Also tagged as:")
                for tag in tags[1:]:
                    print(f"     - {tag}")
            
            print()
        
        return images
    
    def pull_image(self, image_name, tag="latest"):
        """Pull an image from Docker Hub."""
        full_name = f"{image_name}:{tag}"
        
        print(f"⬇️  Pulling image: {full_name}")
        
        try:
            image = self.client.images.pull(image_name, tag=tag)
            print(f"✅ Image pulled successfully!")
            print(f"   ID: {image.short_id}")
            
            return image
            
        except Exception as e:
            print(f"❌ Error pulling image: {e}")
            return None
    
    def build_image(self, dockerfile_path, tag_name, build_args=None):
        """Build an image from a Dockerfile."""
        print(f"🔨 Building image: {tag_name}")
        print(f"   Dockerfile: {dockerfile_path}")
        
        try:
            # Build image
            image, build_logs = self.client.images.build(
                path=os.path.dirname(dockerfile_path),
                dockerfile=os.path.basename(dockerfile_path),
                tag=tag_name,
                buildargs=build_args or {},
                rm=True
            )
            
            # Print build logs
            for log in build_logs:
                if 'stream' in log:
                    print(log['stream'].strip())
            
            print(f"\n✅ Image built successfully!")
            print(f"   Tag: {tag_name}")
            print(f"   ID: {image.short_id}")
            
            return image
            
        except Exception as e:
            print(f"❌ Error building image: {e}")
            return None
    
    def build_from_string(self, dockerfile_content, tag_name):
        """Build an image from Dockerfile content string."""
        print(f"🔨 Building image from content: {tag_name}")
        
        try:
            # Create file-like object from string
            f = io.BytesIO(dockerfile_content.encode('utf-8'))
            
            image, build_logs = self.client.images.build(
                fileobj=f,
                tag=tag_name,
                rm=True
            )
            
            # Print build logs
            for log in build_logs:
                if 'stream' in log:
                    print(log['stream'].strip())
            
            print(f"\n✅ Image built successfully!")
            print(f"   Tag: {tag_name}")
            
            return image
            
        except Exception as e:
            print(f"❌ Error building image: {e}")
            return None
    
    def tag_image(self, image_name, new_tag):
        """Tag an existing image."""
        try:
            image = self.client.images.get(image_name)
            
            # Parse new tag
            if ':' in new_tag:
                repository, tag = new_tag.split(':', 1)
            else:
                repository = new_tag
                tag = 'latest'
            
            image.tag(repository, tag)
            print(f"✅ Image tagged: {new_tag}")
            
        except Exception as e:
            print(f"❌ Error tagging image: {e}")
    
    def remove_image(self, image_name, force=False):
        """Remove an image."""
        try:
            self.client.images.remove(image_name, force=force)
            print(f"✅ Image removed: {image_name}")
            
        except Exception as e:
            print(f"❌ Error removing image: {e}")
    
    def inspect_image(self, image_name):
        """Get detailed information about an image."""
        try:
            image = self.client.images.get(image_name)
            
            print(f"\n{'='*80}")
            print(f"Image: {image.tags[0] if image.tags else image.short_id}")
            print(f"{'='*80}\n")
            
            print(f"ID: {image.id}")
            print(f"Short ID: {image.short_id}")
            print(f"Created: {image.attrs['Created']}")
            print(f"Size: {image.attrs['Size'] / (1024 * 1024):.2f} MB")
            
            # Architecture
            print(f"\nArchitecture: {image.attrs['Architecture']}")
            print(f"OS: {image.attrs['Os']}")
            
            # Labels
            labels = image.attrs['Config'].get('Labels', {})
            if labels:
                print(f"\nLabels:")
                for key, value in labels.items():
                    print(f"  {key}: {value}")
            
            # Env variables
            env_vars = image.attrs['Config'].get('Env', [])
            if env_vars:
                print(f"\nEnvironment Variables:")
                for env in env_vars[:10]:
                    print(f"  {env}")
            
            # Exposed ports
            exposed_ports = image.attrs['Config'].get('ExposedPorts', {})
            if exposed_ports:
                print(f"\nExposed Ports:")
                for port in exposed_ports.keys():
                    print(f"  {port}")
            
            return image
            
        except Exception as e:
            print(f"❌ Error inspecting image: {e}")
            return None
    
    def prune_images(self, dangling_only=True):
        """Remove unused images."""
        filters = {'dangling': True} if dangling_only else {}
        
        print("🧹 Pruning unused images...")
        
        try:
            result = self.client.images.prune(filters=filters)
            
            deleted = result.get('ImagesDeleted', [])
            space_reclaimed = result.get('SpaceReclaimed', 0)
            
            print(f"✅ Pruned {len(deleted)} images")
            print(f"   Space reclaimed: {space_reclaimed / (1024 * 1024):.2f} MB")
            
            return result
            
        except Exception as e:
            print(f"❌ Error pruning images: {e}")
            return None


if __name__ == "__main__":
    manager = ImageManager()
    
    # List images
    manager.list_images()
    
    # Pull an image
    # manager.pull_image("nginx", "alpine")
    
    # Build from string
    dockerfile = """
    FROM python:3.9-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install -r requirements.txt
    COPY . .
    CMD ["python", "app.py"]
    """
    # manager.build_from_string(dockerfile, "my-python-app:latest")
```

### Exercise 2.2: Build Custom Application Image

Create `build_app.py`:

```python
import docker
import os
import tempfile


def create_python_app_image():
    """Build a complete Python web application image."""
    client = docker.from_env()
    
    # Create temporary directory for build context
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"📁 Creating build context in {tmpdir}")
        
        # Create Dockerfile
        dockerfile = """FROM python:3.9-slim

LABEL maintainer="devops@example.com"
LABEL version="1.0"
LABEL description="Python Flask DevOps App"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run application
CMD ["python", "app.py"]
"""
        
        # Create requirements.txt
        requirements = """flask==2.3.0
requests==2.31.0
gunicorn==21.2.0
"""
        
        # Create app.py
        app_code = """from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'DevOps Python Application',
        'hostname': socket.gethostname(),
        'version': '1.0'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/info')
def info():
    return jsonify({
        'python_version': os.sys.version,
        'environment': os.environ.get('ENVIRONMENT', 'development')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
"""
        
        # Write files
        with open(os.path.join(tmpdir, 'Dockerfile'), 'w') as f:
            f.write(dockerfile)
        
        with open(os.path.join(tmpdir, 'requirements.txt'), 'w') as f:
            f.write(requirements)
        
        with open(os.path.join(tmpdir, 'app.py'), 'w') as f:
            f.write(app_code)
        
        # Build image
        print("\n🔨 Building Docker image...")
        
        try:
            image, build_logs = client.images.build(
                path=tmpdir,
                tag='devops-python-app:latest',
                rm=True
            )
            
            for log in build_logs:
                if 'stream' in log:
                    print(log['stream'].strip())
            
            print(f"\n✅ Image built successfully!")
            print(f"   Tag: devops-python-app:latest")
            print(f"   ID: {image.short_id}")
            
            # Run container from the image
            print(f"\n🚀 Running container...")
            
            container = client.containers.run(
                'devops-python-app:latest',
                name='devops-app',
                ports={'5000/tcp': 5000},
                environment={'ENVIRONMENT': 'production'},
                detach=True,
                remove=False
            )
            
            print(f"✅ Container started!")
            print(f"   Container ID: {container.short_id}")
            print(f"   Access at: http://localhost:5000")
            print(f"\n   Test endpoints:")
            print(f"     http://localhost:5000/")
            print(f"     http://localhost:5000/health")
            print(f"     http://localhost:5000/info")
            
            return image, container
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None, None


if __name__ == "__main__":
    image, container = create_python_app_image()
    
    if container:
        print(f"\n💡 To stop and remove:")
        print(f"   docker stop devops-app")
        print(f"   docker rm devops-app")
```

---

## Part 3: Networks and Volumes

### Exercise 3.1: Manage Docker Networks

Create `network_manager.py`:

```python
import docker


class NetworkManager:
    """Manage Docker networks."""
    
    def __init__(self):
        self.client = docker.from_env()
    
    def list_networks(self):
        """List all Docker networks."""
        networks = self.client.networks.list()
        
        print(f"\n{'='*70}")
        print(f"Docker Networks ({len(networks)} total)")
        print(f"{'='*70}\n")
        
        for network in networks:
            print(f"🌐 {network.name}")
            print(f"   ID: {network.short_id}")
            print(f"   Driver: {network.attrs['Driver']}")
            print(f"   Scope: {network.attrs['Scope']}")
            
            # Connected containers
            containers = network.attrs.get('Containers', {})
            if containers:
                print(f"   Connected Containers: {len(containers)}")
                for container_id, container_info in containers.items():
                    print(f"     - {container_info['Name']}: {container_info['IPv4Address']}")
            
            print()
        
        return networks
    
    def create_network(self, name, driver='bridge'):
        """Create a new network."""
        try:
            print(f"🌐 Creating network: {name} (driver: {driver})")
            
            network = self.client.networks.create(
                name=name,
                driver=driver,
                check_duplicate=True
            )
            
            print(f"✅ Network created successfully!")
            print(f"   ID: {network.short_id}")
            
            return network
            
        except Exception as e:
            print(f"❌ Error creating network: {e}")
            return None
    
    def remove_network(self, name):
        """Remove a network."""
        try:
            network = self.client.networks.get(name)
            network.remove()
            print(f"✅ Network '{name}' removed")
            
        except Exception as e:
            print(f"❌ Error removing network: {e}")
    
    def connect_container(self, network_name, container_name):
        """Connect a container to a network."""
        try:
            network = self.client.networks.get(network_name)
            network.connect(container_name)
            print(f"✅ Connected '{container_name}' to '{network_name}'")
            
        except Exception as e:
            print(f"❌ Error connecting container: {e}")
    
    def disconnect_container(self, network_name, container_name):
        """Disconnect a container from a network."""
        try:
            network = self.client.networks.get(network_name)
            network.disconnect(container_name)
            print(f"✅ Disconnected '{container_name}' from '{network_name}'")
            
        except Exception as e:
            print(f"❌ Error disconnecting container: {e}")


class VolumeManager:
    """Manage Docker volumes."""
    
    def __init__(self):
        self.client = docker.from_env()
    
    def list_volumes(self):
        """List all Docker volumes."""
        volumes = self.client.volumes.list()
        
        print(f"\n{'='*70}")
        print(f"Docker Volumes ({len(volumes)} total)")
        print(f"{'='*70}\n")
        
        for volume in volumes:
            print(f"💾 {volume.name}")
            print(f"   Driver: {volume.attrs['Driver']}")
            print(f"   Mountpoint: {volume.attrs['Mountpoint']}")
            print(f"   Created: {volume.attrs['CreatedAt'][:19]}")
            print()
        
        return volumes
    
    def create_volume(self, name, driver='local'):
        """Create a new volume."""
        try:
            print(f"💾 Creating volume: {name}")
            
            volume = self.client.volumes.create(
                name=name,
                driver=driver
            )
            
            print(f"✅ Volume created successfully!")
            print(f"   Name: {volume.name}")
            print(f"   Mountpoint: {volume.attrs['Mountpoint']}")
            
            return volume
            
        except Exception as e:
            print(f"❌ Error creating volume: {e}")
            return None
    
    def remove_volume(self, name, force=False):
        """Remove a volume."""
        try:
            volume = self.client.volumes.get(name)
            volume.remove(force=force)
            print(f"✅ Volume '{name}' removed")
            
        except Exception as e:
            print(f"❌ Error removing volume: {e}")
    
    def prune_volumes(self):
        """Remove all unused volumes."""
        print("🧹 Pruning unused volumes...")
        
        try:
            result = self.client.volumes.prune()
            
            deleted = result.get('VolumesDeleted', [])
            space_reclaimed = result.get('SpaceReclaimed', 0)
            
            print(f"✅ Pruned {len(deleted) if deleted else 0} volumes")
            print(f"   Space reclaimed: {space_reclaimed / (1024 * 1024):.2f} MB")
            
        except Exception as e:
            print(f"❌ Error pruning volumes: {e}")


if __name__ == "__main__":
    net_manager = NetworkManager()
    vol_manager = VolumeManager()
    
    # List networks and volumes
    net_manager.list_networks()
    vol_manager.list_volumes()
    
    # Example: Create custom network
    # net_manager.create_network("my-app-network")
    
    # Example: Create volume
    # vol_manager.create_volume("my-data-volume")
```

---

## Part 4: Multi-Container Application

### Exercise 4.1: Deploy Multi-Tier Application

Create `deploy_stack.py`:

```python
import docker
import time


class ApplicationStack:
    """Deploy and manage multi-container application stack."""
    
    def __init__(self, stack_name="myapp"):
        self.client = docker.from_env()
        self.stack_name = stack_name
        self.network_name = f"{stack_name}-network"
        self.volume_name = f"{stack_name}-data"
    
    def deploy(self):
        """Deploy complete application stack."""
        print(f"\n{'='*70}")
        print(f"Deploying Application Stack: {self.stack_name}")
        print(f"{'='*70}\n")
        
        # 1. Create network
        print("1️⃣  Creating network...")
        try:
            network = self.client.networks.create(
                self.network_name,
                driver="bridge"
            )
            print(f"✅ Network created: {self.network_name}")
        except Exception as e:
            print(f"⚠️  Network may already exist: {e}")
            network = self.client.networks.get(self.network_name)
        
        # 2. Create volume for database
        print("\n2️⃣  Creating volume...")
        try:
            volume = self.client.volumes.create(self.volume_name)
            print(f"✅ Volume created: {self.volume_name}")
        except Exception as e:
            print(f"⚠️  Volume may already exist: {e}")
        
        # 3. Deploy Redis (cache)
        print("\n3️⃣  Deploying Redis...")
        redis_container = self._deploy_redis()
        
        # 4. Deploy PostgreSQL (database)
        print("\n4️⃣  Deploying PostgreSQL...")
        db_container = self._deploy_postgres()
        
        # Wait for database to be ready
        print("⏳ Waiting for database to be ready...")
        time.sleep(10)
        
        # 5. Deploy application
        print("\n5️⃣  Deploying application...")
        app_container = self._deploy_app()
        
        # 6. Deploy Nginx (reverse proxy)
        print("\n6️⃣  Deploying Nginx...")
        nginx_container = self._deploy_nginx()
        
        print(f"\n{'='*70}")
        print(f"✅ Stack Deployed Successfully!")
        print(f"{'='*70}\n")
        print(f"Access application at: http://localhost:8080")
        
        return {
            'network': network,
            'redis': redis_container,
            'database': db_container,
            'app': app_container,
            'nginx': nginx_container
        }
    
    def _deploy_redis(self):
        """Deploy Redis container."""
        container_name = f"{self.stack_name}-redis"
        
        try:
            container = self.client.containers.run(
                "redis:7-alpine",
                name=container_name,
                network=self.network_name,
                detach=True,
                remove=False
            )
            print(f"✅ Redis deployed: {container_name}")
            return container
        except docker.errors.APIError as e:
            if "Conflict" in str(e):
                print(f"⚠️  Redis already running")
                return self.client.containers.get(container_name)
            raise
    
    def _deploy_postgres(self):
        """Deploy PostgreSQL container."""
        container_name = f"{self.stack_name}-db"
        
        try:
            container = self.client.containers.run(
                "postgres:14-alpine",
                name=container_name,
                network=self.network_name,
                environment={
                    'POSTGRES_DB': 'appdb',
                    'POSTGRES_USER': 'appuser',
                    'POSTGRES_PASSWORD': 'apppass'
                },
                volumes={
                    self.volume_name: {'bind': '/var/lib/postgresql/data', 'mode': 'rw'}
                },
                detach=True,
                remove=False
            )
            print(f"✅ PostgreSQL deployed: {container_name}")
            return container
        except docker.errors.APIError as e:
            if "Conflict" in str(e):
                print(f"⚠️  PostgreSQL already running")
                return self.client.containers.get(container_name)
            raise
    
    def _deploy_app(self):
        """Deploy application container."""
        container_name = f"{self.stack_name}-app"
        
        try:
            container = self.client.containers.run(
                "python:3.9-slim",
                name=container_name,
                network=self.network_name,
                environment={
                    'DATABASE_URL': f'postgresql://appuser:apppass@{self.stack_name}-db:5432/appdb',
                    'REDIS_URL': f'redis://{self.stack_name}-redis:6379/0'
                },
                command='python -m http.server 5000',
                detach=True,
                remove=False
            )
            print(f"✅ Application deployed: {container_name}")
            return container
        except docker.errors.APIError as e:
            if "Conflict" in str(e):
                print(f"⚠️  Application already running")
                return self.client.containers.get(container_name)
            raise
    
    def _deploy_nginx(self):
        """Deploy Nginx reverse proxy."""
        container_name = f"{self.stack_name}-nginx"
        
        try:
            container = self.client.containers.run(
                "nginx:alpine",
                name=container_name,
                network=self.network_name,
                ports={'80/tcp': 8080},
                detach=True,
                remove=False
            )
            print(f"✅ Nginx deployed: {container_name}")
            return container
        except docker.errors.APIError as e:
            if "Conflict" in str(e):
                print(f"⚠️  Nginx already running")
                return self.client.containers.get(container_name)
            raise
    
    def status(self):
        """Show status of all stack components."""
        print(f"\n{'='*70}")
        print(f"Stack Status: {self.stack_name}")
        print(f"{'='*70}\n")
        
        components = ['redis', 'db', 'app', 'nginx']
        
        for component in components:
            container_name = f"{self.stack_name}-{component}"
            try:
                container = self.client.containers.get(container_name)
                status_emoji = '🟢' if container.status == 'running' else '🔴'
                print(f"{status_emoji} {component:10s} - {container.status}")
            except docker.errors.NotFound:
                print(f"⚪ {component:10s} - not found")
    
    def teardown(self):
        """Remove all stack components."""
        print(f"\n🗑️  Tearing down stack: {self.stack_name}")
        
        # Stop and remove containers
        components = ['nginx', 'app', 'db', 'redis']
        
        for component in components:
            container_name = f"{self.stack_name}-{component}"
            try:
                container = self.client.containers.get(container_name)
                print(f"Stopping {container_name}...")
                container.stop(timeout=10)
                container.remove()
                print(f"✅ Removed {container_name}")
            except docker.errors.NotFound:
                print(f"⚠️  {container_name} not found")
            except Exception as e:
                print(f"❌ Error removing {container_name}: {e}")
        
        # Remove network
        try:
            network = self.client.networks.get(self.network_name)
            network.remove()
            print(f"✅ Removed network: {self.network_name}")
        except Exception as e:
            print(f"❌ Error removing network: {e}")
        
        # Remove volume
        try:
            volume = self.client.volumes.get(self.volume_name)
            volume.remove()
            print(f"✅ Removed volume: {self.volume_name}")
        except Exception as e:
            print(f"❌ Error removing volume: {e}")
        
        print(f"\n✅ Stack teardown complete!")


if __name__ == "__main__":
    stack = ApplicationStack("devops-app")
    
    # Deploy stack
    stack.deploy()
    
    # Show status
    time.sleep(2)
    stack.status()
    
    # Teardown (uncomment to remove)
    # stack.teardown()
```

---

## Practice Challenges

### Challenge 1: Container Health Monitor
Build a monitoring tool that:
- Checks health of all running containers
- Restarts unhealthy containers
- Sends alerts for failures
- Logs container metrics

### Challenge 2: Auto-Scaling Container Manager
Create a system that:
- Monitors container CPU/memory usage
- Automatically scales containers up/down
- Implements load balancing
- Manages container lifecycle

### Challenge 3: CI/CD Pipeline with Docker
Build a pipeline that:
- Builds Docker images on code changes
- Runs tests in containers
- Pushes images to registry
- Deploys to staging/production

### Challenge 4: Docker Cleanup Automation
Create a cleanup tool that:
- Removes stopped containers older than X days
- Deletes unused images
- Prunes networks and volumes
- Generates cleanup reports

---

## What You Learned

In this lab, you learned:

✅ **Container Management**
- Listing and inspecting containers
- Running containers with various configurations
- Managing container lifecycle (start, stop, restart, remove)
- Executing commands in containers
- Viewing container logs and stats

✅ **Image Management**
- Listing and pulling images
- Building custom images from Dockerfiles
- Tagging and managing image versions
- Inspecting image details
- Pruning unused images

✅ **Networks and Volumes**
- Creating and managing Docker networks
- Connecting containers to networks
- Creating and managing volumes
- Implementing persistent storage
- Network isolation

✅ **Multi-Container Applications**
- Deploying multi-tier applications
- Managing container dependencies
- Implementing service discovery
- Orchestrating complex deployments

✅ **Automation Patterns**
- Building reusable Docker management classes
- Implementing error handling
- Automating deployment workflows
- Infrastructure as Code with Docker

## Next Steps

- Learn Docker Compose for declarative deployments
- Explore container orchestration with Kubernetes
- Implement Docker Registry for private images
- Study Docker security best practices
- Build production-ready containerized applications

## Additional Resources

- [Docker SDK for Python Documentation](https://docker-py.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Container Security](https://docs.docker.com/engine/security/)
- [Docker Compose](https://docs.docker.com/compose/)
