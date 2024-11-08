import subprocess


def get_wifi_ssid():
    try:
        # Execute the ipconfig command to get ipv4
        result = subprocess.check_output(
            ["ipconfig"], encoding='utf-8')

        # Look for the line containing "SSID"
        for line in result.split('\n'):
            if "IPv4 Address" in line:
                ssid = line.split(":")[1].strip()
                return ssid
        return "IPv4 Address not found"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    ssid = get_wifi_ssid()
    print(f"Connected to: {ssid}")
