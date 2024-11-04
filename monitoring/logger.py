import logging
import os

# Set up a basic logging configuration
LOG_DIRECTORY = "logs"
os.makedirs(LOG_DIRECTORY, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    """Set up a logger with the specified name, log file, and level."""
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler(os.path.join(LOG_DIRECTORY, log_file))
    file_handler.setFormatter(formatter)
    
    logger.setLevel(level)
    logger.addHandler(file_handler)
    
    return logger

# Example loggers for container and cloud operations
container_logger = setup_logger("container_logger", "container.log")
cloud_logger = setup_logger("cloud_logger", "cloud.log")

# Example usage
def log_container_event(event_message):
    container_logger.info(event_message)
    print(f"Logged container event: {event_message}")

def log_cloud_event(event_message):
    cloud_logger.info(event_message)
    print(f"Logged cloud event: {event_message}")

# Testing the logger
if __name__ == "__main__":
    log_container_event("Container started successfully.")
    log_cloud_event("Cloud deployment created.")
