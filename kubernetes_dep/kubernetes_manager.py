from kubernetes import client, config

# Load the kubeconfig file to connect to the cluster
config.load_kube_config()

def create_deployment(image_name, deployment_name, namespace='default'):
    """Create a deployment in the specified namespace."""
    try:
        # Define the container spec
        container = client.V1Container(name=deployment_name, image=image_name)
        
        # Define the pod template spec
        template = client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(labels={"app": deployment_name}),
                                            spec=client.V1PodSpec(containers=[container]))
        
        #Define the deployment spec
        spec = client.V1DeploymentSpec(replicas=1, template=template)
        
        #Create a deployment
        deployment = client.V1Deployment(api_version="apps/v1", kind="Deployment",
                                         metadata=client.V1ObjectMeta(name=deployment_name),
                                         spec=spec)
        
        api = client.AppsV1Api()
        api.create_namespaced_deployment(namespace=namespace, body=deployment)
        print(f"Deployment '{deployment_name}' created successfully in namespace '{namespace}'.")
    except Exception as e:
        print(f"Error creating deployment: {e}")
        
def scale_deployment(deployment_name, replicas, namespace='default'):
    """Scale a deployment to the specified number of replicas."""
    try:
     api = client.AppsV1Api()
     deployment = api.read_namespaced_deployment(deployment_name, namespace)
     deployment.spec.replicas = replicas
     api.patch_namespaced_deployment(deployment_name, namespace, deployment)   
    except Exception as e:
        print(f"Error scalling deployment: {e}")
        
        
        
def delete_deployment(deployment_name, namespace='default'):
    """Delete a deployment in the specified namespace."""
    try:
        api = client.AppsV1Api()
        api.delete_namespaced_deployment(deployment_name, namespace)
        print(f"Deployment  '{deployment_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting deployment: {e}")


def get_pod_logs(deployment_name, namespace='default'):
    """Get logs from the pods in the specified deployment."""
    try:
        api = client.CoreV1Api()
        pods = api.list_namespaced_pod(namespace, label_selector=f'app={deployment_name}')

        for pod in pods.items:
            logs = api.read_namespaced_pod_log(pod.metadata.name, namespace)
            print(f"Logs for pod '{pod.metadata.name}':\n{logs}")
    except Exception as e:
        print(f"Error retrieving logs: {e}")
        
        
if __name__ == "__main__":
    # Example usage:
    # create_deployment("my_image", "my_deployment")
    # scale_deployment("my_deployment", 3)
    # delete_deployment("my_deployment")
    # get_pod_logs("my_deployment")

    while True:
        action = input("Enter action (create, scale, delete, logs, exit): ").strip().lower()
        
        if action == "create":
            image_name = input("Enter Docker image name: ").strip()
            deployment_name = input("Enter deployment name: ").strip()
            create_deployment(image_name, deployment_name)
        
        elif action == "scale":
            deployment_name = input("Enter deployment name to scale: ").strip()
            replicas = int(input("Enter number of replicas: "))
            scale_deployment(deployment_name, replicas)
        
        elif action == "delete":
            deployment_name = input("Enter deployment name to delete: ").strip()
            delete_deployment(deployment_name)
        
        elif action == "logs":
            deployment_name = input("Enter deployment name to get logs: ").strip()
            get_pod_logs(deployment_name)
        
        elif action == "exit":
            print("Exiting Kubernetes manager.")
            break
        else:
            print("Unknown action. Please try again.")