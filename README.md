# Script to Replace Slack with Teams

## Description

This Python script automates the process of replacing Slack integrations with Teams integrations in a given repository. It performs several tasks, such as creating a new git branch, copying a file, replacing certain text occurrences, and modifying configuration files. It's designed to be used with repositories that follow a specific structure.

## Prerequisites

- Python 3.7+

## Setup

1. Create a new Conda environment:

   ```
   conda create --name replace-slack python=3.7
   ```

2. Activate the Conda environment:

   ```
   conda activate replace-slack
   ```

3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Update the constants in the script (at the top of the script) with your specific values. The constants are: `TEMPLATE_FOLDER`, `SERVICE_NAME`, `TARGET_REPO_FOLDER`, `PRIMARY_BRANCH` `TICKET_NUMBER`, `PYTHON_VERSION`, `ENV_NAME`, `TEAMS_WEBHOOK_URL`, `DEV_CHANNEL`, and `PROD_CHANNEL`.

2. Run the script:

   ```
   python src/index.py
   ```

3. Check the target folder and change that were made. Double check them to make sure it's all good
4. Run the tests

# Warning

This will delete any comments in the config files. So make sure to add them back in when you've run the script
