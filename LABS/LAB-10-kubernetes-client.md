# LAB 10: Kubernetes Python Client

## Learning Objectives
By the end of this lab, you will be able to:
- Use the Kubernetes Python client to interact with clusters
- List and manage Kubernetes resources programmatically
- Create and deploy applications to Kubernetes
- Scale deployments and manage replicas
- Work with ConfigMaps and Secrets
- Monitor pod status and logs
- Implement automated Kubernetes operations
- Apply DevOps automation patterns with Kubernetes

## Prerequisites
- Python 3.8+ installed
- Kubernetes cluster access (minikube, kind, GKE, EKS, or AKS)
- kubectl configured and working
- Basic understanding of Kubernetes concepts

## Setup

### Install Kubernetes Python Client

```bash
# Install the Kubernetes Python client
pip install kubernetes

# Verify kubectl is configured
kubectl cluster-info
kubectl get nodes
```

### Test Kubernetes Connection

Create `test_k8s.py`:

```python
from kubernetes import client, config

try:
    # Load kubeconfig
    config.load_kube_config()
    
    # Create API client
    v1 = client.CoreV1Api()
    
    print("✅ Kubernetes client configured successfully!")
    
    # List nodes
    nodes = v1.list_node()
    print(f"\nCluster has {len(nodes.items)} node(s):")
    for node in nodes.items:
        print(f"  - {node.metadata.name}")
        
except Exception as e:
    print(f"❌ Error connecting to Kubernetes: {e}")
    print("   Make sure kubectl is configured correctly")
```

---

## Part 1: Listing Resources

### Exercise 1.1: List Pods, Deployments, and Services

Create `list_resources.py`:

