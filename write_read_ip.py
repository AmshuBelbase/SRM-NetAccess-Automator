from datetime import datetime
from read_lines import cred

import os 

# Get the parent directory of the Python file being executed
parent_folder = os.path.dirname(os.path.abspath(__file__))

filepath = f"{parent_folder}/files.txt"



def write_text_to_file(filename, text):
    try:
        with open(filename, 'w') as file:
            file.write(text)
            print("Text written to file successfully.")
    except Exception as e:
        print(f"Error writing to file: {e}")


def read_text_from_file(filename):
    try:
        with open(filename, 'r') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error reading from file: {e}"


if __name__ == "__main__":
    # Get the current date and time
    current_time = datetime.now()

    # Print the date and time
    print("Current Date and Time:", current_time)
    creds = cred(filepath)
 
    text_to_write = "Hello, this is a line of text!"

    # Write text to the file
    write_text_to_file(creds[2], text_to_write)

    # Retrieve and print the text from the file
    retrieved_text = read_text_from_file(creds[2])
    print("Retrieved text:", retrieved_text)
