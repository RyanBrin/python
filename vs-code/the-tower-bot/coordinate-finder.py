# Coordinate Finder
# Ryan Brinkman
# 3/27/2026

# main
import pyautogui
import time
import win

print("Hover over target. Press Ctrl+C when ready.\n")

print(win.left, win.top)

try:
    while True:
        x, y = pyautogui.position()
        print(f"X={x} Y={y}", end="\r")
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nDone.")