```python
from kubernetes import client, config
from datetime import datetime


class KubernetesManager:
    """Manage Kubernetes resources."""
    
    def __init__(self):
        # Load kubeconfig
        config.load_kube_config()
        
        # Create API clients
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
    
    def list_namespaces(self):
        """List all namespaces."""
        try:
            namespaces = self.core_v1.list_namespace()
            
            print(f"\n{'='*70}")
            print(f"Namespaces ({len(namespaces.items)} total)")
            print(f"{'='*70}\n")
            
            for ns in namespaces.items:
                status = ns.status.phase
                age = self._get_age(ns.metadata.creation_timestamp)
                
                print(f"📦 {ns.metadata.name}")
                print(f"   Status: {status}")
                print(f"   Age: {age}")
                print()
            
            return namespaces.items
            
        except Exception as e:
            print(f"❌ Error listing namespaces: {e}")
            return []
    
    def list_pods(self, namespace="default"):
        """List all pods in a namespace."""
        try:
            pods = self.core_v1.list_namespaced_pod(namespace)
            
            print(f"\n{'='*70}")
            print(f"Pods in namespace '{namespace}' ({len(pods.items)} total)")
            print(f"{'='*70}\n")
            
            if not pods.items:
                print("No pods found.")
                return []
            
            for pod in pods.items:
                # Status emoji
                phase = pod.status.phase
                status_emoji = {
                    'Running': '🟢',
                    'Pending': '🟡',
                    'Succeeded': '✅',
                    'Failed': '❌',
                    'Unknown': '❓'
                }.get(phase, '⚪')
                
                print(f"{status_emoji} {pod.metadata.name}")
                print(f"   Namespace: {pod.metadata.namespace}")
                print(f"   Status: {phase}")
                print(f"   Node: {pod.spec.node_name or 'Not scheduled'}")
                print(f"   IP: {pod.status.pod_ip or 'N/A'}")
                
                # Container info
                if pod.spec.containers:
                    print(f"   Containers:")
                    for container in pod.spec.containers:
                        print(f"     - {container.name}: {container.image}")
                
                # Restarts
                if pod.status.container_statuses:
                    total_restarts = sum(
                        cs.restart_count for cs in pod.status.container_statuses
                    )
                    if total_restarts > 0:
                        print(f"   ⚠️  Restarts: {total_restarts}")
                
                age = self._get_age(pod.metadata.creation_timestamp)
                print(f"   Age: {age}")
                print()
            
            return pods.items
            
        except Exception as e:
            print(f"❌ Error listing pods: {e}")
            return []
    
    def list_deployments(self, namespace="default"):
        """List all deployments in a namespace."""
        try:
            deployments = self.apps_v1.list_namespaced_deployment(namespace)
            
            print(f"\n{'='*70}")
            print(f"Deployments in namespace '{namespace}' ({len(deployments.items)} total)")
            print(f"{'='*70}\n")
            
            if not deployments.items:
                print("No deployments found.")
                return []
            
            for deploy in deployments.items:
                ready_replicas = deploy.status.ready_replicas or 0
                desired_replicas = deploy.spec.replicas
                
                # Status emoji
                if ready_replicas == desired_replicas:
                    status_emoji = '✅'
                elif ready_replicas == 0:
                    status_emoji = '❌'
                else:
                    status_emoji = '⚠️'
                
                print(f"{status_emoji} {deploy.metadata.name}")
                print(f"   Replicas: {ready_replicas}/{desired_replicas} ready")
                print(f"   Available: {deploy.status.available_replicas or 0}")
                print(f"   Updated: {deploy.status.updated_replicas or 0}")
                
                # Image
                if deploy.spec.template.spec.containers:
                    container = deploy.spec.template.spec.containers[0]
                    print(f"   Image: {container.image}")
                
                age = self._get_age(deploy.metadata.creation_timestamp)
                print(f"   Age: {age}")
                print()
            
            return deployments.items
            
        except Exception as e:
            print(f"❌ Error listing deployments: {e}")
            return []
    
    def list_services(self, namespace="default"):
        """List all services in a namespace."""
        try:
            services = self.core_v1.list_namespaced_service(namespace)
            
            print(f"\n{'='*70}")
            print(f"Services in namespace '{namespace}' ({len(services.items)} total)")
            print(f"{'='*70}\n")
            
            if not services.items:
                print("No services found.")
                return []
            
            for svc in services.items:
                print(f"🌐 {svc.metadata.name}")
                print(f"   Type: {svc.spec.type}")
                print(f"   Cluster IP: {svc.spec.cluster_ip}")
                
                # Ports
                if svc.spec.ports:
                    print(f"   Ports:")
                    for port in svc.spec.ports:
                        node_port = f":{port.node_port}" if port.node_port else ""
                        print(f"     {port.port}/{port.protocol} -> {port.target_port}{node_port}")
                
                # External IPs
                if svc.status.load_balancer.ingress:
                    print(f"   External IPs:")
                    for ingress in svc.status.load_balancer.ingress:
                        ip = ingress.ip or ingress.hostname
                        print(f"     {ip}")
                
                age = self._get_age(svc.metadata.creation_timestamp)
                print(f"   Age: {age}")
                print()
            
            return services.items
            
        except Exception as e:
            print(f"❌ Error listing services: {e}")
            return []
    
    def _get_age(self, creation_timestamp):
        """Calculate resource age."""
        if not creation_timestamp:
            return "Unknown"
        
        now = datetime.now(creation_timestamp.tzinfo)
        age = now - creation_timestamp
        
        days = age.days
        hours = age.seconds // 3600
        minutes = (age.seconds % 3600) // 60
        
        if days > 0:
            return f"{days}d{hours}h"
        elif hours > 0:
            return f"{hours}h{minutes}m"
        else:
            return f"{minutes}m"
    
    def get_pod_logs(self, pod_name, namespace="default", tail_lines=50):
        """Get logs from a pod."""
        try:
            logs = self.core_v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                tail_lines=tail_lines
            )
            
            print(f"\n{'='*70}")
            print(f"Logs for pod '{pod_name}' (last {tail_lines} lines)")
            print(f"{'='*70}\n")
            print(logs)
            
            return logs
            
        except Exception as e:
            print(f"❌ Error getting logs: {e}")
            return None


if __name__ == "__main__":
    manager = KubernetesManager()
    
    # List namespaces
    manager.list_namespaces()
    
    # List resources in default namespace
    manager.list_pods()
    manager.list_deployments()
    manager.list_services()
    
    # Get logs from a pod (uncomment and replace with your pod name)
    # manager.get_pod_logs("my-pod-name")
```

---

## Part 2: Creating Resources

### Exercise 2.1: Create Deployments

Create `create_deployment.py`:

