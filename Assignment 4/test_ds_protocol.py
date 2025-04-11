# test_ds_protocol.py
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

"""
This module contains unit tests for ds_protocol to ensure all functions
work correctly and meet expected behaviors.
"""

import json
from unittest.mock import patch, MagicMock
from ds_protocol import (
    create_join_message, send_direct_msg, request_unread_messages,
    request_all_messages, extract_json, send_message, Data
)

# coverage testing:
# 1. coverage run -m pytest .
# 2. coverage report -m (shows report with percent)
# 3. coverage run -m --branch pytest . (branch coverage)


def test_create_join_message():
    """Test for create_join_message"""
    username = "test_user"
    password = "test_pass"
    expected = json.dumps({
        "join": {
            "username": username,
            "password": password,
            "token": ""
        }
    })
    assert create_join_message(username, password) == expected


def test_send_direct_msg():
    """Test for send_direct_msg"""
    token = "test_token"
    message = "Hello"
    recipient = "recipient_user"
    timestamp = "1234567890"
    expected = json.dumps({
        "token": token,
        "directmessage": {
            "recipient": recipient,
            "entry": message,
            "timestamp": timestamp
        }
    })
    assert send_direct_msg(token, message, recipient, timestamp) == expected


def test_request_unread_messages():
    """Test for request_unread_messages"""
    token = "test_token"
    expected = json.dumps({
        "token": token,
        "directmessage": "new"
    })
    assert request_unread_messages(token, "") == expected


def test_request_all_messages():
    """Test for request_all_messages"""
    token = "test_token"
    expected = json.dumps({
        "token": token,
        "directmessage": "all"
    })
    assert request_all_messages(token, "") == expected


def test_extract_json_valid():
    """Test for extracting valid JSON response"""
    json_data = json.dumps({
        "response": {
            "token": "abc123",
            "type": "success",
            "message": "Operation successful",
            "messages": ["msg1", "msg2"]
        }
    })
    expected = Data("abc123", "success", "Operation successful",
                    ["msg1", "msg2"])
    assert extract_json(json_data) == expected


def test_extract_json_invalid_json():
    """Test for extracting an invalid JSON"""
    invalid_json = '{"response": {"token": "xyz" "type": "error"}}'
    expected = Data("error", "", "", [])
    assert extract_json(invalid_json) == expected


def test_extract_json_no_response_key():
    """Test for JSON without response key"""
    json_data = json.dumps({"invalid_key": {}})
    expected = Data("", "", "", [])
    assert extract_json(json_data) == expected


def test_extract_json_missing_fields():
    """Test for extracting JSON with missing fields"""
    json_data = json.dumps({"response": {"type": "error"}})
    expected = Data("", "error", "", [])
    assert extract_json(json_data) == expected


def test_extract_json_empty_string():
    """Test for extracting from an empty string"""
    expected = Data("error", "", "", [])
    assert extract_json("") == expected


def test_extract_json_non_string_input():
    """Test for extracting from a non-string input"""
    expected = Data("error", "", "", [])
    assert extract_json(12345) == expected


def test_send_message_valid():
    """Test for sending a valid message"""
    class FakeStream:
        """Fake stream class for testing"""
        def __init__(self, response):
            self.response = response
            self.data = ""

        def write(self, data):
            """Write data"""
            self.data = data

        def flush(self):
            """Flush data"""

        def readline(self):
            """Read line"""
            return self.response

    response_json = json.dumps({
        "response": {
            "token": "valid_token",
            "type": "success",
            "message": "Message sent",
            "messages": []
        }
    })

    send_stream = FakeStream("")
    recv_stream = FakeStream(response_json + "\n")
    expected = Data("valid_token", "success", "Message sent", [])
    assert send_message(send_stream, recv_stream,
                        '{"token": "xyz"}') == expected


def test_send_message_empty_response():
    """Test for sending a message with empty response"""
    class FakeStream:
        """Fake stream class for testing"""
        def __init__(self, response=""):
            self.response = response

        def write(self, _):
            """Write data"""

        def flush(self):
            """Flush data"""

        def readline(self):
            """Read line"""
            return self.response

    send_stream = FakeStream()
    recv_stream = FakeStream("\n")
    expected = Data("error", "", "", [])
    assert send_message(send_stream, recv_stream,
                        '{"token": "xyz"}') == expected


@patch("builtins.print")
def test_send_message_timeout(mock_print):
    """Test for TimeoutError handling in send_message()."""
    fake_send_stream = MagicMock()
    fake_recv_stream = MagicMock()

    with patch.object(fake_send_stream, "write",
                      side_effect=TimeoutError("Mock Timeout")):
        result = send_message(fake_send_stream,
                              fake_recv_stream, '{"key": "value"}')
        mock_print.assert_called_with("TimeoutError occured: Mock Timeout")
        assert isinstance(result, Data)
        assert result.token == "error"
        assert result.type == ""
        assert result.message == "Timeout while sending message"
        assert result.messages == []
