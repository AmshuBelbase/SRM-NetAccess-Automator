import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from read_lines import cred
import os 

# Get the parent directory of the Python file being executed
parent_folder = os.path.dirname(os.path.abspath(__file__))

filepath = f"{parent_folder}/files.txt"

# Global variable to store the initialized app
firebase_app = None


def initialize_firebase():
    global firebase_app, filepath
    creds = cred(filepath)
    if not firebase_app:
        c = credentials.Certificate(creds[0])
        # Give your app a unique name (e.g., 'my_firebase_app')
        firebase_app = firebase_admin.initialize_app(c, {
            'databaseURL': creds[1]
        })


def get_ip_from_firebase(custom_key):
    try:
        ref = db.reference('ip_addresses', app=firebase_app)
        ip_data = ref.child(custom_key).get()

        if ip_data is not None:
            ip_address = ip_data.get('ip_address', None)
            return ip_address
        else:
            return "No IP address found for the given key."
    except Exception as e:
        return f"Error retrieving IP address: {e}"


def close_firebase_connection():
    global firebase_app
    if firebase_app:
        firebase_admin.delete_app(firebase_app)
        print("Firebase app connection closed.")


def get_remote_ip():
    global filepath
    try:
        creds = cred(filepath)
        initialize_firebase()
        custom_key = creds[3]
        ip_address = get_ip_from_firebase(custom_key)
        print(f"IP Address for '{custom_key}': {ip_address}")
        close_firebase_connection()
        return ip_address
    except Exception as e:
        return f"Error while retrieving IP address from FB: {e}"


if __name__ == "__main__":
    print(get_remote_ip())