```python
from kubernetes import client, config
import time


def create_nginx_deployment(name="nginx-deployment", replicas=3, namespace="default"):
    """Create an nginx deployment."""
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    
    # Define container
    container = client.V1Container(
        name="nginx",
        image="nginx:1.24",
        ports=[client.V1ContainerPort(container_port=80)],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "100m", "memory": "128Mi"},
            limits={"cpu": "500m", "memory": "512Mi"}
        )
    )
    
    # Define pod template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container])
    )
    
    # Define deployment spec
    spec = client.V1DeploymentSpec(
        replicas=replicas,
        selector=client.V1LabelSelector(
            match_labels={"app": name}
        ),
        template=template
    )
    
    # Create deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec
    )
    
    # Create deployment
    try:
        print(f"🚀 Creating deployment '{name}'...")
        
        api_response = apps_v1.create_namespaced_deployment(
            namespace=namespace,
            body=deployment
        )
        
        print(f"✅ Deployment created successfully!")
        print(f"   Name: {api_response.metadata.name}")
        print(f"   Namespace: {namespace}")
        print(f"   Replicas: {replicas}")
        
        # Wait for deployment to be ready
        print(f"\n⏳ Waiting for deployment to be ready...")
        wait_for_deployment(name, namespace)
        
        return api_response
        
    except client.exceptions.ApiException as e:
        if e.status == 409:
            print(f"⚠️  Deployment '{name}' already exists")
        else:
            print(f"❌ Error creating deployment: {e}")
        return None


def wait_for_deployment(name, namespace="default", timeout=300):
    """Wait for deployment to be ready."""
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            deployment = apps_v1.read_namespaced_deployment(name, namespace)
            
            ready_replicas = deployment.status.ready_replicas or 0
            desired_replicas = deployment.spec.replicas
            
            print(f"   Status: {ready_replicas}/{desired_replicas} replicas ready")
            
            if ready_replicas == desired_replicas:
                print(f"✅ Deployment is ready!")
                return True
            
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ Error checking deployment: {e}")
            return False
    
    print(f"⚠️  Timeout waiting for deployment to be ready")
    return False


def create_python_app_deployment(name="python-app", replicas=2, namespace="default"):
    """Create a Python Flask app deployment."""
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    
    # Define container
    container = client.V1Container(
        name="app",
        image="python:3.9-slim",
        command=["/bin/sh"],
        args=[
            "-c",
            "pip install flask && "
            "python -c \""
            "from flask import Flask, jsonify; "
            "import socket; "
            "app = Flask(__name__); "
            "@app.route('/') "
            "def home(): return jsonify({'message': 'Hello from K8s!', 'pod': socket.gethostname()}); "
            "@app.route('/health') "
            "def health(): return jsonify({'status': 'healthy'}); "
            "app.run(host='0.0.0.0', port=5000)"
            "\""
        ],
        ports=[client.V1ContainerPort(container_port=5000)],
        liveness_probe=client.V1Probe(
            http_get=client.V1HTTPGetAction(
                path="/health",
                port=5000
            ),
            initial_delay_seconds=30,
            period_seconds=10
        ),
        readiness_probe=client.V1Probe(
            http_get=client.V1HTTPGetAction(
                path="/health",
                port=5000
            ),
            initial_delay_seconds=5,
            period_seconds=5
        )
    )
    
    # Pod template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container])
    )
    
    # Deployment spec
    spec = client.V1DeploymentSpec(
        replicas=replicas,
        selector=client.V1LabelSelector(match_labels={"app": name}),
        template=template
    )
    
    # Create deployment
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec
    )
    
    try:
        print(f"🚀 Creating Python app deployment '{name}'...")
        
        api_response = apps_v1.create_namespaced_deployment(
            namespace=namespace,
            body=deployment
        )
        
        print(f"✅ Deployment created!")
        print(f"   Name: {name}")
        print(f"   Replicas: {replicas}")
        
        return api_response
        
    except client.exceptions.ApiException as e:
        if e.status == 409:
            print(f"⚠️  Deployment '{name}' already exists")
        else:
            print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    # Create nginx deployment
    create_nginx_deployment("nginx-test", replicas=3)
    
    # Create Python app deployment
    # create_python_app_deployment("python-app", replicas=2)
```

### Exercise 2.2: Create Services

Create `create_service.py`:

