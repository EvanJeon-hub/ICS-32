# ds_client.py
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

import socket
from ds_protocol import create_join_message, create_post_message
from ds_protocol import send_message, create_bio_message


def send(server: str, port: int, username: str,
         password: str, message: str, bio: str = None, timestamp: str = None):
    try:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cs:
            cs.settimeout(5)
            cs.connect((server, port))

            with cs.makefile('w') as st, cs.makefile('r') as rt:

                # Join Server
                join_msg = create_join_message(username, password)
                response = send_message(st, rt, join_msg, "Join")

                if response is None or response.type == "error":
                    print("Error joining server:",
                          response.message if response else "No response")
                    return False

                token = response.token

                # Send Post
                if message:
                    post_msg = create_post_message(token, message, timestamp)
                    post_response = send_message(st, rt, post_msg, "Post")

                    if not post_response or post_response.type == "error":
                        print("Error posting message:",
                              post_response.message if post_response else
                              "Unknown error")
                        return False

                # Send/Update Bio
                if bio:
                    bio_msg = create_bio_message(token, bio, timestamp)
                    bio_response = send_message(st, rt, bio_msg, "Bio")

                    if not bio_response or bio_response.type == "error":
                        print("Error updating bio:",
                              bio_response.message if bio_response else
                              "Unknown error")
                        return False

                return True

    except socket.timeout:
        print("Error: Server connection timed out.")
        return False

    except ConnectionError as ce:
        print(f"Connection Error: {ce}")
        return False

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False

