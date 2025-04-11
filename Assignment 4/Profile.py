# profile.py
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

"""
Profile Module
This module provides classes for handling profiles, direct messages, and posts.
"""

import json
from pathlib import Path


class DsuFileError(Exception):
    """Exception raised for DSU file errors."""


class DsuProfileError(Exception):
    """Exception raised for DSU profile errors."""


# Part 3: Store Messages Locally
class DirectMessage(dict):
    """Class representing a direct message."""
    def __init__(self, recipient=None, sender=None, message=None,
                 timestamp=None):
        """Initialize a DirectMessage instance."""
        self.recipient = recipient
        self.sender = sender
        self.message = message
        self.timestamp = timestamp
        dict.__init__(self, recipient=self.recipient, sender=self.sender,
                      message=self.message, timestamp=self.timestamp)


class Profile:
    """Class representing a user profile."""
    def __init__(self, dsuserver=None, username=None, password=None,
                 profile_path="user_data.dsu"):
        """Initialize a Profile instance."""
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        # Part 3: Store Messages Locally
        self._messages = []
        self._classmates = set()  # in order to remove duplicates
        self.profile_path = profile_path

    # Part 3: Store Messages Locally
    def add_message(self, message: DirectMessage) -> None:
        """Add a message to the profile."""
        self._messages.append(message)

    def add_classmates(self, classmate: str) -> None:
        """Add a classmate to the profile."""
        self._classmates.add(classmate)

    # Part 3: Store Messages Locally
    def get_messages(self) -> list[DirectMessage]:
        """Get all messages."""
        return self._messages

    def get_classmates(self) -> list[str]:
        """Get all classmates as a sorted list."""
        return list(self._classmates)  # convert set into list to sort

    def save_profile(self) -> None:
        """Save profile to a DSU file."""
        try:
            profile_data = {
                "dsuserver": self.dsuserver,
                "username": self.username,
                "password": self.password,
                "profile_path": self.profile_path,
                "_messages": [{"recipient": m.recipient,
                               "sender": m.sender,
                               "message": m.message,
                               "timestamp": m.timestamp}
                              for m in self._messages],
                "_classmates": list(self._classmates),
            }

            with open(self.profile_path, 'w', encoding="utf-8") as f:
                json.dump(profile_data, f, indent=4)

        except Exception as e:
            raise DsuFileError(f"Error saving profile: {e}") from e

    def load_profile(self, profile_path=None) -> None:
        """Load profile from a file"""
        try:
            if profile_path:
                self.profile_path = profile_path
            if not Path(self.profile_path).exists():
                self.save_profile()
            if Path(self.profile_path).stat().st_size == 0:
                self.save_profile()
            if Path(self.profile_path).exists():
                with open(self.profile_path, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                    self.dsuserver = obj.get('dsuserver', '')
                    self.username = obj.get('username', '')
                    self.password = obj.get('password', '')
                # Part 3: Store Messages Locally
                    self._messages = [
                        DirectMessage(m['recipient'],
                                      m['sender'],
                                      m['message'],
                                      m['timestamp'])
                        for m in obj.get('_messages', [])]
                    self._classmates = set(obj.get('_classmates', []))
        except Exception as e:
            raise DsuFileError(f"Error loading profile: {e}") from e
