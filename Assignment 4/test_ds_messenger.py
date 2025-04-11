# test_ds_messenger.py
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

"""
Testing module for ds_messenger.py
"""

import unittest
from unittest.mock import patch, MagicMock
from ds_messenger import DirectMessenger
from ds_protocol import Data
from Profile import DirectMessage

# coverage testing:
# 1. coverage run -m pytest .
# 2. coverage report -m (shows report with percent)
# 3. coverage run -m --branch pytest . (branch coverage)


class TestDirectMessenger(unittest.TestCase):
    """Test DirectMessenger class"""
    def setUp(self):
        """Setup testing environment"""
        with patch("ds_messenger.Profile") as mock_profile, \
             patch("ds_messenger.socket.socket") as mock_socket:
            self.mock_profile = mock_profile.return_value
            self.mock_socket_instance = mock_socket.return_value
            self.mock_socket_instance.makefile.return_value = MagicMock()
            self.messenger = DirectMessenger("test_server",
                                             "test_user", "test_pass")
            self.messenger.token = "test_token"

    @patch("ds_messenger.send_message")
    @patch("ds_messenger.create_join_message")
    def test_join_server_success(self, _, mock_send_message):
        """Test successful server join"""
        mock_send_message.return_value = Data("test_token",
                                              "success", "Joined", [])
        self.assertTrue(self.messenger.join_server())
        self.assertEqual(self.messenger.token, "test_token")

    @patch("ds_messenger.send_message")
    def test_join_server_timeout(self, mock_send_message):
        """Test server join timeout"""
        mock_send_message.side_effect = TimeoutError("Connection timed out")
        result = self.messenger.join_server()
        self.assertFalse(result)

    @patch("ds_messenger.send_message")
    @patch("ds_messenger.send_direct_msg")
    def test_send_message_success(self, mock_send_direct_msg,
                                  mock_send_message):
        """Test successful message send and profile update"""
        mock_send_message.return_value = Data("", "success", "Sent", [])
        recipient = "friend"
        message = "Hello!"
        result = self.messenger.send(message, recipient)
        self.assertTrue(result)
        self.mock_profile.add_message.assert_called_once()
        self.mock_profile.add_classmates.assert_called_once_with(recipient)
        mock_send_direct_msg.assert_called_once_with("test_token",
                                                     message,
                                                     recipient,
                                                     unittest.mock.ANY)

    @patch("ds_messenger.send_message")
    @patch("ds_messenger.send_direct_msg")
    def test_send_message_error_response(self, _, mock_send_message):
        """Test message send failure due to error response"""
        mock_send_message.return_value = Data("", "error", "Failed", [])
        self.assertFalse(self.messenger.send("Hello", "recipient"))
        self.mock_profile.add_message.assert_not_called()
        self.mock_profile.add_classmates.assert_not_called()

    @patch("ds_messenger.send_message")
    def test_send_message_no_token(self, _):
        """Test message send failure due to missing token"""
        self.messenger.token = None
        self.assertFalse(self.messenger.send("Hello", "recipient"))

    @patch("ds_messenger.send_message")
    def test_send_message_timeout(self, mock_send_message):
        """Test message send timeout"""
        mock_send_message.side_effect = TimeoutError("Connection timed out")
        self.assertFalse(self.messenger.send("Hello", "recipient"))

    @patch("ds_messenger.send_message")
    @patch("ds_messenger.send_direct_msg")
    def test_send_message_constructs_correct_message(self,
                                                     mock_send_direct_msg,
                                                     mock_send_message):
        """Test send() constructs the correct message (Lines 61-66)"""
        mock_send_message.return_value = Data("", "success", "Sent", [])
        recipient = "friend"
        message = "Hello!"
        self.messenger.send(message, recipient)

        mock_send_direct_msg.assert_called_once_with("test_token",
                                                     message, recipient,
                                                     unittest.mock.ANY)

    @patch("ds_messenger.send_message")
    def test_retrieve_new_success(self, mock_send_message):
        """Test retrieving and storing new messages successfully"""
        messages = [
            {"recipient": "test_user", "from": "user1",
             "message": "Hello!", "timestamp": "12345"},
            {"recipient": "test_user", "from": "user2",
             "message": "How are you?", "timestamp": "12346"},
        ]
        mock_send_message.return_value = Data("", "success", "", messages)
        result = self.messenger.retrieve_new()
        self.assertEqual(len(result), 2)
        self.assertEqual(self.mock_profile.add_message.call_count, 2)
        self.assertEqual(self.mock_profile.add_classmates.call_count, 2)
        self.mock_profile.save_profile.assert_called()

    @patch("ds_messenger.send_message")
    def test_retrieve_new_no_token(self, _):
        """Test retrieving new messages when token is missing"""
        self.messenger.token = None
        messages = self.messenger.retrieve_new()
        self.assertEqual(messages, [])

    @patch("ds_messenger.send_message")
    def test_retrieve_new_invalid_json(self, mock_send_message):
        """Test retrieving new messages with JSON decode error"""
        mock_send_message.return_value = Data("", "error", "Invalid", [])
        messages = self.messenger.retrieve_new()
        self.assertEqual(messages, [])

    @patch("ds_messenger.send_message")
    def test_retrieve_new_no_response(self, mock_send_message):
        """Test retrieving new messages when no response is returned"""
        mock_send_message.return_value = Data("", "success", "", [])
        messages = self.messenger.retrieve_new()
        self.assertEqual(messages, [])

    @patch("ds_messenger.send_message")
    def test_retrieve_new_server_error(self, mock_send_message):
        """Test retrieve_new() when server returns an error"""
        mock_send_message.return_value = Data("", "error", "Server Error", [])
        result = self.messenger.retrieve_new()
        self.assertEqual(result, [])
        self.mock_profile.add_message.assert_not_called()
        self.mock_profile.add_classmates.assert_not_called()

    @patch("ds_messenger.send_message")
    def test_retrieve_new_timeout_handling(self, mock_send_message):
        """Test TimeoutError"""
        mock_send_message.side_effect = TimeoutError("Timeout occurred")
        result = self.messenger.retrieve_new()
        self.assertEqual(result, [])
        mock_send_message.assert_called_once()

    @patch("ds_messenger.send_message")
    def test_retrieve_all_messages(self, _):
        """Test retrieving all stored messages"""
        stored_messages = [
            DirectMessage(recipient="user1", sender="test_user",
                          message="Hi", timestamp="123456")
        ]
        self.mock_profile.get_messages.return_value = stored_messages
        messages = self.messenger.retrieve_all()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "Hi")
