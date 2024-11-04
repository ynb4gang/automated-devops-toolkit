import smtplib
from email.mime.text import MIMEText
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Configuration for Slack
SLACK_TOKEN = ""  # your Slack token
slack_client = WebClient(token=SLACK_TOKEN)

# Configuration for Email
SMTP_SERVER = ""  # your SMTP server
SMTP_PORT = 0  # your SMTP port
EMAIL_USERNAME = "" # your email username
EMAIL_PASSWORD = "" # your email password

def send_slack_alert(message, channel="#alerts"):
    """Send a notification to a Slack channel."""
    try:
        response = slack_client.chat_postMessage(channel=channel, text=message)
        print(f"Slack alert sent to {channel}: {message}")
    except SlackApiError as e:
        print(f"Error sending Slack message: {e.response['error']}")

def send_email_alert(subject, body, to_email):
    """Send an email notification."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USERNAME
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, to_email, msg.as_string())
        print(f"Email alert sent to {to_email}: {subject}")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_deployment_health(health_status, deployment_name, alert_threshold=0):
    """Check the health of a deployment and send an alert if below the threshold."""
    if health_status <= alert_threshold:
        message = f"ALERT: Deployment '{deployment_name}' is unhealthy!"
        send_slack_alert(message)
        send_email_alert(subject="Deployment Health Alert", body=message, to_email="admin@example.com")
        print(message)

if __name__ == "__main__":
    # Example alerts based on sample data
    deployment_name = "example_deployment"
    health_status = 0  # Unhealthy status (0 means unhealthy, 1 means healthy)

    check_deployment_health(health_status, deployment_name)
