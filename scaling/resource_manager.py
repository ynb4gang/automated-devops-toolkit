from kubernetes import client, config
from prometheus_client import Gauge, start_http_server
import requests
import time

# Initialize Kubernetes client
config.load_kube_config()
k8s_apps_v1 = client.AppsV1Api()

# Define scaling parameters
NAMESPACE = ""  #your Kubernetes namespace
MIN_REPLICAS = 1
MAX_REPLICAS = 10
CPU_THRESHOLD = 0.75  # Scale up if CPU usage exceeds 75%
MEMORY_THRESHOLD = 0.75  # Scale up if memory usage exceeds 75%

# Prometheus Gauges for monitoring
cpu_usage_gauge = Gauge("cpu_usage", "Current CPU usage of deployment", ["deployment_name"])
memory_usage_gauge = Gauge("memory_usage", "Current memory usage of deployment", ["deployment_name"])

def get_prometheus_metric(metric_name, deployment_name):
    """Query Prometheus for a specific metric related to a deployment."""
    query = f'{metric_name}{{deployment="{deployment_name}"}}'
    url = f"http://localhost:9090/api/v1/query"  # Replace with actual Prometheus server URL
    response = requests.get(url, params={"query": query})
    
    if response.status_code == 200:
        results = response.json().get("data", {}).get("result", [])
        if results:
            return float(results[0]["value"][1])
    return 0.0

def scale_deployment(deployment_name, replicas):
    """Scale a Kubernetes deployment to the specified number of replicas."""
    current_deployment = k8s_apps_v1.read_namespaced_deployment(deployment_name, NAMESPACE)
    current_deployment.spec.replicas = replicas
    k8s_apps_v1.patch_namespaced_deployment(deployment_name, NAMESPACE, current_deployment)
    print(f"Scaled deployment '{deployment_name}' to {replicas} replicas.")

def check_and_scale_deployment(deployment_name):
    """Monitor resource usage and auto-scale deployment if thresholds are exceeded."""
    # Get current CPU and memory usage from Prometheus
    cpu_usage = get_prometheus_metric("cpu_usage", deployment_name)
    memory_usage = get_prometheus_metric("memory_usage", deployment_name)
    
    # Update Prometheus Gauges
    cpu_usage_gauge.labels(deployment_name=deployment_name).set(cpu_usage)
    memory_usage_gauge.labels(deployment_name=deployment_name).set(memory_usage)
    
    # Fetch the current replica count
    deployment = k8s_apps_v1.read_namespaced_deployment(deployment_name, NAMESPACE)
    current_replicas = deployment.spec.replicas
    
    # Scale up if either CPU or memory usage exceeds threshold and replicas are below MAX_REPLICAS
    if (cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD) and current_replicas < MAX_REPLICAS:
        new_replicas = min(current_replicas + 1, MAX_REPLICAS)
        scale_deployment(deployment_name, new_replicas)
    
    # Scale down if CPU and memory usage are below thresholds and replicas are above MIN_REPLICAS
    elif cpu_usage < CPU_THRESHOLD and memory_usage < MEMORY_THRESHOLD and current_replicas > MIN_REPLICAS:
        new_replicas = max(current_replicas - 1, MIN_REPLICAS)
        scale_deployment(deployment_name, new_replicas)

def start_scaling_monitor(deployment_name):
    """Start the auto-scaling monitor for a deployment."""
    start_http_server(8001)  # Start a Prometheus server for tracking metrics
    print("Scaling monitor server started on port 8001")
    
    while True:
        check_and_scale_deployment(deployment_name)
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    deployment_name = ""  #your Kubernetes deployment name
    start_scaling_monitor(deployment_name)
