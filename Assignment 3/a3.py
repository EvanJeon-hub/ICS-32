# a3.py
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

import pathlib
import shlex
from Profile import Profile, Post 
import ds_client
import time

# from server.py
port = 3001

# /Users/evanjeon/'ICS 32'/"ICS 32 - Assignment 3"/ -n evan
# pycodestyle check code: open terminal in vscode and type "pycodestyle a3.py"

def create_profile(directory, filename): 
    dir_path = pathlib.Path(directory).resolve() 
    
    if not dir_path.is_dir(): 
        print("File you wanted to create is not located in dircetory.")
        return None, None 
    
    file_path = dir_path / f"{filename}.dsu"
    
    if file_path.exists(): 
        print("File you asked is already exists. Loading existing file:")
        return open_profile(str(file_path))
    
    print('\nPlease Enter Your Information\n')
    dsuserver = input("Enter the DSP Server Address (this will always be '127.0.0.1' or 'localhost'): ").strip()
    username = input('Please Enter Your Username: ').strip() 
    password = input('Please Enter Your Password: ').strip()
    bio = input('Please Enter Your Bio: ').strip() 
       
    if not username or not password or not bio:
        print('Profile creation was canceled')
        return None, None 
    
    ds_client.send(dsuserver, port, username, password, None, bio, str(time.time())) # message is None since we can only add post through edit_profile()
    
    profile = Profile(dsuserver=dsuserver, username=username, password=password)
    profile.bio = bio

    try:
        file_path.touch(exist_ok=False)  # Ensure the file is created before saving
        profile.save_profile(str(file_path.resolve()))  
        print(f"Profile successfully created at {file_path}")
        
    except Exception as e:
        print(f"Error saving profile: {e}")
        return None, None

    return profile, str(file_path)


def open_profile(filepath):
    
    path = pathlib.Path(filepath) 

    if not path.exists() or not path.is_file() or path.suffix != ".dsu": 
        print("ERROR: Invalid file.")
        return None, None 

    profile = Profile() 
    profile.load_profile(str(path)) 
    
    print(f"\nProfile Loaded Sucessfully!")
    print(f"Username: {profile.username}")
    print(f"Password: {profile.password}")
    print(f"Bio: {profile.bio}")
    print(f"DSP Server: {profile.dsuserver}")
    
    return profile, str(path) 


def edit_profile(profile, profile_path, lst):
    try:
        
        if not profile or not profile.dsuserver:
            print("ERROR: No profile loaded or server address is missing.")
            return
        
        i = 0
        
        for i in range(len(lst)): 
            
            if lst[i] == "-usr": 
                i += 1 
                if i < len(lst): 
                    profile.username = lst[i] 
                    print("Profile updated successfully.")
                else:
                    print("ERROR: Missing username.")
                    return
            
            elif lst[i] == "-pwd": 
                i += 1 
                if i < len(lst):
                    profile.password = lst[i]
                    print("Profile updated successfully.")
                else:
                    print("ERROR: Missing password.")
                    return
            
            elif lst[i] == "-bio":
                new_bio = lst[i + 1].strip() if i + 1 < len(lst) else ""
                if new_bio:
                    confirm = input("Publish this bio online? (Yes/No): ").strip().lower()
                    if confirm == "yes":
                        ds_client.send(profile.dsuserver, port, profile.username, profile.password, None, new_bio, str(time.time()))
                        print('\nBio added to the server sucessfully.')
                        profile.bio = new_bio
                        profile.save_profile(profile_path)
                    
            elif lst[i] == "-addpost":
                new_post = lst[i + 1].strip() if i + 1 < len(lst) else ""
                if new_post:
                    confirm = input("Also update your bio? (Yes/No): ").strip().lower()
                    if confirm == "yes":
                        new_bio = input("Enter new bio: ").strip()
                        ds_client.send(profile.dsuserver, port, profile.username, profile.password, new_post, new_bio, str(time.time()))
                        print('\nPost and Bio added to the server sucessfully.')
                        profile.bio = new_bio
                        profile.save_profile(profile_path)
                    else:
                        ds_client.send(profile.dsuserver, port, profile.username, profile.password, new_post, None, str(time.time()))
                        print('\nPost added to the server sucessfully.')
                    profile.add_post(Post(new_post, str(time.time())))
            
            elif lst[i] == "-delpost": 
                i += 1 
                if i < len(lst): 
                    try:
                        post_id = int(lst[i]) 
                        if not profile.del_post(post_id): 
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

    except Exception as e:
        print(f"ERROR in edit_profile: {e}")
        
                
