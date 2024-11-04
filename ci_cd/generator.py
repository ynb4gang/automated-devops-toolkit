import os


OUTPUT_DIR = "ci_cd/generated_workflows"
os.makedirs(OUTPUT_DIR, exist_ok=True)

WORKFLOW_TEMPLATE = """
name: {workflow_name}

on:
  push:
    branches:
      - {branch}
  pull_request:
    branches:
      - {branch}

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '{python_version}'

      - name: Install dependencies
        run: {install_command}

      - name: Run build
        run: {build_command}

      - name: Run tests
        run: {test_command}
"""

def get_user_input():
    """Prompts the user for input to fill in the CI/CD workflow template."""
    workflow_name = input("Enter the workflow name (e.g., CI/CD Pipeline): ")
    branch = input("Enter the branch to trigger the workflow (e.g., main): ")
    python_version = input("Enter Python version (e.g., 3.8): ")
    install_command = input("Enter the command to install dependencies (e.g., pip install -r requirements.txt): ")
    build_command = input("Enter the build command (e.g., python setup.py build): ")
    test_command = input("Enter the test command (e.g., pytest): ")
    
    return {
        "workflow_name": workflow_name,
        "branch": branch,
        "python_version": python_version,
        "install_command": install_command,
        "build_command": build_command,
        "test_command": test_command
    }
    
def generate_workflow_file():
    """Generates a GitHub Actions workflow file based on user input."""
    user_input = get_user_input()
    filled_template = WORKFLOW_TEMPLATE.format(**user_input)
    
    # Define the output file path
    output_file_path = os.path.join(OUTPUT_DIR, f"{user_input['workflow_name'].replace(' ', '_')}.yml")
    
    # Write the filled template to a file
    with open(output_file_path, "w") as workflow_file:
        workflow_file.write(filled_template)
    
    print(f"Workflow file generated at: {output_file_path}")

if __name__ == "__main__":
    generate_workflow_file()