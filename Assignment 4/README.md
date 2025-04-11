README for a4.py

[Overview]
This project is a graphical user interface (GUI) application for the "ICS 32 Distributed Social Messenger" built using Python's Tkinter library. The main script (a4.py) initializes the application and manages the user interface.

- Features -
Uses tkinter to create a GUI-based messenger application.
Imports and runs the MainApp class from the frame module.
Sets up the main application window with a minimum size of 720x480.
Uses a timed event (after(2000, app.check_new)) to periodically check for new messages.
Runs on port 3001, as specified in the script.

Prerequisites - Ensure you have Python installed (preferably Python 3.6 or later).
Required Dependencies - Make sure you have the necessary dependencies installed: pip install tk
How to Run - Ensure that the frame module is available in the same directory or installed in your environment.
Run the script using: python a4.py, The GUI window should appear with the title "ICS 32 Distributed Social Messenger".

[Code Structure]
a4.py: The main entry point that initializes the Tkinter GUI.
ds_messenger.py: Contains the DirectMessenger class which handles the direct messaging functionality of the aplication
ds_protocol.py: Contains the functions for handling the direct messaging protocol.
frame.py: Contains the MainApp class which handles the core functionality of the application.
Profile.py: Contains the Profile class which handles the profile-related functionality of the application
server.py: Contains the DSUServer class which handles the server-side functionality of the application
test_ds_messenger.py: Contains unit tests for the DirectMessenger class
test_ds_protocol.py: Contains unit tests for the ds_protocol module

Configuration - The application runs on port 3001. If necessary, modify the port in a4.py.
If frame.py is missing, ensure that it is available in the same directory.
If the application does not start, check for missing dependencies and install them.
Ensure that port 3001 is not blocked by a firewall.

Evan-Soobin Jeon
Email: ejeon2@uci.edu
Student ID: 35377131