```python
from kubernetes import client, config


def create_service(
    name,
    selector_app,
    port=80,
    target_port=80,
    service_type="ClusterIP",
    namespace="default"
):
    """Create a Kubernetes service."""
    config.load_kube_config()
    core_v1 = client.CoreV1Api()
    
    # Define service spec
    spec = client.V1ServiceSpec(
        type=service_type,
        selector={"app": selector_app},
        ports=[
            client.V1ServicePort(
                port=port,
                target_port=target_port,
                protocol="TCP"
            )
        ]
    )
    
    # Create service object
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec
    )
    
    try:
        print(f"🌐 Creating service '{name}'...")
        
        api_response = core_v1.create_namespaced_service(
            namespace=namespace,
            body=service
        )
        
        print(f"✅ Service created successfully!")
        print(f"   Name: {api_response.metadata.name}")
        print(f"   Type: {service_type}")
        print(f"   Port: {port} -> {target_port}")
        print(f"   Selector: app={selector_app}")
        
        if service_type == "ClusterIP":
            print(f"   Cluster IP: {api_response.spec.cluster_ip}")
        
        return api_response
        
    except client.exceptions.ApiException as e:
        if e.status == 409:
            print(f"⚠️  Service '{name}' already exists")
        else:
            print(f"❌ Error creating service: {e}")
        return None


def create_loadbalancer_service(
    name,
    selector_app,
    port=80,
    target_port=80,
    namespace="default"
):
    """Create a LoadBalancer service."""
    return create_service(
        name=name,
        selector_app=selector_app,
        port=port,
        target_port=target_port,
        service_type="LoadBalancer",
        namespace=namespace
    )


def create_nodeport_service(
    name,
    selector_app,
    port=80,
    target_port=80,
    node_port=None,
    namespace="default"
):
    """Create a NodePort service."""
    config.load_kube_config()
    core_v1 = client.CoreV1Api()
    
    # Define service port
    service_port = client.V1ServicePort(
        port=port,
        target_port=target_port,
        protocol="TCP"
    )
    
    if node_port:
        service_port.node_port = node_port
    
    # Define service spec
    spec = client.V1ServiceSpec(
        type="NodePort",
        selector={"app": selector_app},
        ports=[service_port]
    )
    
    # Create service
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec
    )
    
    try:
        print(f"🌐 Creating NodePort service '{name}'...")
        
        api_response = core_v1.create_namespaced_service(
            namespace=namespace,
            body=service
        )
        
        actual_node_port = api_response.spec.ports[0].node_port
        
        print(f"✅ Service created!")
        print(f"   Type: NodePort")
        print(f"   Port: {port} -> {target_port}")
        print(f"   NodePort: {actual_node_port}")
        
        return api_response
        
    except client.exceptions.ApiException as e:
        if e.status == 409:
            print(f"⚠️  Service '{name}' already exists")
        else:
            print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    # Create ClusterIP service for nginx
    create_service(
        name="nginx-service",
        selector_app="nginx-test",
        port=80,
        target_port=80
    )
    
    # Create NodePort service
    # create_nodeport_service(
    #     name="nginx-nodeport",
    #     selector_app="nginx-test",
    #     port=80,
    #     target_port=80,
    #     node_port=30080
    # )
```

---

## Part 3: Scaling and Updates

### Exercise 3.1: Scale Deployments

Create `scale_deployment.py`:

