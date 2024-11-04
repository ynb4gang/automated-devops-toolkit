from prometheus_client import start_http_server, Gauge
import time
import requests
from notification.alert_manager import check_deployment_health

# Define Prometheus metrics
deployment_health_gauge = Gauge("deployment_health", "Health status of deployments", ["deployment_name"])

def monitor_health(url, deployment_name):
    """Basic health check for a deployment."""
    try:
        response = requests.get(url, timeout=5)
        health_status = 1 if response.status_code == 200 else 0
        deployment_health_gauge.labels(deployment_name=deployment_name).set(health_status)
        
        # Trigger alert if health status is unhealthy
        check_deployment_health(health_status, deployment_name)
        
        print(f"Deployment '{deployment_name}' is healthy." if health_status else f"Deployment '{deployment_name}' is unhealthy.")
    except requests.RequestException:
        deployment_health_gauge.labels(deployment_name=deployment_name).set(0)
        check_deployment_health(0, deployment_name)
        print(f"Deployment '{deployment_name}' failed health check.")

def start_monitoring_server():
    """Start Prometheus HTTP server for metrics collection."""
    start_http_server(8000)
    print("Prometheus monitoring server started on port 8000")

if __name__ == "__main__":
    # Start Prometheus server
    start_monitoring_server()

    # Sample URLs for health monitoring
    deployment_urls = {
        "example_service": "http://example.com/health",
        "another_service": "http://another-service.com/health",
    }

    # Basic loop to monitor each deployment periodically
    while True:
        for deployment_name, url in deployment_urls.items():
            monitor_health(url, deployment_name)
        time.sleep(60)  # Run every 60 seconds
