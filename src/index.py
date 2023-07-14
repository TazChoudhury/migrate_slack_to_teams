import os
import shutil
from git import Repo
import configparser
import glob

# Local path to the Lambda-Template repo
TEMPLATE_FOLDER = "local/path/to/Lambda-Template"

# Local path to the target repo e.g GEOIntelligenceSuperResolution-Sagemaker
SERVICE_NAME = "service-name"
TARGET_REPO_FOLDER = "local/path/to/service-name"
PRIMARY_BRANCH = "main"

TICKET_NUMBER = "ticket-number"

# Teams channel names
DEV_CHANNEL = "dev_channel_name"
PROD_CHANNEL = "prod_channel_name"


print("Starting script")
# Switch to branch main, stash any change, pull, and create a new branch
repo: Repo = Repo(TARGET_REPO_FOLDER)

# make sure it's a git repository
assert not repo.bare

NEW_BRANCH = f"({TICKET_NUMBER})--replace-slack-with-teams"

print(f"Ensuring branch {PRIMARY_BRANCH} is up to date")
repo.git.checkout(PRIMARY_BRANCH)
repo.git.stash()
repo.git.pull()

print(f"Creating branch {NEW_BRANCH}")
# Check if branch exists
if NEW_BRANCH not in repo.heads:
    # Branch doesn't exist, create it
    repo.git.checkout('-b', NEW_BRANCH)
else:
    # Branch exists, just checkout
    repo.git.checkout(NEW_BRANCH)

print(f"Copying teams files from {TEMPLATE_FOLDER} to {TARGET_REPO_FOLDER}")
# # 2. Copy 'utils/teams.py' into the utils folder in the second folder.
shutil.copy(
    os.path.join(TEMPLATE_FOLDER, 'src', 'utils', 'teams.py'),
    os.path.join(TARGET_REPO_FOLDER, 'src', 'utils')
)

teams_file_path = os.path.join(TARGET_REPO_FOLDER, 'src', 'utils', 'teams.py')

# Replace 'Template-Lambda' with the service name
print(f"Replacing 'Template-Lambda' with '{SERVICE_NAME}' in {teams_file_path}")
with open(teams_file_path, 'r+') as file:
    content = file.read()
    content = content.replace('SERVICE = "Template-Lambda"', f'SERVICE = "{SERVICE_NAME}"')
    file.seek(0)
    file.write(content)
    file.truncate()

print(f"Deleting TODO in {teams_file_path}")
with open(teams_file_path, 'r') as file:
    content = file.readlines()

delete_lines = [
    "# TODO: you need to do two things to set up Teams messaging:\n",
    "# 1. Update the SERVICE constant below to the lambda name\n",
    "# 2. Change the channel name in the TEAM_NOTIFICATIONS_CHANNEL constant\n",
    "# to the channel you want to message\n"
]

with open(teams_file_path, 'w') as file:
    for line in content:
        if line not in delete_lines:
            file.write(line)

# Replace 'utils.slack' with 'utils.teams'
# Replace 'log_error_to_slack' with 'log_error_to_teams'
# Replace 'log_to_slack' with 'log_to_teams'
print(f"Replacing 'utils.slack' with 'utils.teams' in {TARGET_REPO_FOLDER}")
print(f"Replacing 'log_error_to_slack' with 'log_error_to_teams' in {TARGET_REPO_FOLDER}")
print(f"Replacing 'log_to_slack' with 'log_to_teams' in {TARGET_REPO_FOLDER}")
for dirpath, dirnames, filenames in os.walk(TARGET_REPO_FOLDER):
    for filename in filenames:
        if filename.endswith('.py'):
            with open(os.path.join(dirpath, filename), 'r+') as file:
                content = file.read()
                content = content.replace('utils.slack', 'utils.teams') \
                                 .replace('log_error_to_slack', 'log_error_to_teams') \
                                 .replace('log_to_slack', 'log_to_teams')
                file.seek(0)
                file.write(content)
                file.truncate()


class CaseConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr


print(f"Updating config files in {TARGET_REPO_FOLDER}")
for config_file in glob.glob(os.path.join(TARGET_REPO_FOLDER, 'config', '*.ini')):
    config = CaseConfigParser()
    config.read(config_file)
    if 'SLACK' in config:
        config.remove_section('SLACK')
    if 'TEAMS' not in config:
        config.add_section('TEAMS')
    if os.path.basename(config_file) in ['config_dev.ini']:
        config.set('TEAMS', 'TEAMS_NOTIFICATIONS_CHANNEL', DEV_CHANNEL)
        config.set('TEAMS', 'TEAMS_NOTIFICATIONS_ENABLED', 'True')
    if os.path.basename(config_file) in ['config_vpn.ini']:
        config.set('TEAMS', 'TEAMS_NOTIFICATIONS_CHANNEL', DEV_CHANNEL)
        config.set('TEAMS', 'TEAMS_NOTIFICATIONS_ENABLED', 'False')
    elif os.path.basename(config_file) == 'config_prod.ini':
        config.set('TEAMS', 'TEAMS_NOTIFICATIONS_CHANNEL', PROD_CHANNEL)
        config.set('TEAMS', 'TEAMS_NOTIFICATIONS_ENABLED', 'True')
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Delete 'utils/slack.py'
print(f"Deleting 'utils/slack.py' in {TARGET_REPO_FOLDER}")
slack_file_path = os.path.join(TARGET_REPO_FOLDER, 'src', 'utils', 'slack.py')
if os.path.exists(slack_file_path):
    os.remove(slack_file_path)
    print("'slack.py' has been deleted")
else:
    print("'slack.py' does not exist")


# Search for the string 'slack' and list the file and line number

print("Searching for 'slack' in the codebase")
found = False
for dirpath, dirnames, filenames in os.walk(TARGET_REPO_FOLDER):
    for filename in filenames:
        if filename.endswith('.py'):
            try:
                with open(os.path.join(dirpath, filename), 'r') as file:
                    for line_no, line in enumerate(file, start=1):
                        if 'slack' in line:
                            found = True
                            print(f"'slack' found in file {filename} on line {line_no}")
            except UnicodeDecodeError:
                print(f"Cannot decode file {filename}. Skipping.")

if not found:
    print("'slack' not found in the codebase")

print("Finished script")
