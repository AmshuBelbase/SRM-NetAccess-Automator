import os
import subprocess
from read_lines import cred

# Get the parent directory of the Python file being executed
parent_folder = os.path.dirname(os.path.abspath(__file__))

credpath = f"{parent_folder}/cred.txt"

# Get Credentials
creds = cred(credpath)  
      

env_name = creds[2]
device_name = creds[3]

print("Parent folder of the file being executed:", parent_folder)

# Define the crontab entries with parent_folder variable
entries = f"""
@reboot sleep 10 && {parent_folder}/{env_name}/bin/python3 {parent_folder}/automate_click.py > {parent_folder}/Reboot_Wifi_Log.log 2>&1
*/30 * * * * {parent_folder}/{env_name}/bin/python3 {parent_folder}/automate_click.py > {parent_folder}/Cron_Wifi_Log.log 2>&1
@reboot rm {parent_folder}/my_last_ip.txt
@reboot sudo bash {parent_folder}/wifi-to-eth-route.sh > {parent_folder}/wifitoethroute.log
"""

# Define the content to write
content = f"""{parent_folder}/narcs-1805c-firebase-adminsdk-c4xll-18fd0504a9.json
https://narcs-1805c.firebaseio.com/
{parent_folder}/my_last_ip.txt
{device_name}
"""

# Specify the file path
file_path = "files.txt"

# Write the content to the file
with open(file_path, "w") as file:
    file.write(content)

print(f"Content written to {file_path}")


def add_crontab_entries(entries):
    # Fetch current crontab
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    current_crontab = result.stdout
    
    # Check if entries are already in crontab
    if entries.strip() not in current_crontab:
        # Append entries to current crontab
        new_crontab = current_crontab + entries
        # Set the new crontab
        process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        process.communicate(new_crontab)
        print("Crontab entries added.")
    else:
        print("Entries already exist in crontab.")

# Run the function
add_crontab_entries(entries)