# ui.py
# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

import pathlib
import shlex  # shlex is a python module that provides a lexical analyzer for simple shell-like syntaxes
from Profile import Profile, Post  # import profile.py


# Part 1 - Creating and Opening Profile
# 1-1. create dsu file and collect user data
def create_profile(directory, filename):  # For User mode
    dir_path = pathlib.Path(directory).resolve()  # create a path object from the directory
    # resolve() returns the absolute path of the directory

    if not dir_path.is_dir():  # check if the path is a directory
        print("File you wanted to create is not located in dircetory.")
        return None, None  # for profile and path

    file_path = dir_path / f"{filename}.dsu"

    if file_path.exists():  # if file already exists, we should open the file instead.
        print("File you asked is already exists. Loading existing file:")
        return open_profile(str(file_path))

    # Collect user data
    print('\nPlease Enter Your Information\n')
    username = input('Please Enter Your Username: ').strip()
    if not username:
        print('Profile creation was canceled')
        return None, None  # only create the file after user data is collected.

    password = input('Please Enter Your Password: ').strip()
    if not password:
        print('Profile creation was canceled')
        return None, None

    bio = input('Please Enter Your Bio: ').strip()
    if not bio:
        print('Profile creation was canceled')
        return None, None

        # Create and store date into profile
    profile = Profile()  # create an instance of profile from profile.py - Class Profile
    # profile.dsuserver = dsuserver
    profile.username = username
    profile.password = password
    profile.bio = bio

    # save profile to file
    try:
        file_path.touch(exist_ok=False)  # create a file at the file_path
        profile.save_profile(str(file_path))  # Uses save_profile() from Profile.py
        print(f"Your profile is sucessfully created at {file_path}")
    except Exception as e:
        print('ERROR: cannnot create the file - {e}')
        return None, None

    return profile, str(
        file_path)  # return the profile and the path. why? because the profile and the path will be used in edit_profile()


# 1-2. open and diaplay user details of dsu file
def open_profile(filepath):
    path = pathlib.Path(filepath)  # create a path object from the filepath

    if not path.exists() or not path.is_file() or path.suffix != ".dsu":  # check if the path is a file, and the file is a dsu file, and the file exists
        print("ERROR: Invalid file.")
        return None, None  # return None for both profile and path.

    profile = Profile()  # create an instance of profile from profile.py - Class Profile
    profile.load_profile(str(path))  # load_profile method is from profile.py
    # load_profile() will populate the current instance of Profile with data stored in a DSU file

    # display user details in output
    print(f"\nProfile Loaded Sucessfully!")
    print(f"Username: {profile.username}")
    print(f"Password: {profile.password}")
    print(f"Bio: {profile.bio}")

    return profile, str(
        path)  # return the profile and the path. why? because the profile and the path will be used in edit_profile()


# Part 2 - Editing and Printing profile
# 2-1. edit_profile() will edit the loaded profile based on user input options.
def edit_profile(profile, profile_path, lst):  # lst is a list of strings
    # example of multiple options: E - usr evanjeon - pwd 1234
    # why lst? because the user can input multiple options at once
    try:
        i = 0  # why i = 0? because the first element is the command. It is also an index.
        # why should we state i = 0? because we need to iterate through all the elements in the list.
        while i < len(lst):  # why i < len(lst)? because we need to iterate through all the elements in the list
            # ex) -usr evanjeon
            #       0     1
            if lst[i] == "-usr":  # if not username, then next option is  "-usr"
                i += 1  # why i += 1? because the next element is the usernae. example: evanjeon

                if i < len(lst):  # why i < len(lst)? because we need to check if the next element exists.
                    # if the next element does not exist, it will throw an error.
                    profile.username = lst[i]  # set the username to the next element
                    print("Profile updated successfully.")

                else:
                    print("ERROR: Missing username.")
                    return  # return will exit the function
            # ex) -pwd 1234
            #      0    1

            elif lst[i] == "-pwd":  # if not username, then next option is  "-pwd"
                i += 1  # why i += 1? because the next element is the password example: 1234
                if i < len(lst):
                    profile.password = lst[i]
                    print("Profile updated successfully.")

                else:
                    print("ERROR: Missing password.")
                    return

            elif lst[i] == "-bio":  # if not password, then next option is "-bio"
                # why bio? because bio is the last option of the list
                # example: E -usr evanjeon - pwd 1234 -bio "I'm a ICS 32 student"
                i += 1  # why i += 1? because the next element is the bio. example: "I'm a ICS 32 student"
                if i < len(lst):
                    profile.bio = lst[i]
                    print("Profile updated successfully.")

                else:
                    print("ERROR: Missing bio.")
                    return

            elif lst[i] == "-addpost":  # if not bio, the next optio is "-addpost"
                i += 1  # example: E -usr evanjeon -pwd 1234 -bio "I'm a ICS 32 student" -addpost "I'm a post"
                if i < len(lst):  # checks if the next element exists.
                    profile.add_post(
                        Post(lst[i]))  # add_post() is from Profile.py - add_post() will add a post to the profile.
                    print("Profile updated successfully.")

                else:
                    print("ERROR: Missing post content.")
                    return

            elif lst[i] == "-delpost":  # if not addpost, the next option is "-delpost"
                i += 1  # example: E -usr evanjeon -pwd 1234 -bio "I'm a ICS 32 student" -delpost 1
                # from the example above, 1 is the post id
                # post id is the index of the post in the list of posts. if post id is 1, the second post will be deleted.
                if i < len(lst):
                    try:
                        post_id = int(lst[i])  # convert the post id to an integer
                        if not profile.del_post(
                                post_id):  # del_post() is fro Profile.py - del_post() will delete a post from the profile. exmaple of post: I'm a post
                            # why if not? because del_post() will return False if the post id is invalid.
                            print(f"ERROR: Invalid post ID {post_id}.")
                            return
                        else:
                            print("Profile updated successfully.")
                    except ValueError:
                        print("ERROR: Post ID must be an integer.")
                        return
                else:
                    print("ERROR: Missing post ID.")
                    return
            else:
                print('ERROR: please enter valid command.')

            i += 1  # why i += 1? because we need to iterate through all elements in the list.
        # Save the updated profile
        profile.save_profile(
            profile_path)  # save_profile() is from Profile.py - save_profile() will save the profile into a DSU file.
        # profile_path is from open_profile() - open_profile() will return the path of the DSU file.
        # post = E -usr evanjeon -pwd 1234 -bio "I'm a ICS 32 student" -addpost "I'm a post" -del post 0
        # from the example above, the profile will be updated with the new post and the post with the id of 0 (which is the first post - I'm a post)

    except Exception as e:
        print(f"ERROR: {e}")