```python
from kubernetes import client, config
import time


class DeploymentScaler:
    """Scale Kubernetes deployments."""
    
    def __init__(self):
        config.load_kube_config()
        self.apps_v1 = client.AppsV1Api()
    
    def scale_deployment(self, name, replicas, namespace="default"):
        """Scale a deployment to specified replica count."""
        try:
            print(f"📊 Scaling deployment '{name}' to {replicas} replicas...")
            
            # Get current deployment
            deployment = self.apps_v1.read_namespaced_deployment(name, namespace)
            current_replicas = deployment.spec.replicas
            
            print(f"   Current replicas: {current_replicas}")
            print(f"   Target replicas: {replicas}")
            
            # Update replica count
            deployment.spec.replicas = replicas
            
            # Patch deployment
            api_response = self.apps_v1.patch_namespaced_deployment(
                name=name,
                namespace=namespace,
                body=deployment
            )
            
            print(f"✅ Scaling initiated!")
            
            # Wait for scaling to complete
            self._wait_for_scale(name, replicas, namespace)
            
            return api_response
            
        except Exception as e:
            print(f"❌ Error scaling deployment: {e}")
            return None
    
    def _wait_for_scale(self, name, target_replicas, namespace, timeout=120):
        """Wait for deployment to scale."""
        print(f"\n⏳ Waiting for scaling to complete...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                deployment = self.apps_v1.read_namespaced_deployment(name, namespace)
                ready_replicas = deployment.status.ready_replicas or 0
                
                print(f"   {ready_replicas}/{target_replicas} replicas ready", end='\r')
                
                if ready_replicas == target_replicas:
                    print(f"\n✅ Scaling complete!")
                    return True
                
                time.sleep(2)
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                return False
        
        print(f"\n⚠️  Timeout waiting for scaling")
        return False
    
    def autoscale_deployment(
        self,
        name,
        min_replicas=2,
        max_replicas=10,
        cpu_percent=80,
        namespace="default"
    ):
        """Create horizontal pod autoscaler for deployment."""
        autoscaling_v1 = client.AutoscalingV1Api()
        
        try:
            print(f"📈 Creating HorizontalPodAutoscaler for '{name}'...")
            
            # Define HPA spec
            spec = client.V1HorizontalPodAutoscalerSpec(
                scale_target_ref=client.V1CrossVersionObjectReference(
                    api_version="apps/v1",
                    kind="Deployment",
                    name=name
                ),
                min_replicas=min_replicas,
                max_replicas=max_replicas,
                target_cpu_utilization_percentage=cpu_percent
            )
            
            # Create HPA
            hpa = client.V1HorizontalPodAutoscaler(
                api_version="autoscaling/v1",
                kind="HorizontalPodAutoscaler",
                metadata=client.V1ObjectMeta(name=f"{name}-hpa"),
                spec=spec
            )
            
            api_response = autoscaling_v1.create_namespaced_horizontal_pod_autoscaler(
                namespace=namespace,
                body=hpa
            )
            
            print(f"✅ HPA created!")
            print(f"   Min replicas: {min_replicas}")
            print(f"   Max replicas: {max_replicas}")
            print(f"   CPU target: {cpu_percent}%")
            
            return api_response
            
        except client.exceptions.ApiException as e:
            if e.status == 409:
                print(f"⚠️  HPA already exists")
            else:
                print(f"❌ Error: {e}")
            return None
    
    def get_deployment_status(self, name, namespace="default"):
        """Get detailed deployment status."""
        try:
            deployment = self.apps_v1.read_namespaced_deployment(name, namespace)
            
            print(f"\n{'='*70}")
            print(f"Deployment Status: {name}")
            print(f"{'='*70}\n")
            
            print(f"Replicas:")
            print(f"  Desired: {deployment.spec.replicas}")
            print(f"  Current: {deployment.status.replicas or 0}")
            print(f"  Ready: {deployment.status.ready_replicas or 0}")
            print(f"  Available: {deployment.status.available_replicas or 0}")
            print(f"  Updated: {deployment.status.updated_replicas or 0}")
            
            # Conditions
            if deployment.status.conditions:
                print(f"\nConditions:")
                for condition in deployment.status.conditions:
                    print(f"  {condition.type}: {condition.status}")
                    if condition.message:
                        print(f"    Message: {condition.message}")
            
            return deployment
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


if __name__ == "__main__":
    scaler = DeploymentScaler()
    
    # Scale deployment
    scaler.scale_deployment("nginx-test", replicas=5)
    
    # Get status
    time.sleep(2)
    scaler.get_deployment_status("nginx-test")
    
    # Create autoscaler (requires metrics-server)
    # scaler.autoscale_deployment("nginx-test", min_replicas=2, max_replicas=10)
```

---

## Part 4: ConfigMaps and Secrets

### Exercise 4.1: Manage ConfigMaps and Secrets

Create `config_secrets.py`:

