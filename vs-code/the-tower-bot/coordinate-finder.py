# Coordinate Finder
# Ryan Brinkman
# 3/27/2026

# main
import ctypes
import time
import keyboard

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse_pos():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

print("Coordinate grabber started.")
print("Press F8 to print current mouse position.")
print("Press ESC to quit.\n")

while True:
    if keyboard.is_pressed("f8"):
        x, y = get_mouse_pos()
        print(f"X={x}, Y={y}")
        time.sleep(0.25)  # prevents spam

    if keyboard.is_pressed("esc"):
        print("Exiting.")
        break

    time.sleep(0.02)