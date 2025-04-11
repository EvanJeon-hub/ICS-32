
# ICS 32 Assignment 1
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

import pathlib
import shlex

def create_file(directory, filename): #Command C
    dir_path = pathlib.Path(directory) # create a path object
    if not dir_path.is_dir(): # if directory does not exist
        print("ERROR")
        return
    file_path = dir_path / f"{filename}.dsu" # create a file path with dsu extensio
    if file_path.exists(): # if file already exists
        print("ERROR")
    else:
        try:
            file_path.touch(exist_ok=False) # touch creates a file
            print(file_path)
        except Exception:
            print("ERROR")

def delete_file(filepath): #Command D
    path = pathlib.Path(filepath)
    if not path.exists() or not path.is_file() or not path.suffix == '.dsu': 
        print("ERROR")
    else:
        try:
            path.unlink() # unlink deletes a file
            print(f"{path} DELETED")
        except Exception:
            print("ERROR")

def read_file(filepath): #command R
    path = pathlib.Path(filepath)
    if not path.exists() or not path.is_file() or not path.suffix == '.dsu':
        print("ERROR")
    else:
        try:
            content = path.read_text().strip() # read_text reads the context of the file - pathlib built in function
            if content == "":
                print("EMPTY")
            else:
                print(content)
        except Exception:
            print("ERROR")
    
def main():
    while True:
        input_command = input().strip()
        if input_command.upper() == "Q":
            break
        try:
            token = shlex.split(input_command) # shlex split the input command into tokens by whitespaces
            if not token:
                print('ERROR')
                continue
            
            command = token[0].upper()
            
            if command == "C":
                if len(token) == 4 and token[2] == "-n": # if the length of the token is 4 and the third token is -n
                    directory = token[1]
                    filename = token[3]
                    create_file(directory, filename)
                else:
                    print('ERROR')
                    
            elif command == 'D':
                if len(token) == 2:
                    filepath = token[1]
                    delete_file(filepath)
                else:
                    print('ERROR')
                    
            elif command == 'R':
                if len(token) == 2:
                    filepath = token[1]
                    read_file(filepath) 
                else:
                    print('ERROR')
            else:
                print('ERROR')
        except Exception:
            print('ERROR')   

if __name__ == "__main__":         
    main()