```python
from kubernetes import client, config
import base64


class ConfigManager:
    """Manage ConfigMaps and Secrets."""
    
    def __init__(self):
        config.load_kube_config()
        self.core_v1 = client.CoreV1Api()
    
    def create_configmap(self, name, data, namespace="default"):
        """Create a ConfigMap."""
        try:
            print(f"📝 Creating ConfigMap '{name}'...")
            
            configmap = client.V1ConfigMap(
                api_version="v1",
                kind="ConfigMap",
                metadata=client.V1ObjectMeta(name=name),
                data=data
            )
            
            api_response = self.core_v1.create_namespaced_config_map(
                namespace=namespace,
                body=configmap
            )
            
            print(f"✅ ConfigMap created!")
            print(f"   Name: {name}")
            print(f"   Keys: {', '.join(data.keys())}")
            
            return api_response
            
        except client.exceptions.ApiException as e:
            if e.status == 409:
                print(f"⚠️  ConfigMap '{name}' already exists")
            else:
                print(f"❌ Error: {e}")
            return None
    
    def create_secret(self, name, data, secret_type="Opaque", namespace="default"):
        """Create a Secret."""
        try:
            print(f"🔐 Creating Secret '{name}'...")
            
            # Encode data to base64
            encoded_data = {}
            for key, value in data.items():
                encoded_data[key] = base64.b64encode(value.encode()).decode()
            
            secret = client.V1Secret(
                api_version="v1",
                kind="Secret",
                metadata=client.V1ObjectMeta(name=name),
                type=secret_type,
                data=encoded_data
            )
            
            api_response = self.core_v1.create_namespaced_secret(
                namespace=namespace,
                body=secret
            )
            
            print(f"✅ Secret created!")
            print(f"   Name: {name}")
            print(f"   Type: {secret_type}")
            print(f"   Keys: {', '.join(data.keys())}")
            
            return api_response
            
        except client.exceptions.ApiException as e:
            if e.status == 409:
                print(f"⚠️  Secret '{name}' already exists")
            else:
                print(f"❌ Error: {e}")
            return None
    
    def get_configmap(self, name, namespace="default"):
        """Get ConfigMap data."""
        try:
            configmap = self.core_v1.read_namespaced_config_map(name, namespace)
            
            print(f"\n📝 ConfigMap: {name}")
            print(f"{'='*60}\n")
            
            for key, value in configmap.data.items():
                print(f"{key}:")
                print(f"{value}\n")
            
            return configmap.data
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_secret(self, name, namespace="default", decode=True):
        """Get Secret data."""
        try:
            secret = self.core_v1.read_namespaced_secret(name, namespace)
            
            print(f"\n🔐 Secret: {name}")
            print(f"{'='*60}\n")
            
            data = {}
            for key, value in secret.data.items():
                if decode:
                    decoded_value = base64.b64decode(value).decode()
                    data[key] = decoded_value
                    print(f"{key}: {decoded_value}")
                else:
                    data[key] = value
                    print(f"{key}: [base64 encoded]")
            
            print()
            return data
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def update_configmap(self, name, data, namespace="default"):
        """Update ConfigMap data."""
        try:
            configmap = self.core_v1.read_namespaced_config_map(name, namespace)
            configmap.data = data
            
            api_response = self.core_v1.replace_namespaced_config_map(
                name=name,
                namespace=namespace,
                body=configmap
            )
            
            print(f"✅ ConfigMap '{name}' updated!")
            return api_response
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def delete_configmap(self, name, namespace="default"):
        """Delete a ConfigMap."""
        try:
            self.core_v1.delete_namespaced_config_map(name, namespace)
            print(f"✅ ConfigMap '{name}' deleted")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def delete_secret(self, name, namespace="default"):
        """Delete a Secret."""
        try:
            self.core_v1.delete_namespaced_secret(name, namespace)
            print(f"✅ Secret '{name}' deleted")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    manager = ConfigManager()
    
    # Create ConfigMap
    app_config = {
        'database_host': 'postgres.default.svc.cluster.local',
        'database_port': '5432',
        'log_level': 'INFO',
        'app_config.yaml': """
app:
  name: My Application
  version: 1.0.0
  debug: false
        """
    }
    
    manager.create_configmap("app-config", app_config)
    
    # Create Secret
    db_credentials = {
        'username': 'admin',
        'password': 'super-secret-password',
        'api_key': 'sk-1234567890abcdef'
    }
    
    manager.create_secret("db-credentials", db_credentials)
    
    # Get ConfigMap
    # manager.get_configmap("app-config")
    
    # Get Secret
    # manager.get_secret("db-credentials", decode=True)
```

---

## Part 5: Complete Application Deployment

### Exercise 5.1: Deploy Full Stack Application

Create `deploy_app.py`:

