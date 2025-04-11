# frame.py

"""
Graphic User Interface module for ds_messenger.py
"""

import tkinter as tk
from tkinter import ttk, simpledialog
from typing import Text
from ds_messenger import DirectMessenger


class Body(tk.Frame):
    """Represents the main chat interface containing messages and contacts."""
    def __init__(self, root, recipient_selected_callback=None):
        """Initializes the Body frame."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = []
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, _):
        """Handles selection of a contact from the tree view."""
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """Inserts a contact into the contact list."""
        self._contacts.append(contact)
        con_id = len(self._contacts) - 1
        self._insert_contact_tree(con_id, contact)

    def _insert_contact_tree(self, con_id, contact: str):
        """Inserts a contact into the tree view."""
        if len(contact) > 25:
            _ = contact[:24] + "..."
        con_id = self.posts_tree.insert('', con_id, con_id, text=contact)

    def insert_user_message(self, message: str):
        """Inserts a user-sent message into the chat window."""
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        """Inserts a received message into the chat window."""
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """Retrieves the current text from the message entry field."""
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """Sets the text in the message entry field."""
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """Draws the layout for the chat interface."""
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """Represents the footer with a send button."""
    def __init__(self, root, send_callback=None):
        """Initializes the Footer frame."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """Handles send button click event."""
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """Draws the footer layout with a send button."""
        # Part 4: The Graphical User Interface
        save_button = tk.Button(
            master=self, text="Send", width=20, command=self.send_click
            )
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """NewContactDialog class for handling UI interactions."""
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        """Initializes the NewContactDialog"""
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        """Body frame for adding contact UI"""
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()
        # Part 4: The Graphical User Interface
        self.password_label = tk.Label(frame, width=30, text="password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        """apply new contacts"""
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """Main application class for handling UI interactions."""
    def __init__(self, root):
        """Initializes the MainApp frame."""
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.sender = ''
        # Part 4: The Graphical User Interface
        self.direct_messenger = None
        self._draw()

    def send_message(self):
        """Sends a message to the selected recipient."""
        # Part 4: The Graphical User Interface
        if self.recipient and self.direct_messenger:
            message = self.body.get_text_entry()
            if message:
                success = self.direct_messenger.send(message, self.recipient)
                if success:
                    formatted_message = f"You: {message}"
                    self.body.insert_user_message(formatted_message)
                    if self.recipient not in self.body._contacts:
                        self.body.insert_contact(self.recipient)
                else:
                    print("Failed to send message.")
            self.body.set_text_entry("")

    def add_contact(self):
        """Prompts the user to add a new contact."""
        # Part 4: The Graphical User Interface
        new_contact = simpledialog.askstring("Add Contact",
                                             "Enter the username:")
        if new_contact:
            self.body.insert_contact(new_contact)

    # Part 4: The Graphical User Interface
    def recipient_selected(self, recipient):
        """Retrive and display messages for selected recipient"""
        self.recipient = recipient
        self.body.entry_editor.delete(1.0, tk.END)

        if self.direct_messenger:
            all_messages = self.direct_messenger.retrieve_all()
            chat_history = [
                msg for msg in all_messages
                if msg.recipient == recipient or
                msg.sender == recipient or msg.recipient == self.username
                ]

            for msg in chat_history:
                sender = "You" if msg.sender == self.username else msg.sender
                formatted_message = f"{sender}: {msg.message}"
                if sender == "You":
                    self.body.insert_user_message(formatted_message)
                else:
                    self.body.insert_contact_message(formatted_message)

    def configure_server(self):
        """Configures the server and login credentials."""
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger = DirectMessenger(
            self.server, self.username, self.password)
        print(f"Configured server: {self.server}, Username: {self.username}")

    def publish(self, sender: str, message: str):
        """Publishs the sent & recieved message"""
        if sender not in self.body._contacts:
            self.body.insert_contact(sender)
        if sender == self.username:
            self.body.insert_user_message(message)
        else:
            self.body.insert_contact_message(message)

    def check_new(self):
        """checks the new message recieved"""
        if self.direct_messenger:
            new_messages = self.direct_messenger.retrieve_new()
            for msg in new_messages:
                sender = msg.get('from', '')
                message = msg.get('message', '')
                if sender and message:
                    if sender not in self.body._contacts:
                        self.body.insert_contact(sender)
                    self.publish(sender, message)
        self.after(3000, self.check_new)

    def _draw(self):
        """Draw the Mainapp with add function"""
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
