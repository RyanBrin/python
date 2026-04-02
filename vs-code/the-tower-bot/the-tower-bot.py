"""
Project: The Tower Bot
Author: Ryan Brinkman
Date: April 1, 2026
GitHub Repository: https://github.com/RyanBrin/python/tree/main/vs-code/the-tower-bot/
"""

import time
import subprocess
import ctypes
from ctypes import wintypes
import threading

import pyautogui
import pygetwindow as gw
import keyboard

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

pyautogui.PAUSE = 0.03
pyautogui.FAILSAFE = True

PHONE_LINK_TITLE = "Phone Link"
GAME_TITLE = "The Tower"
STOP_KEY = "f8"

running = True
last_focus_time = 0.0
FOCUS_COOLDOWN = 1.0

# Phone Link
APPS_BUTTON = (587, 62)
SEARCH_BAR = (2255, 155)
FIRST_RESULT = (2238, 199)

# Game clicks based on the live client area
REL = {
    "dismiss_popup_blank": (0.18, 0.22),
    "home_resume_battle": (0.50, 0.825),
    "ad_gem": (0.089, 0.581),

    "attack_tab": (0.128, 0.965),
    "defense_tab": (0.370, 0.965),

    # working loop buttons
    "health_buy": (0.345, 0.785),
    "damage_buy": (0.345, 0.785),

    # stored upgrade button positions for later automation
    "attack_left_top": (0.369, 0.766),      # Damage
    "attack_right_top": (0.850, 0.767),     # Attack Speed
    "attack_left_mid": (0.366, 0.854),      # Critical Chance
    "attack_right_mid": (0.865, 0.852),     # Critical Factor
    "attack_left_bottom": (0.362, 0.945),   # Range
    "attack_right_bottom": (0.858, 0.939),  # Damage / Meter

    "defense_left_top": (0.369, 0.766),      # Health
    "defense_right_top": (0.850, 0.767),     # Health Regen
    "defense_left_mid": (0.366, 0.854),      # Defense %
    "defense_right_mid": (0.865, 0.852),     # Defense Absolute
    "defense_left_bottom": (0.362, 0.945),   # Thorn Damage
    "defense_right_bottom": (0.858, 0.939),  # Lifesteal

    "utility_left_top": (0.369, 0.766),      # Cash Bonus
    "utility_right_top": (0.850, 0.767),     # Cash / Wave
    "utility_left_mid": (0.366, 0.854),      # Coins / Kill Bonus
    "utility_right_mid": (0.865, 0.852),     # Coins / Wave
    "utility_left_bottom": (0.362, 0.945),   # Free Attack Upgrade
    "utility_right_bottom": (0.858, 0.939),  # Free Defense Upgrade
}

PHONE_LINK_LOAD_TIME = 2.3
SEARCH_RESULTS_LOAD_TIME = 1.5
GAME_LOAD_TIME = 9.0
POST_DISMISS_WAIT = 1.15
POST_RESUME_WAIT = 4.0
LOOP_WAIT = 0.08
AD_GEM_CHECK_INTERVAL = 0.7


def stop_listener():
    global running
    keyboard.wait(STOP_KEY)
    running = False
    print(f"[STOP] {STOP_KEY.upper()} pressed")


def check_running():
    return running


def get_exact_window(title):
    for win in gw.getAllWindows():
        try:
            if win.title.strip() == title:
                return win
        except Exception:
            pass
    return None


def get_active_window_title():
    try:
        active = gw.getActiveWindow()
        return active.title.strip() if active and getattr(active, "title", None) else ""
    except Exception:
        return ""


def wait_for_exact_window(title, timeout=20.0, poll=0.2):
    start = time.time()
    while time.time() - start < timeout:
        if not check_running():
            return None
        win = get_exact_window(title)
        if win:
            return win
        time.sleep(poll)
    return None


def focus_window(win):
    if not win:
        return False
    try:
        hwnd = win._hWnd
        ctypes.windll.user32.ShowWindow(hwnd, 9)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.2)
        return True
    except Exception:
        return False


def maximize_window(win):
    if not win:
        return False
    try:
        ctypes.windll.user32.ShowWindow(win._hWnd, 3)
        time.sleep(0.12)
        return True
    except Exception:
        return False


def ensure_game_focused():
    global last_focus_time

    if get_active_window_title() == GAME_TITLE:
        return True

    now = time.time()
    if now - last_focus_time < FOCUS_COOLDOWN:
        return False

    win = get_exact_window(GAME_TITLE)
    if not win:
        return False

    last_focus_time = now
    return focus_window(win)