```python
from kubernetes import client, config
import time


class ApplicationDeployer:
    """Deploy complete application stack to Kubernetes."""
    
    def __init__(self, namespace="default"):
        config.load_kube_config()
        self.namespace = namespace
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
    
    def deploy_full_stack(self, app_name="myapp"):
        """Deploy complete application stack."""
        print(f"\n{'='*70}")
        print(f"Deploying Application Stack: {app_name}")
        print(f"{'='*70}\n")
        
        # 1. Create namespace (if not default)
        if self.namespace != "default":
            self._create_namespace()
        
        # 2. Create ConfigMap
        print("1️⃣  Creating ConfigMap...")
        self._create_app_configmap(app_name)
        
        # 3. Create Secret
        print("\n2️⃣  Creating Secret...")
        self._create_app_secret(app_name)
        
        # 4. Deploy Redis
        print("\n3️⃣  Deploying Redis...")
        self._deploy_redis(app_name)
        
        # 5. Deploy Application
        print("\n4️⃣  Deploying Application...")
        self._deploy_app(app_name)
        
        # 6. Create Service
        print("\n5️⃣  Creating Service...")
        self._create_app_service(app_name)
        
        print(f"\n{'='*70}")
        print(f"✅ Application Stack Deployed Successfully!")
        print(f"{'='*70}\n")
        
        # Show access instructions
        self._show_access_info(app_name)
    
    def _create_namespace(self):
        """Create namespace if it doesn't exist."""
        try:
            namespace = client.V1Namespace(
                metadata=client.V1ObjectMeta(name=self.namespace)
            )
            self.core_v1.create_namespace(namespace)
            print(f"✅ Namespace '{self.namespace}' created")
        except client.exceptions.ApiException as e:
            if e.status == 409:
                print(f"⚠️  Namespace '{self.namespace}' already exists")
    
    def _create_app_configmap(self, app_name):
        """Create application ConfigMap."""
        configmap = client.V1ConfigMap(
            metadata=client.V1ObjectMeta(name=f"{app_name}-config"),
            data={
                'REDIS_HOST': f'{app_name}-redis',
                'REDIS_PORT': '6379',
                'APP_ENV': 'production'
            }
        )
        
        try:
            self.core_v1.create_namespaced_config_map(
                self.namespace,
                configmap
            )
            print(f"✅ ConfigMap created")
        except client.exceptions.ApiException as e:
            if e.status == 409:
                print(f"⚠️  ConfigMap already exists")
    
    def _create_app_secret(self, app_name):
        """Create application Secret."""
        import base64
        
        secret = client.V1Secret(
            metadata=client.V1ObjectMeta(name=f"{app_name}-secret"),
            type="Opaque",
            data={
                'api_key': base64.b64encode(b'my-secret-api-key').decode()
            }
        )
        
        try:
            self.core_v1.create_namespaced_secret(
                self.namespace,
                secret
            )
            print(f"✅ Secret created")
        except client.exceptions.ApiException as e:
            if e.status == 409:
                print(f"⚠️  Secret already exists")
    
    def _deploy_redis(self, app_name):
        """Deploy Redis."""
        container = client.V1Container(
            name="redis",
            image="redis:7-alpine",
            ports=[client.V1ContainerPort(container_port=6379)]
        )
        
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": f"{app_name}-redis"}),
            spec=client.V1PodSpec(containers=[container])
        )
        
        spec = client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={"app": f"{app_name}-redis"}
            ),
            template=template
        )
        
        deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(name=f"{app_name}-redis"),
            spec=spec
        )
        
        try:
            self.apps_v1.create_namespaced_deployment(
                self.namespace,
                deployment
            )
            print(f"✅ Redis deployment created")
            
            # Create service
            service = client.V1Service(
                metadata=client.V1ObjectMeta(name=f"{app_name}-redis"),
                spec=client.V1ServiceSpec(
                    selector={"app": f"{app_name}-redis"},
                    ports=[client.V1ServicePort(port=6379, target_port=6379)]
                )
            )
            
            self.core_v1.create_namespaced_service(
                self.namespace,
                service
            )
            print(f"✅ Redis service created")
            
        except client.exceptions.ApiException as e:
            if e.status == 409:
                print(f"⚠️  Redis already deployed")
    
    def _deploy_app(self, app_name):
        """Deploy main application."""
        # Environment from ConfigMap and Secret
        env = [
            client.V1EnvVar(
                name="REDIS_HOST",
                value_from=client.V1EnvVarSource(
                    config_map_key_ref=client.V1ConfigMapKeySelector(
                        name=f"{app_name}-config",
                        key="REDIS_HOST"
                    )
                )
            ),
            client.V1EnvVar(
                name="API_KEY",
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name=f"{app_name}-secret",
                        key="api_key"
                    )
                )
            )
        ]
        
        container = client.V1Container(
            name="app",
            image="nginx:alpine",  # Replace with your app image
            ports=[client.V1ContainerPort(container_port=80)],
            env=env
        )
        
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": app_name}),
            spec=client.V1PodSpec(containers=[container])
        )
        
        spec = client.V1DeploymentSpec(
            replicas=3,
            selector=client.V1LabelSelector(match_labels={"app": app_name}),
            template=template
        )
        
        deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(name=app_name),
            spec=spec
        )
        
        try:
            self.apps_v1.create_namespaced_deployment(
                self.namespace,
                deployment
            )
            print(f"✅ Application deployment created")
        except client.exceptions.ApiException as e:
            if e.status == 409:
                print(f"⚠️  Application already deployed")
    
    def _create_app_service(self, app_name):
        """Create application service."""
        service = client.V1Service(
            metadata=client.V1ObjectMeta(name=app_name),
            spec=client.V1ServiceSpec(
                type="NodePort",
                selector={"app": app_name},
                ports=[
                    client.V1ServicePort(
                        port=80,
                        target_port=80,
                        node_port=30080
                    )
                ]
            )
        )
        
        try:
            self.core_v1.create_namespaced_service(
                self.namespace,
                service
            )
            print(f"✅ Service created")
        except client.exceptions.ApiException as e:
            if e.status == 409:
                print(f"⚠️  Service already exists")
    
    def _show_access_info(self, app_name):
        """Show how to access the application."""
        print(f"Access Information:")
        print(f"  Service: {app_name}")
        print(f"  NodePort: 30080")
        print(f"\n  Get node IP:")
        print(f"    kubectl get nodes -o wide")
        print(f"\n  Access application:")
        print(f"    http://<node-ip>:30080")
    
    def cleanup(self, app_name="myapp"):
        """Remove all deployed resources."""
        print(f"\n🗑️  Cleaning up {app_name}...")
        
        # Delete deployments
        try:
            self.apps_v1.delete_namespaced_deployment(
                app_name,
                self.namespace
            )
            print(f"✅ Deleted deployment: {app_name}")
        except:
            pass
        
        try:
            self.apps_v1.delete_namespaced_deployment(
                f"{app_name}-redis",
                self.namespace
            )
            print(f"✅ Deleted deployment: {app_name}-redis")
        except:
            pass
        
        # Delete services
        try:
            self.core_v1.delete_namespaced_service(app_name, self.namespace)
            print(f"✅ Deleted service: {app_name}")
        except:
            pass
        
        try:
            self.core_v1.delete_namespaced_service(
                f"{app_name}-redis",
                self.namespace
            )
            print(f"✅ Deleted service: {app_name}-redis")
        except:
            pass
        
        # Delete ConfigMap and Secret
        try:
            self.core_v1.delete_namespaced_config_map(
                f"{app_name}-config",
                self.namespace
            )
            print(f"✅ Deleted ConfigMap")
        except:
            pass
        
        try:
            self.core_v1.delete_namespaced_secret(
                f"{app_name}-secret",
                self.namespace
            )
            print(f"✅ Deleted Secret")
        except:
            pass
        
        print(f"\n✅ Cleanup complete!")


if __name__ == "__main__":
    deployer = ApplicationDeployer(namespace="default")
    
    # Deploy application
    deployer.deploy_full_stack("my-web-app")
    
    # Cleanup (uncomment to remove)
    # deployer.cleanup("my-web-app")
```

