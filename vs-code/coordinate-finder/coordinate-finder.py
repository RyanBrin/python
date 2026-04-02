"""
Project: Coordinate Finder
Author: Ryan Brinkman
Date: April 1, 2026
GitHub Repository: https://github.com/RyanBrin/python/tree/main/vs-code/coordinate-finder/
"""

import ctypes
from ctypes import wintypes
import time
import keyboard
import pygetwindow as gw

WINDOW_TITLE = "The Tower"
PRINT_KEY = "f8"
QUIT_KEY = "esc"


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_mouse_pos():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def get_exact_window(title):
    for win in gw.getAllWindows():
        try:
            if win.title.strip() == title:
                return win
        except Exception:
            pass
    return None


def get_client_rect_screen(win):
    rect = wintypes.RECT()
    ctypes.windll.user32.GetClientRect(win._hWnd, ctypes.byref(rect))
    pt = wintypes.POINT(rect.left, rect.top)
    ctypes.windll.user32.ClientToScreen(win._hWnd, ctypes.byref(pt))
    return pt.x, pt.y, rect.right - rect.left, rect.bottom - rect.top


def get_relative_data(x, y):
    win = get_exact_window(WINDOW_TITLE)
    if not win:
        return None

    left, top, width, height = get_client_rect_screen(win)

    inside = left <= x <= left + width and top <= y <= top + height
    if not inside:
        return {
            "inside": False,
            "left": left,
            "top": top,
            "width": width,
            "height": height,
        }

    rel_x = (x - left) / width
    rel_y = (y - top) / height

    return {
        "inside": True,
        "left": left,
        "top": top,
        "width": width,
        "height": height,
        "local_x": x - left,
        "local_y": y - top,
        "rel_x": rel_x,
        "rel_y": rel_y,
    }


print("Coordinate finder started.")
print(f"Press {PRINT_KEY.upper()} to print current mouse position.")
print(f"Press {QUIT_KEY.upper()} to quit.\n")

while True:
    if keyboard.is_pressed(PRINT_KEY):
        x, y = get_mouse_pos()
        data = get_relative_data(x, y)

        print("-" * 50)
        print(f"Screen: X={x}, Y={y}")

        if data is None:
            print(f'Window "{WINDOW_TITLE}" not found.')
        else:
            print(f'Client Rect: left={data["left"]}, top={data["top"]}, width={data["width"]}, height={data["height"]}')
            if data["inside"]:
                print(f'Local: X={data["local_x"]}, Y={data["local_y"]}')
                print(f'Relative: ("name": ({data["rel_x"]:.3f}, {data["rel_y"]:.3f}))')
            else:
                print(f'Mouse is outside "{WINDOW_TITLE}" client area.')

        time.sleep(0.25)

    if keyboard.is_pressed(QUIT_KEY):
        print("Exiting.")
        break

    time.sleep(0.02)
