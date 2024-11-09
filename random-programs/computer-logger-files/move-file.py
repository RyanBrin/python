import shutil
import getpass
import os

def moveLogs():
    username = getpass.getuser()
    source_path = "C:/Users/" + username + "/OneDrive/Programming/Python/computerLogger/logs.txt"
    destination_path = "C:/Users/" + username + "/Desktop"

    if os.path.exists(source_path):
        shutil.move(source_path, destination_path)
        print("logs.txt moved to " + destination_path)
    else:
        print("logs.txt not found")

moveLogs()