def print_profile(profile, lst): 
    try:
        if not profile:
            print("ERROR: No profile loaded.")
            return
              
        if "-usr" in lst:
            print(f"Username: {profile.username}")

        if "-pwd" in lst:
            print(f"Password: {profile.password}")

        if "-bio" in lst:
            print(f"Bio: {profile.bio}")
        
        if "-posts" in lst:
            print("Posts:")
            for index, post in enumerate(profile.get_posts()): 
                print(f"{index}: {post.entry} (Timestamp: {post.timestamp})")
                
        if "-post" in lst:
            try:
                post_index = lst.index("-post") + 1 
                if post_index < len(lst): 
                    post_id = int(lst[post_index])  
                    if 0 <= post_id < len(profile.get_posts()): 
                        print(f"Post {post_id}: {profile.get_posts()[post_id].entry} (Timestamp: {profile.get_posts()[post_id].timestamp})")
                    else:
                        print("ERROR: Invalid post ID.")
                else:
                    print("ERROR: Missing post ID.")
            except (IndexError, ValueError):
                print("ERROR: Invalid post ID format.") 
        
        if "-all" in lst: 
            print(f"Username: {profile.username}")
            print(f"Password: {profile.password}")
            print(f"Bio: {profile.bio}")
            print(f"DSP Server: {profile.dsuserver}")
            print("Posts:")
            for index, post in enumerate(profile.get_posts()): 
                print(f"{index}: {post.entry} (Timestamp: {post.timestamp})")
                
    except Exception as e:
        print(f"ERROR: {e}")


def User_interface(): 
    print("\nWelcome to the DSU Profile Manager Application!\n")
    print("Here are the commands you can use:")
    print('c - You can create a new DSU file.') # create_profile()
    print('o - You can open an existing DSU file.') # open_profile()
    print('e - You can edit the profile.') # edit_profile()
    print('p - You can print the profile.') # print_profile()
    print('q - You can quit the appliction.') 
    print('If you have any issues with the application, please contact via email: ejeon2@uci.edu')
    print('Thank you for visiting our DSU Profile Manager Application!')
    
    
def main():
    profile = None 
    profile_path = None 
    
    while True:
        User_interface()
        user_command = input('Please enter a command: ').strip() 
            
        if user_command.upper() == 'C': # create_profile
            user_input = input('Good! What is the name of the file do you want to create?\n')
            Token = shlex.split(user_input) 
            if len(Token) == 3 and Token[1] == "-n": 
                profile, profile_path = create_profile(Token[0], Token[2]) 
            else:
                print("ERROR: Invalid C command format.")
                    
        elif user_command.upper() == 'O': # open_profile
            filepath = input('Great! what is the name of the file you want to load?\n').strip()
            if filepath:
                profile, profile_path = open_profile(filepath)
            else:
                print("ERROR: File path cannot be empty.")
                    
        elif user_command.upper() == 'E': # edit_profile
            if profile and profile_path:
                print('\nHere are two options you can make:')
                print('Changing username: -usr new_username')
                print('Changing Password: -pwd new_password')
                print("Changing bio: -bio new_bio")
                print("Adding Both/Only Bio and Post: -addpost your_post")
                print('Deleting post: -delpost post_number')
                edit_command = input("Please enter edit command: ").strip()
                if edit_command:
                    edit_profile(profile, profile_path, shlex.split(edit_command)) 
                else:
                    print('ERROR: Edit command cannot be empty.')  
            else:
                print('ERROR: No profile is loaded.')
                
        elif user_command.upper() == 'P': # print_profile
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
                    print_profile(profile, shlex.split(printing_command) )
                else:
                    print('ERROR: Print command cannot be empty.')
            else:
                print('ERROR: Profile not printed')
            
        elif user_command.upper() == 'Q':
            print('Thank you for using the DSU Profile Manager Application!')
            break
            
        else:
            print('ERROR: Invalid command. Please enter valid command.')
            

if __name__ == '__main__':
    main()
    