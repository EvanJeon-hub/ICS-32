# a2.py
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

import ui  # import ui.py
import pathlib
import shlex  # shlex is a python module that provides a lexical analyzer for simple shell-like syntaxes
from Profile import Profile, Post  # import profile.py


# example of input = C /Users/evanjeon/"ICS 32 - Assignment 2"/ -n evanjeon
# example of dsu file name: /Users/evanjeon/ICS 32 - Assignment 2/evanjeon.dsu
# Example edit command:  -usr evanjeon -pwd 1234 -bio "I'm a ICS 32 student"

def main():
    profile = None  # why None? because the profile is not loaded yet. It will be loaded when the user uses the open_profile () in O command.
    profile_path = None  # why None? because the profile is not loaded yet. It will be loaded when the user uses the open_profile () in O command.
    admin_mode = False  # why False? because the admin mode is not actived yet. It will activated when the user uses the admin command.

    while True:

        # 3-2. User mode
        if not admin_mode:
            ui.User_interface()
            user_command = input('Please enter a command: ').strip()  # strip() removes leading and trailing whitespaces

            if user_command.upper() == 'C':  # create_profile
                user_input = input('Good! What is the name of the file do you want to create?\n')
                Token = shlex.split(user_input)  # split the user_command into tokens by whitespaces
                if len(Token) == 3 and Token[
                    1] == "-n":  # check if the token has 3 elements and the second element is -n
                    directory = Token[0]  # First token is the directory since It is the user mode
                    filename = Token[2]  # last token will be the filename
                    # /Users/evanjeon/"ICS 32 - Assignment 2"/ -n evanjeon
                    #             0(directory)                 1    2(filename)
                    profile, profile_path = ui.create_profile(Token[0],
                                                              Token[2])  # create_profile is from this file (ui.py)
                else:
                    print("ERROR: Invalid C command format.")

            elif user_command.upper() == 'O':  # open_profile
                filepath = input('Great! what is the name of the file you want to load?\n').strip()
                if filepath:
                    profile, profile_path = ui.open_profile(filepath)  # open_profile returns profile, str(path)
                    # profile is returned to profile, str(path) is returned to profile_path
                else:
                    print("ERROR: File path cannot be empty.")

            elif user_command.upper() == 'E':  # edit_profile
                if profile and profile_path:
                    print('\nHere are several options you can make:')
                    print("Changing username: '-usr new_username'")
                    print("Changing password: '-pwd new_password'")
                    print("Changing bio: '-bio new_bio'")
                    print("Adding a new post: '-addpost your_post'")
                    print("Deleting a post: '-delpost post_number'\n")
                    edit_command = input("Please enter edit command: ").strip()
                    if edit_command:
                        ui.edit_profile(profile, profile_path, shlex.split(
                            edit_command))  # why shlex.split? edit_profile(profile, profile_path, and lst)
                        # lst is list of string, therefore edit_command must be changed into the list by splitting by whitspaces.
                        # ex) lst = ['-usr', 'Evan']
                        #               0       1
                    else:
                        print('ERROR: Edit command cannot be empty.')

                else:
                    print('ERROR: No profile is loaded.')

            elif user_command.upper() == 'P':  # print_profile
                if profile:
                    print('\nHere are several options you can make:')
                    print("Viewing username: '-usr")
                    print("Viewing password: '-pwd")
                    print("Viewing bio: '-bio'")
                    print("Viewing all posts: '-posts'")
                    print("Viewing a specific post: '-post post_number'")
                    print("Viewing every content: '-all'\n")
                    printing_command = input("Please enter print command: ").strip()
                    if printing_command:
                        ui.print_profile(profile,
                                         shlex.split(printing_command))  # why shlex.split? print_profile(profile, lst)
                        # lst is list of string, therefore edit_command must be changed into the list by splitting by whitspaces.
                        # ex) lst = ['-post', '0']
                        #               0      1
                    else:
                        print('ERROR: Print command cannot be empty.')

                else:
                    print('ERROR: Profile not printed')

            elif user_command.upper() == 'ADMIN':  # admin_mode
                admin_mode = True

            elif user_command.upper() == 'Q':
                print('Thank you for using the DSU Profile Manager Application!')
                break

            else:
                print('ERROR: Invalid command. Please enter valid command.')

        # 3-3. Admin mode
        else:
            input_command = input().strip()  # strip() removes leading and trailing whitespaces
            if input_command.upper() == "Q":  # quit command
                break

            try:
                token = shlex.split(input_command)  # split the input_command into tokens by whitespaces
                if not token:  # if no command entered
                    print("ERROR")
                    continue

                command = token[0].upper()  # the first token is the comamnd
                # ex) C /Users/evanjeon/"ICS 32 - Assignment 2"/ -n evanjeon2
                # 0                 1(directory)             2    3(filename)
                # token index visualization

                if command == "C":  # create_profile
                    if len(token) == 4 and token[
                        2] == "-n":  # check if the token has 4 elements and the third element is -n
                        directory = token[1]
                        filename = token[3]
                        profile, profile_path = ui.admin_create_profile(token[1], token[
                            3])  # create_profile is from this file (ui.py)
                        # admin_create_profile is create_profile for admin mode
                    else:
                        print("ERROR: Invalid C command format.")

                elif command == "O":
                    if len(token) == 2:  # check if the token has 2 elements. "-n" should be removed
                        profile, profile_path = ui.open_profile(token[1])  # open_profile is from this file (ui.py)
                    else:
                        print("ERROR: Invalid O command format.")

                elif command == 'E':
                    if profile and profile_path:  # check if the profile is loaded
                        ui.edit_profile(profile, profile_path, token[1:])  # edit_profile is from this file (ui.py)
                    # why 1:? because the first element is the command. the rest of the elements are options.
                    else:
                        print('Error: Invalid E command format.')

                elif command == 'P':
                    if profile:  # check if the profile is loaded
                        ui.print_profile(profile, token[1:])  # print_profile is from this file (ui.py)
                    # why 1:? because the first element is the command. the rest of the elements are options.
                    else:
                        print('Error: Invalid P command format.')
                else:
                    print("ERROR: Unknown command.")

            except Exception as e:
                print(f"ERROR: {e}")


if __name__ == '__main__':
    main()