# ds_protocol.py
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

"""
DS Protocol module for handling message creation, transmission, and parsing.
"""

import json
from collections import namedtuple

# coverage testing:
# 1. coverage report -m (shows report with percent)
# 2. coverage run -m --branch pytest . (branch coverage)
Data = namedtuple('Data', ['token', 'type', 'message', 'messages'])


# Part 1: Implement the Direct Messaging Protocol
def create_join_message(username: str, password: str):
    """
    Creates a JSON-formatted join message.
    """
    return json.dumps({
        "join": {
            "username": username,
            "password": password,
            "token": ""
        }
    })


def send_direct_msg(token: str, message: str, recipient: str, timestamp: str):
    """
    Creates a JSON-formatted direct message.
    """
    return json.dumps({
        "token": token,
        "directmessage": {
            "recipient": recipient,
            "entry": message,
            "timestamp": timestamp
        }
    })


def request_unread_messages(token: str, _: str):
    """
    Creates a JSON request for unread messages.
    """
    return json.dumps({
        "token": token,
        "directmessage": "new"
    })


def request_all_messages(token: str, _: str):
    """
    Creates a JSON request for all messages.
    """
    return json.dumps({
        "token": token,
        "directmessage": "all"
    })


def extract_json(extracted_data: str):
    """
    Extracts data from a JSON string and returns a named tuple.
    """
    try:
        if not isinstance(extracted_data, str):
            print(f"Error: Not recieved JSON string: {type(extracted_data)}.")
            return Data("error", "", "", [])

        if not extracted_data:
            return Data("error", "", "", [])

        data = json.loads(extracted_data)  # Convert JSON string to dictionary
        respond = data.get("response", {})

        return Data(
            respond.get("token", ""),
            respond.get("type", ""),
            respond.get("message", ""),
            respond.get("messages", [])
            )

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return Data("error", "", "", [])


def send_message(send_stream, recv_stream, message_json: str):
    """
    Sends a JSON message to the server and waits for a response.
    """
    try:
        send_stream.write(message_json + '\r\n')
        send_stream.flush()
        response = recv_stream.readline().strip()

        if not response:
            print("Error: No response received from server")

        return extract_json(response)

    except TimeoutError as e:
        print(f'TimeoutError occured: {e}')
        return Data("error", "", "Timeout while sending message", [])
