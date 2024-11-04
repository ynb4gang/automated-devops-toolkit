import os
import boto3
from kubernetes import client, config
from base64 import b64decode

# Choose the configuration source: "aws" or "kubernetes"
CONFIG_SOURCE = os.getenv("CONFIG_SOURCE", "aws")

# AWS Secrets Manager client setup
if CONFIG_SOURCE == "aws":
    session = boto3.session.Session()
    secrets_client = session.client(service_name="secretsmanager", region_name="us-west-2")  # Replace with your region

# Kubernetes client setup for secrets
elif CONFIG_SOURCE == "kubernetes":
    config.load_kube_config()
    k8s_client = client.CoreV1Api()

def get_secret_aws(secret_name):
    """Retrieve a secret from AWS Secrets Manager."""
    try:
        secret_value = secrets_client.get_secret_value(SecretId=secret_name)
        secret_data = secret_value.get("SecretString")
        print(f"Retrieved secret '{secret_name}' from AWS.")
        return secret_data
    except Exception as e:
        print(f"Error retrieving AWS secret: {e}")
        return None

def get_secret_kubernetes(secret_name, namespace="default"):
    """Retrieve a Kubernetes secret."""
    try:
        secret = k8s_client.read_namespaced_secret(secret_name, namespace)
        secret_data = {key: b64decode(value).decode("utf-8") for key, value in secret.data.items()}
        print(f"Retrieved secret '{secret_name}' from Kubernetes.")
        return secret_data
    except client.exceptions.ApiException as e:
        print(f"Error retrieving Kubernetes secret: {e}")
        return None

def get_config(config_name):
    """Retrieve configuration based on the configured source."""
    if CONFIG_SOURCE == "aws":
        return get_secret_aws(config_name)
    elif CONFIG_SOURCE == "kubernetes":
        return get_secret_kubernetes(config_name)
    else:
        print("Invalid CONFIG_SOURCE specified.")
        return None

if __name__ == "__main__":
    # Example usage for retrieving secrets/configurations
    secret_name = ""  #your actual secret name
    config_data = get_config(secret_name)
    if config_data:
        print(f"Configuration data: {config_data}")