# 2-2. print_profile() will print data from the loaded profile based on user input options.
def print_profile(profile, lst):  # lst is a list of strings. example: P -usr evanjeon -pwd 1234
    # whitespace is used to separate the options
    try:
        if "-usr" in lst:
            print(f"Username: {profile.username}")

        if "-pwd" in lst:
            print(f"Password: {profile.password}")

        if "-bio" in lst:
            print(f"Bio: {profile.bio}")

        if "-posts" in lst:
            print("Posts:")
            for index, post in enumerate(
                    profile.get_posts()):  # get_posts() is from Profile.py - get_posts() will return a list of posts
                # enumerate() will return the index and the element of the list
                # example: 0: I'm a post. 1: I'm a post 2.
                print(f"{index}: {post.entry}")  # .entry is from Profile.py - it will return the post content

        if "-post" in lst:
            try:
                post_index = lst.index("-post") + 1  # find the index of "-post" and add 1 to get the post id
                # index() will return the index of the first occurrence of the element in the list
                if post_index < len(
                        lst):  # check if the post id exists. why? because the post id is the next element after "-post"
                    post_id = int(lst[post_index])  # post id is the next element after "-post"
                    if 0 <= post_id < len(
                            profile.get_posts()):  # check if the post id is valid. why 0 <= and 1 < len(profile.gets_posts())? because the post id should be greater than or equal to 0 and less than the length of the list of posts.
                        print(
                            f"Post {post_id}: {profile.get_posts()[post_id].entry}")  # get_posts() is from Profile.py. entry is from Profile.py
                    else:
                        print("ERROR: Invalid post ID.")
                else:
                    print("ERROR: Missing post ID.")
            except (IndexError):
                print("ERROR: Invalid post ID format.")
            except (ValueError):
                print('ERROR: Post ID must be an integer.')

        if "-all" in lst:  # if the user wants to print all the data: username, password, bio, and posts
            print(f"Username: {profile.username}")
            print(f"Password: {profile.password}")
            print(f"Bio: {profile.bio}")
            print("Posts:")
            for index, post in enumerate(profile.get_posts()):  # function of "-posts"
                # enumerate creates the list by index with posts
                # 0 : post
                # 1 : Second post
                print(f"{index}: {post.entry}")

    except Exception as e:
        print(f"ERROR: {e}")


# Part 3 - Creating User Interface (UI)
# 3-1 User_interface() will display the commands that the user can use.
def User_interface():
    print("\nWelcome to the DSU Profile Manager Application!\n")
    print("Here are the commands you can use:")
    print('c - You can create a new DSU file.')  # create_profile()
    print('o - You can open an existing DSU file.')  # open_profile()
    print('e - You can edit the profile.')  # edit_profile()
    print('p - You can print the profile.')  # print_profile()
    print('admin - You can switch application into admin mode.')  # admin_mode
    print('q - You can quit the appliction.')
    print('If you have any issues with the application, please contact via email: ejeon2@uci.edu')
    print('Thank you for visiting our DSU Profile Manager Application!')


def admin_create_profile(directory, filename):  # For admin mode
    dir_path = pathlib.Path(directory).resolve()  # create a path object from the directory
    # resolve() returns the absolute path of the directory

    if not dir_path.is_dir():  # check if the path is a directory
        print("dir_path is not a dircetory.")
        return None, None  # for profile and path

    file_path = dir_path / f"{filename}.dsu"

    if file_path.exists():  # if file already exists, we should open the file instead.
        print("File already exists. Loading existing file:")
        return open_profile(str(file_path))

    username = input().strip()
    if not username:
        print('Profile creation was canceled')
        return None, None  # only create the file after user data is collected.

    password = input().strip()
    if not password:
        print('Profile creation was canceled')
        return None, None

    bio = input().strip()
    if not bio:
        print('Profile creation was canceled')
        return None, None

        # Create and store date into profile
    profile = Profile()  # create an instance of profile from profile.py - Class Profile
    # profile.dsuserver = dsuserver
    profile.username = username
    profile.password = password
    profile.bio = bio

    # save profile to file
    try:
        file_path.touch(exist_ok=False)  # create a file at the file_path
        profile.save_profile(str(file_path))  # Uses save_profile() from Profile.py
        print(f"Creation completed: {file_path}")
    except Exception as e:
        print('ERROR: cannnot create the file - {e}')
        return None, None

    return profile, str(
        file_path)  # return the profile and the path. why? because the profile and the path will be used in edit_profile()