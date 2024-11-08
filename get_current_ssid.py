import subprocess


def get_wifi_ssid():
    try:
        # Execute the iwgetid command to get the Wi-Fi SSID
        result = subprocess.check_output(["/usr/sbin/iwgetid", "-r"], encoding='utf-8').strip()
        if result:
            return result
        return "SSID not found"
    except subprocess.CalledProcessError:
        return "Error: Unable to get SSID"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    ssid = get_wifi_ssid()
    print(f"Connected to: {ssid}")