import argparse
from ci_cd.generator import generate_pipeline
from cloud.cloud_manager import manage_cloud_resources
from docker_dep.docker_manager import manage_docker
from kubernetes_dep.kubernetes_manager import deploy_kubernetes
from monitoring.monitor import start_monitoring
from notification.alert_manager import send_alerts
from scaling.resource_manager import manage_resources
from config.config_manager import get_config
 
def main():
    parser = argparse.ArgumentParser(description="Automated DevOps Toolkit")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # CI/CD Generator
    ci_cd_parser = subparsers.add_parser('ci_cd', help='Generate CI/CD configuration')
    ci_cd_parser.add_argument('--template', type=str, help='Path to the CI/CD template file')

    # Cloud Manager
    cloud_parser = subparsers.add_parser('cloud', help='Manage cloud resources')
    cloud_parser.add_argument('--action', type=str, choices=['create', 'delete'], help='Action to perform on cloud resources')

    # Docker Manager
    docker_parser = subparsers.add_parser('docker', help='Manage Docker images and containers')
    docker_parser.add_argument('--action', type=str, choices=['build', 'push'], help='Action to perform on Docker images')

    # Kubernetes Manager
    kubernetes_parser = subparsers.add_parser('k8s', help='Deploy applications to Kubernetes')
    kubernetes_parser.add_argument('--deploy', type=str, help='Path to the Kubernetes manifest')

    # Monitoring
    monitoring_parser = subparsers.add_parser('monitor', help='Start monitoring services')

    # Notification
    notification_parser = subparsers.add_parser('notify', help='Send alerts')
    notification_parser.add_argument('--message', type=str, help='Alert message to send')

    # Resource Management
    resource_parser = subparsers.add_parser('resources', help='Manage resources and auto-scaling')

    # Configuration Management
    config_parser = subparsers.add_parser('config', help='Retrieve configurations and secrets')
    config_parser.add_argument('--name', type=str, help='Name of the configuration or secret to retrieve')

    args = parser.parse_args()

    if args.command == 'ci_cd':
        generate_pipeline(args.template)
    elif args.command == 'cloud':
        manage_cloud_resources(args.action)
    elif args.command == 'docker':
        manage_docker(args.action)
    elif args.command == 'k8s':
        deploy_kubernetes(args.deploy)
    elif args.command == 'monitor':
        start_monitoring()
    elif args.command == 'notify':
        send_alerts(args.message)
    elif args.command == 'resources':
        manage_resources()
    elif args.command == 'config':
        config_data = get_config(args.name)
        print(f"Retrieved configuration: {config_data}")

if __name__ == "__main__":
    main()
