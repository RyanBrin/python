# The Tower Bot
# Ryan Brinkman
# 3/27/2026

# main
import time
import subprocess
import pyautogui

pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True

APPS_BUTTON = (589, 6309)
SEARCH_BAR = (2252, 1556)
FIRST_RESULT = (2236, 1983)

def click_and_wait(point, label, wait_time=1.5):
    print(f"[INFO] {label} at {point}")
    pyautogui.click(point[0], point[1])
    time.sleep(wait_time)

subprocess.Popen(
    'explorer.exe shell:AppsFolder\\Microsoft.YourPhone_8wekyb3d8bbwe!App',
    shell=True
)

time.sleep(6)
click_and_wait(APPS_BUTTON, "Clicking Apps", 2.0)
click_and_wait(SEARCH_BAR, "Clicking search bar", 1.0)

pyautogui.hotkey("ctrl", "a")
time.sleep(0.1)
pyautogui.press("backspace")
time.sleep(0.2)

pyautogui.write("The Tower", interval=0.03)
time.sleep(1.0)

click_and_wait(FIRST_RESULT, "Clicking first result", 1.0)

print("[DONE]")