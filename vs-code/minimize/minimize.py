# Ryan Brinkman
# Minimize
# Page None
# 3/26/23

# imports
import os
from sys import platform
import time
import pyautogui
import keyboard

# variables
os_name = ""
doMinimize = True

# obtain information about the operating system
if platform == "win32" or platform == "win64":
    os_name = "Windows"
elif platform == "linux":
    os_name = "Linux"
elif platform == "darwin":
    os_name = "Mac OS"
else: 
    print("Unsure of OS; Assuming OS is Windows")
    os_name = "Windows"

# function to minimize user applications
def windows():
    print("Windows")
    while doMinimize:
        pyautogui.hotkey('win', 'm')
        if keyboard.is_pressed('shift+alt+s'):
            print("Admin Shutdown Initialized")
            break

def linux():
    print("Linux")
    while doMinimize:
        pyautogui.hotkey('ctrl', 'alt', 'd')
        if keyboard.is_pressed('shift+alt+s'):
            print("Admin Shutdown Initialized")
            break

def mac_os():
    print("Mac OS")
    while doMinimize:
        pyautogui.hotkey('command', 'm')
        if keyboard.is_pressed('shift+alt+s'):
            print("Admin Shutdown Initialized")
            break

# match os name
if os_name == "Windows":
    windows()
elif os_name == "Linux":
    linux()
elif os_name == "Mac OS":
    mac_os()
else:
    print("Error: OS not supported")