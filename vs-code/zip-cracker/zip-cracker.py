"""
Project: Zip Cracker
Author: Ryan Brinkman
Date: February 14, 2025
GitHub Repository: https://github.com/RyanBrin/java/tree/main/intellij/zip-cracker/
"""

import zipfile
from pathlib import Path

passwords = []

def crack_zip(zip_file, password):
    """Attempts to crack the password of a ZIP file."""
    try:
        zip_file.extractall(pwd=password.encode())
        print(f"Password found: {password}")
        return True
    except Exception as e:
        return False
    
def get_zip_file():
    """Prompts the user to enter the ZIP file path."""
    zip_file_path = input("Enter the path to the ZIP file: ").strip()
    return zip_file_path

def get_wordlist_file():
    """Prompts the user to enter the wordlist file path."""
    wordlist_path = input("Enter the path to the wordlist file: ").strip()
    return wordlist_path

def load_wordlist(wordlist_file):
    """Loads a wordlist file into memory."""
    with open(wordlist_file, "r") as file:
        for line in file:
            passwords.append(line.strip())

def main():
    zip_file_path = get_zip_file()
    wordlist_file = get_wordlist_file()
    load_wordlist(wordlist_file)
    
    zip_file = zipfile.ZipFile(zip_file_path)
    
    for password in passwords:
        if crack_zip(zip_file, password):
            break
    else:
        print("Password not found.")

if __name__ == "__main__":
    main()