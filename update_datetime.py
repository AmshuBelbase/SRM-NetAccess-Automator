import requests
import subprocess
import datetime

def get_current_time(timezone="Asia/Kolkata"):
    try:
        # Using the timeapi.io API to get the current time for a specified timezone
        url = f"https://timeapi.io/api/Time/current/zone?timeZone={timezone}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response.json()
        current_time = data['dateTime']  # The current time in the specified timezone

        return current_time
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the API."
    except requests.exceptions.Timeout:
        return "Error: The request timed out."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def set_system_datetime(new_datetime):
    try:
        # Update the system date and time
        subprocess.call(["sudo", "date", new_datetime])
        print(f"System date and time updated to: {new_datetime}")
    except Exception as e:
        print(f"Error updating system date and time: {e}")

def update_time():
    # Get the current internet time for the specified timezone
    internet_time = get_current_time("Asia/Kolkata")  # Change the timezone as needed
    print("Current Internet Time:", internet_time)

    # Convert the received time to MMDDhhmmCCYY format
    if "Error" not in internet_time:
        # Parse the received time
        dt = datetime.datetime.fromisoformat(internet_time[:-1])  # Remove the 'Z' at the end for parsing

        # Format it to MMDDhhmmCCYY
        new_datetime = dt.strftime("%m%d%H%M%Y")  # MMDDhhmmYYYY format
        set_system_datetime(new_datetime)
    else:
        print(internet_time)  # Print the error message if any

if __name__ == "__main__":
    update_time()
