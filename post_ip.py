import socket
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from datetime import datetime

# private imports
from get_current_ssid import get_wifi_ssid
from write_read_ip import read_text_from_file
from write_read_ip import write_text_to_file
from read_lines import cred

import os 

# Get the parent directory of the Python file being executed
parent_folder = os.path.dirname(os.path.abspath(__file__))

filepath = f"{parent_folder}/files.txt"

# Global variable to store the initialized app
firebase_app = None


def initialize_firebase():
    global firebase_app
    creds = cred(filepath)
    if not firebase_app:
        c = credentials.Certificate(creds[0])
        # Give your app a unique name (e.g., 'my_firebase_app')
        firebase_app = firebase_admin.initialize_app(c, {
            'databaseURL': creds[1]
        })


def get_local_ip():
    try:
        # Connect to a public DNS server to get the IP used for outbound traffic
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Error: {e}"


def post_ip_to_firebase(ip, custom_key):
    try:
        ref = db.reference('ip_addresses', app=firebase_app)
        ref.child(custom_key).set({'ip_address': ip})
        print(
            f"Posted IP address {ip} with key '{custom_key}' to Firebase successfully!")
        # Get the current date and time
        now = datetime.now()
        # Convert datetime to string in a readable format
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        print(now)
        ref.child(custom_key).update({'last_updated': now})
    except Exception as e:
        print(f"Error posting IP address to Firebase: {e}")


def close_firebase_connection():
    global firebase_app
    if firebase_app:
        firebase_admin.delete_app(firebase_app)
        print("Firebase app connection closed.")


def post_ip():
    global filepath
    try:
        local_ip = get_local_ip()  # Get the local IP address

        # get ssid
        ssid = get_wifi_ssid()
        print(f"Current SSID: {ssid}")

        ssid_local_ip = ssid+" "+local_ip
        creds = cred(filepath)
        retrieved_text = read_text_from_file(creds[2])

        if ssid_local_ip == retrieved_text:
            print("Same as Previous IP address, No need to Post")
        else:
            initialize_firebase()  # Initialize Firebase 

            # Define a custom key for the device
            custom_key = creds[3]


            

            post_ip_to_firebase(ssid_local_ip, custom_key)
            write_text_to_file(creds[2], ssid_local_ip)

            close_firebase_connection()

        return ssid_local_ip
    except Exception as e:
        return f"Error while getting and posting IP address to FB: {e}"


if __name__ == "__main__":
    print(post_ip())
