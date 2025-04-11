# ds_protocol.py
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

import json
from collections import namedtuple

# Pytest testing:
# 1. cd ICS\ 32\ -\ Assignment\ 4
# 2. pytest .

# coverage testing:
# 1. coverage run -m pytest .
# 2. coverage report -m (shows report with percent)
# 3. coverage run -m --branch pytest . (branch coverage)

Data = namedtuple('Data', ['type', 'message', 'token'])

def create_join_message(username: str, password: str):
    return json.dumps({"join":
        {"username": username, "password": password, "token": ""}})


def create_post_message(token: str, message: str, timestamp: str):
    return json.dumps({"token": token, "post":
        {"entry": message, "timestamp": timestamp}})


def create_bio_message(token: str, bio: str, timestamp: str):
    return json.dumps({"token": token, "bio":
        {"entry": bio, "timestamp": timestamp}})

# Part 1: Implement the Direct Messaging Protocol
def send_direct_message(token: str, message: str, username: str, timestamp: str):
    return json.dumps({"token": token, "directmessage":
        {"entry": message, "recipient": username, "timestamp": timestamp}})


def request_unread_messages(token: str, message: str):
    data = {"token": token, "directmessage": "new"}
    return json.dumps(data)


def request_all_messages(token: str, message: str):
    data = {"token": token, "directmessage": "all"}
    return json.dumps(data)


def extract_json(extracted_data: str):
    try:
        if not isinstance(extracted_data, str):
            print(f"Error: Expected JSON string, but received {type(extracted_data)}.")
            return Data("error", "Non-string data received", "")

        if not extracted_data:
            return Data("error", "Empty Data recieved", "")

        data = json.loads(extracted_data)  # Convert JSON string to dictionary
        respond = data.get("response", {})

        return Data(respond.get("type", "error"),
            respond.get("message", "No message provided"),
            respond.get("token", ""))  # error, No message provided, and "" is default values

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return Data("error", "Invalid JSON response", "")


def send_message(send_stream, recv_stream, message_json: str, action_type: str):
    try:
        send_stream.write(message_json + '\r\n')
        send_stream.flush()

        # Read the server's response
        response = recv_stream.readline().strip()

        if not response:
            print(f"Error: No response received from server: {action_type}.")
            return Data("error", "Empty response from server", "")

        return (extract_json(response))

    except TimeoutError:
        return Data("error", "TimeoutError in send_message", "")