---

## Practice Challenges

### Challenge 1: Cluster Health Monitor
Build a monitoring tool that:
- Checks health of all pods
- Identifies unhealthy or failing pods
- Auto-restarts pods that are failing
- Sends alerts for critical issues

### Challenge 2: Rolling Update Manager
Create a tool that:
- Performs rolling updates safely
- Monitors deployment progress
- Implements automatic rollback on failure
- Validates deployment health

### Challenge 3: Resource Optimizer
Build a system that:
- Analyzes resource usage across cluster
- Identifies over/under-provisioned pods
- Recommends resource adjustments
- Implements auto-scaling based on usage

### Challenge 4: Backup and Restore Tool
Create a tool that:
- Backs up all Kubernetes resources
- Exports to YAML files
- Implements restore functionality
- Handles namespace migrations

---

## What You Learned

In this lab, you learned:

✅ **Kubernetes Python Client Basics**
- Setting up and authenticating with clusters
- Using different API clients (CoreV1Api, AppsV1Api)
- Handling Kubernetes exceptions
- Working with kubeconfig

✅ **Resource Management**
- Listing pods, deployments, services
- Getting detailed resource information
- Monitoring resource status
- Retrieving logs

✅ **Creating Resources**
- Programmatically creating deployments
- Defining pod specifications
- Creating services (ClusterIP, NodePort, LoadBalancer)
- Setting up health checks

✅ **Scaling and Updates**
- Scaling deployments
- Implementing horizontal pod autoscaling
- Monitoring deployment status
- Waiting for operations to complete

✅ **Configuration Management**
- Creating and managing ConfigMaps
- Working with Secrets
- Injecting configuration into pods
- Updating configuration

✅ **Application Deployment**
- Deploying multi-tier applications
- Managing dependencies
- Creating complete stacks
- Cleanup and resource management

## Next Steps

- Learn Helm for package management
- Explore Custom Resource Definitions (CRDs)
- Implement GitOps with ArgoCD or Flux
- Study Kubernetes Operators
- Build production-ready deployment pipelines

## Additional Resources

- [Kubernetes Python Client Documentation](https://github.com/kubernetes-client/python)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Patterns](https://www.redhat.com/en/resources/oreilly-kubernetes-patterns-guide)