def get_client_rect_screen(win):
    rect = wintypes.RECT()
    ctypes.windll.user32.GetClientRect(win._hWnd, ctypes.byref(rect))
    pt = wintypes.POINT(rect.left, rect.top)
    ctypes.windll.user32.ClientToScreen(win._hWnd, ctypes.byref(pt))
    return pt.x, pt.y, rect.right - rect.left, rect.bottom - rect.top


def game_rect():
    win = get_exact_window(GAME_TITLE)
    if not win:
        return None
    return get_client_rect_screen(win)


def game_point(name):
    rect = game_rect()
    if not rect:
        return None

    left, top, width, height = rect
    rx, ry = REL[name]
    return int(left + rx * width), int(top + ry * height)


def click_abs(point, wait=0.25, label=""):
    if not check_running():
        return False

    if label:
        print(f"[CLICK] {label}: {point}")

    pyautogui.click(point[0], point[1])
    time.sleep(wait)
    return True


def click_game(name, wait=0.25, label=""):
    point = game_point(name)
    if not point:
        print(f"[ERROR] Could not get point for {name}")
        return False

    if not ensure_game_focused():
        print("[ERROR] Game is not focused")
        return False

    return click_abs(point, wait=wait, label=label or name)


def open_game():
    print("[INFO] Launching Phone Link...")
    subprocess.Popen(
        r'explorer.exe shell:AppsFolder\Microsoft.YourPhone_8wekyb3d8bbwe!App',
        shell=True
    )

    phone = wait_for_exact_window(PHONE_LINK_TITLE, 20)
    if not phone:
        print("[ERROR] Phone Link not found")
        return False

    focus_window(phone)
    maximize_window(phone)

    print("[INFO] Waiting for Phone Link...")
    time.sleep(PHONE_LINK_LOAD_TIME)

    click_abs(APPS_BUTTON, 0.55, "Apps")
    click_abs(SEARCH_BAR, 0.25, "Search")
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.04)
    pyautogui.press("backspace")
    time.sleep(0.05)
    pyautogui.write("The Tower", interval=0.016)
    time.sleep(SEARCH_RESULTS_LOAD_TIME)
    pyautogui.press("enter")
    time.sleep(1.2)

    if not get_exact_window(GAME_TITLE):
        click_abs(FIRST_RESULT, 0.8, "First result")

    return True


def wait_for_game_ready():
    print("[INFO] Waiting for game window...")
    game = wait_for_exact_window(GAME_TITLE, 25)
    if not game:
        print("[ERROR] Game not found")
        return False

    focus_window(game)
    maximize_window(game)

    print("[INFO] Letting the game load...")
    time.sleep(GAME_LOAD_TIME)
    return True


def close_popup_and_resume():
    print("[INFO] Closing popup...")
    click_game("dismiss_popup_blank", wait=0.28, label="Dismiss popup")

    print("[INFO] Waiting before Resume Battle...")
    time.sleep(POST_DISMISS_WAIT)

    print("[INFO] Clicking Resume Battle...")
    click_game("home_resume_battle", wait=0.75, label="Resume Battle")

    print("[INFO] Waiting for run to come back...")
    time.sleep(POST_RESUME_WAIT)
    return True


def open_defense():
    return click_game("defense_tab", wait=0.16, label="Defense tab")


def open_attack():
    return click_game("attack_tab", wait=0.16, label="Attack tab")


def try_ad_gem():
    return click_game("ad_gem", wait=0.05, label="Ad gem")


def basic_upgrade_loop():
    print("[INFO] Starting loop...")
    last_ad_gem_time = 0.0

    while check_running():
        now = time.time()
        if now - last_ad_gem_time >= AD_GEM_CHECK_INTERVAL:
            try_ad_gem()
            last_ad_gem_time = now

        open_defense()
        click_game("health_buy", wait=0.05, label="Health buy")
        time.sleep(LOOP_WAIT)

        now = time.time()
        if now - last_ad_gem_time >= AD_GEM_CHECK_INTERVAL:
            try_ad_gem()
            last_ad_gem_time = now

        open_attack()
        click_game("damage_buy", wait=0.05, label="Damage buy")
        time.sleep(LOOP_WAIT)


def main():
    print(f"[INFO] Press {STOP_KEY.upper()} to stop")

    if not open_game():
        return

    if not wait_for_game_ready():
        return

    close_popup_and_resume()
    basic_upgrade_loop()


if __name__ == "__main__":
    threading.Thread(target=stop_listener, daemon=True).start()
    main()
