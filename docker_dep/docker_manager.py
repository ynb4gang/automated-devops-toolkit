import docker
import os
import sys
import time

# Initialize the Docker client
client = docker.from_env()

def build_image(dockerfile_path, image_name):
    """Build a Docker image from a specified Dockerfile."""
    try:
        print(f"Building Docker Image '{image_name}' from {dockerfile_path}...")
        image, build_logs = client.images.build(path=dockerfile_path, tag=image_name)
        print(f"Image '{image_name}' built successfully.")
    except docker.errors.BuildError as build_err:
        print(f"Error building image: {build_err}")
    except docker.errors.APIError as api_err:
        print(f"Docker API error: {api_err}")


        
def run_container(image_name, container_name, ports=None):
    """Run a Docker container from an image with optional port mapping."""
    try:
        print(f"Starting container from an image with optional port mapping")
        container = client.containers.run(image_name, name=container_name, ports=ports, detach=True)
        print(f"Container '{container_name}' is now running.")
        return container
    except docker.errors.ContainerError as err:
        print(f"Container error: {err}")
    except docker.errors.ImageNotFound as image_arr:
        print(f"Image '{image_name}' not found. Pleade build the image first.")
    except docker.errors.APIError as api_err:
        print(f"Docker API error: {api_err}")


def stop_container(container_name):
    """Stop a running Docker container by name."""
    try:
        container = client.containers.get(container_name)
        container.stop()
        print(f"Container '{container_name}' has been stopped. ")
    except docker.errors.NotFound as err:
        print(f"Container '{container_name}' not found.")
    except docker.errors.APIError as api_err:
        print(f"Docker API error: {api_err}")


        
def remove_container(container_name):
    """Remove a stopped Docker container by name."""
    try:
        container = client.containers.get(container_name)
        container.remove
        print(f"Container '{container_name}' has been removed.")
    except docker.errors.NotFound as err:
        print(f"Container '{container_name}' not found.")
    except docker.errors.APIError as api_err:
        print(f"Docker API error: {api_err}")
        


def get_logs(container_name):
    """Retrieve logs from a running or stopped container."""
    try:
        container = client.containers.get(container_name)
        logs = container.logs()
        print(f"Logs for container '{container_name}':\n{logs.decode('utf-8')}")
    except docker.errors.NotFound:
        print(f"Container '{container_name}' not found.")
    except docker.errors.APIError as api_err:
        print(f"Docker API error: {api_err}")
        

if __name__ == "__main__":
    # Example usage (for testing):
    # Build an image: build_image(".", "my_image")
    # Run a container: run_container("my_image", "my_container", ports={"8080/tcp": 8080})
    # Stop a container: stop_container("my_container")
    # Remove a container: remove_container("my_container")
    # Get logs: get_logs("my_container")

    # Sample interaction loop (for demonstration purposes)
    while True:
        action = input("Enter action (build, run, stop, remove, logs, exit): ").strip().lower()
        
        if action == "build":
            dockerfile_path = input("Enter path to Dockerfile directory: ").strip()
            image_name = input("Enter image name: ").strip()
            build_image(dockerfile_path, image_name)
        
        elif action == "run":
            image_name = input("Enter image name to run: ").strip()
            container_name = input("Enter container name: ").strip()
            ports = input("Enter ports (e.g., 8080:80) or leave blank: ").strip()
            port_mapping = None
            if ports:
                host_port, container_port = ports.split(":")
                port_mapping = {f"{container_port}/tcp": int(host_port)}
            run_container(image_name, container_name, port_mapping)
        
        elif action == "stop":
            container_name = input("Enter container name to stop: ").strip()
            stop_container(container_name)
        
        elif action == "remove":
            container_name = input("Enter container name to remove: ").strip()
            remove_container(container_name)
        
        elif action == "logs":
            container_name = input("Enter container name to get logs: ").strip()
            get_logs(container_name)
        
        elif action == "exit":
            print("Exiting container manager.")
            break
        else:
            print("Unknown action. Please try again.")