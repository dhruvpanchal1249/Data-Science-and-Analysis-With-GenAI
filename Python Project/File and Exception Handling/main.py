from pathlib import Path
import os

def create_folder():
    try:
        name= input("Enter the name of the folder: ")
        p=Path(name)
        p.mkdir()
        print("Folder created successfully")
    except Exception as e:
        print(f"Sorry an error occured as {e}")


def read_file_folder():
    p=Path("") #the empty string here takes the path of the current folder where the main.py is present
    items = list(p.rglob('*'))
    for i,v in enumerate(items):
        print(f"{i+1} : {v} ")  

def update_folder():
    try:
        read_file_folder()
        old_name = input("please enter the folder name you want to update: ")
        p = Path(old_name)
        if p.exists() and p.is_dir():
            new_name = input("please enter the new folder name: ")
            new_p = Path(new_name)
            p.rename(new_p)
            print("Folder updated successfully")
        else:
            print("Folder not found")
    except Exception as e:
        print(f"Sorry an error occured as {e}")
    
def delete_folder():
    try:
        read_file_folder()
        name = input("please enter the folder name you want to delete: ")
        p = Path(name)
        if p.exists() and p.is_dir():
            p.rmdir()
            print("Folder deleted successfully")
        else:
            print("Folder not found")
    except Exception as e:
        print(f"Sorry an error occured as {e}")
def create_file():
    try:
        read_file_folder()
        name=input("please enter the file name you want to create: ")   
        p=Path(name)
        if p.exists():
            print("This file already exists")
        else:
            with open(name, 'w') as f:
                data=input("please enter the data you want to write in the file: ")
                f.write(data)
            print("File created successfully")
    except Exception as e:
        print(f"Sorry an error occured as {e}")
            
def read_file():
    try:
        read_file_folder()
        name=input("please enter the file name you want to read: ")   
        p=Path(name)
        if p.exists() and p.is_file():
            with open(name, 'r') as f:
                data=f.read()
                print(f"Data in the file is: {data}")
        else:
            print("File not found")
    except Exception as e:
        print(f"Sorry an error occured as {e}")

def update_file():
    try:
        read_file_folder()
        name=input("please enter the file name you want to update: ")
        p=Path(name)
        if p.exists() and p.is_file():
            print("Options for updating the file:")
            print("1. Update the content")
            print("2. Update the file name")
            option = int(input("Please select an option: "))
            if option == 1:
                with open(name, 'w') as f:
                    data = input("Please enter the new content: ")
                    f.write(data)
                print("File updated successfully")
            elif option == 2:
                new_name = input("Please enter the new file name: ")
                new_p = Path(new_name)
                if not new_p.exists():
                    p.rename(new_p)
                    print("File name updated successfully")
                else:
                    print("A file with that name already exists")
        else:
            print("File not found")
    except Exception as e:
        print(f"Sorry an error occurred as {e}")

def delete_file():
    try:
        read_file_folder()
        name=input("please enter the file name you want to delete: ")   
        p=Path(name)
        if p.exists() and p.is_file():
            os.remove(name)
            print("File deleted successfully")
        else:
            print("File not found")
    except Exception as e:
        print(f"Sorry an error occured as {e}")


print("Options")

print("1. Create a Folder")
print("2. Read files and Folder")
print("3. Update Folder")
print("4. Delete Folder")
print("5. Create a file")
print("6. Read a file")
print("7. Update a file")
print("8. Delete a file")

choice = int(input("Please select one option: "))

if choice==1:
    create_folder()
if choice==2:
    read_file_folder()
if choice==3:
    update_folder()
if choice==4:
    delete_folder()
if choice==5:
    create_file()
if choice==6:
    read_file()
if choice==7:
    update_file()
if choice==8:
    delete_file()