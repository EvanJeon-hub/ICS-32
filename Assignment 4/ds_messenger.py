# ds_messenger.py
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

"""
Direct Messenger module for handling direct messages using a socket connection.
"""

import time
import socket
from pathlib import Path
from Profile import DirectMessage, Profile
from ds_protocol import (
    send_direct_msg, request_unread_messages,
    send_message, create_join_message
)
# coverage testing:
# 1. coverage report -m (shows report with percent)
# 2. coverage run -m --branch pytest . (branch coverage)


class DirectMessenger:
    """
    A class to manage direct messaging functionality.
    """
    def __init__(self, dsuserver=None, username=None,
                 password=None, profile_path=None):
        """
        Initializes a DirectMessenger instance.
        """
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.profile_path = f"{username}_data.dsu"
        if not Path(self.profile_path).exists():
            Path((self.profile_path)).touch()
        self.profile = Profile(dsuserver, username, password, profile_path)
        self.profile.load_profile(self.profile_path)
        self.profile.save_profile()
        self.socket = None
        self.token = None
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.dsuserver, 3001))
            self.send_stream = self.socket.makefile('w')
            self.recv_stream = self.socket.makefile('r')
            self.join_server()
        except ConnectionRefusedError:
            print("Connection Refused. Running in offline mode.")
            self.socket = None

    def join_server(self) -> bool:
        """
        Attempts to join the server.
        """
        try:
            jm = create_join_message(self.username, self.password)
            response = send_message(self.send_stream, self.recv_stream, jm)
            if response and response.type != "error":
                self.token = response.token
                return True
        except TimeoutError:
            print("TimeoutError while joining the server")
        return False

    def send(self, message: str, recipient: str) -> bool:
        """
        Sends a direct message to a recipient.
        """
        try:
            if not self.token:
                return False
            timestamp = str(time.time())
            d_msg = send_direct_msg(self.token, message, recipient, timestamp)
            response = send_message(self.send_stream, self.recv_stream, d_msg)
            # Part 3: Store Messages Locally
            if response and response.type != "error":
                new_msg = DirectMessage(recipient=recipient,
                                        sender=self.username,
                                        message=message,
                                        timestamp=timestamp)
                self.profile.add_message(new_msg)
                self.profile.add_classmates(recipient)
                self.profile.save_profile()
                return True
        except TimeoutError:
            print("TimeoutError while joining the server:")
        return False

    def retrieve_new(self) -> list:
        """
        Retrieves new unread messages.
        """
        try:
            if not self.token:
                return []
            n_msg = request_unread_messages(self.token, "new")
            response = send_message(self.send_stream, self.recv_stream, n_msg)
            # Part 3: Store Messages Locally
            if response and response.type != "error":
                try:
                    messa = response.messages
                    message_objects = [DirectMessage(
                        recipient=m.get('recipient'),
                        sender=m.get('from'),
                        message=m.get("message"),
                        timestamp=m.get("timestamp"))
                                       for m in messa]
                    for msg in message_objects:
                        self.profile.add_message(msg)
                        self.profile.add_classmates(msg.sender)
                        self.profile.save_profile()
                    return message_objects
                except OSError:
                    return []
            else:
                return []
        except TimeoutError:
            return []

    def retrieve_all(self) -> list:
        """
        Retrieves all stored messages from the local profile.
        """
        # Part 3: Store Messages Locally
        return self.profile.get_messages()
