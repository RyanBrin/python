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
from pathlib import Path
from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk

import pyautogui
import pygetwindow as gw
import keyboard

try:
    import cv2
    OPENCV_AVAILABLE = True
except Exception:
    OPENCV_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except Exception:
    NUMPY_AVAILABLE = False

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

pyautogui.PAUSE = 0.02
pyautogui.FAILSAFE = True

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


PHONE_LINK_TITLE = "Phone Link"
GAME_TITLE = "The Tower"
BOT_WINDOW_TITLE = "The Tower Bot"
STOP_KEY = "f8"
MENU_TOGGLE_KEY = "f7"
REFRESH_VISION_KEY = "f6"

PHONE_LINK_LOAD_TIME = 4.8
SEARCH_RESULTS_LOAD_TIME = 2.0
GAME_LOAD_TIME = 8.5
RESUME_TRANSITION_TIME = 1.0
HOME_TRANSITION_TIME = 1.0
TAB_WAIT = 0.14
UPGRADE_CLICK_WAIT = 0.06
TIER_CLICK_WAIT = 0.16
DRAG_TIME = 0.20
FOCUS_RETRY_COOLDOWN = 0.7
VISION_REFRESH_INTERVAL = 0.18
AUTO_DEBUG_SNAPSHOT_INTERVAL = 2.5

TARGET_TIER_DEFAULT = 9
TEMPLATE_CONFIDENCE = 0.60
AD_GEM_CHECK_INTERVAL = 1.0
AD_GEM_COOLDOWN_SECONDS = 600.0
FLYING_GEM_CHECK_INTERVAL = 0.08

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
DEBUG_DIR = BASE_DIR / "debug"
DEBUG_DIR.mkdir(parents=True, exist_ok=True)
AD_GEM_TEMPLATE = ASSET_DIR / "ad-gem-button.png"
FLYING_GEM_TEMPLATE = ASSET_DIR / "flying-gem.png"
RESUME_TEMPLATE = ASSET_DIR / "resume-button.png"
DEATH_TEMPLATE = ASSET_DIR / "death-screen.png"
TIER_9_TEMPLATE = ASSET_DIR / "tier-9.png"

running = False
worker_thread = None
last_ad_gem_check = 0.0
last_ad_gem_collect = 0.0
last_flying_gem_check = 0.0
last_focus_attempt = 0.0
last_locator_refresh = 0.0
last_debug_snapshot = 0.0
GUI = None

REL = {
    "menu_btn": (0.924, 0.080),
    "resume_btn": (0.732, 0.615),
    "resume_battle_btn": (0.502, 0.826),
    "attack_tab": (0.120, 0.964),
    "defense_tab": (0.372, 0.964),
    "utility_tab": (0.626, 0.971),
    "ultimate_tab": (0.877, 0.970),
    "tier_minus": (0.356, 0.571),
    "tier_plus": (0.642, 0.571),
    "start_battle": (0.502, 0.826),
    "retry": (0.334, 0.642),
    "home": (0.668, 0.642),
}

RESUME_REGION = (0.16, 0.18, 0.70, 0.52)
TIER_LABEL_REGION = (0.22, 0.46, 0.58, 0.18)
AD_GEM_REGION = (0.02, 0.57, 0.24, 0.14)
FLYING_GEM_REGION = (0.00, 0.02, 1.00, 0.70)

OVERLAY_BG = "#ff00ff"
CLICK_RING_COLOR = "#ffd400"
LOCATOR_RING_COLOR = "#44d6ff"
LOCATOR_TEXT_COLOR = "#ffe066"
CLICK_RING_LIFETIME = 0.45
CLICK_RING_MAX_RADIUS = 28

class FeatureFlags:
    def __init__(self):
        self.lock = threading.Lock()
        self.auto_buy = True
        self.auto_ad_gems = True
        self.auto_flying_gems = True
        self.auto_resume = True
        self.live_locator = True
        self.auto_debug_snapshots = True
        self.show_game_overlay = False
        self.show_click_highlights = True
    def set_flag(self, name, value):
        with self.lock:
            setattr(self, name, bool(value))
    def get(self, name):
        with self.lock:
            return getattr(self, name)

FLAGS = FeatureFlags()

class BotState:
    def __init__(self):
        self.lock = threading.Lock()
        self.phase = "Idle"
        self.detail = "Press Start in the GUI"
        self.current_tab = "None"
        self.last_event = "None"
        self.last_decision = "None"
        self.strategy = "Vision Guided"
        self.health_clicks = 0
        self.damage_clicks = 0
        self.utility_clicks = 0
        self.flying_gems_clicked = 0
        self.ad_gems_collected = 0
        self.loop_cycles = 0
        self.last_ad_gem_collect = 0.0
        self.started_at = time.time()
        self.window_status = "Unknown"
        self.game_window_size = "Unknown"
        self.target_tier = TARGET_TIER_DEFAULT
        self.menu_open = False
        self.vision_status = "Waiting"
        self.detected_count = 0
        self.last_refresh_age = 0.0
    def reset_run_stats(self):
        with self.lock:
            self.phase = "Idle"
            self.detail = "Run starting"
            self.current_tab = "None"
            self.last_event = "None"
            self.last_decision = "None"
            self.strategy = "Vision Guided"
            self.health_clicks = 0
            self.damage_clicks = 0
            self.utility_clicks = 0
            self.flying_gems_clicked = 0
            self.ad_gems_collected = 0
            self.loop_cycles = 0
            self.last_ad_gem_collect = 0.0
            self.started_at = time.time()
            self.window_status = "Unknown"
            self.game_window_size = "Unknown"
            self.target_tier = TARGET_TIER_DEFAULT
            self.menu_open = False
            self.vision_status = "Refreshing"
            self.detected_count = 0
            self.last_refresh_age = 0.0
    def set_phase(self, phase, detail=None):
        with self.lock:
            self.phase = phase
            if detail is not None:
                self.detail = detail
    def set_tab(self, tab_name):
        with self.lock:
            self.current_tab = tab_name
    def set_window_status(self, text):
        with self.lock:
            self.window_status = text
    def set_game_window_size(self, text):
        with self.lock:
            self.game_window_size = text
    def set_strategy(self, text):
        with self.lock:
            self.strategy = text
    def set_target_tier(self, value):
        with self.lock:
            self.target_tier = int(value)
    def set_menu_open(self, value):
        with self.lock:
            self.menu_open = bool(value)
    def set_vision(self, status, count=None, refresh_age=None):
        with self.lock:
            self.vision_status = status
            if count is not None:
                self.detected_count = count
            if refresh_age is not None:
                self.last_refresh_age = refresh_age
    def event(self, text):
        with self.lock:
            self.last_event = text
            self.detail = text
    def decision(self, text):
        with self.lock:
            self.last_decision = text
    def add_health_click(self, n=1):
        with self.lock:
            self.health_clicks += n
    def add_damage_click(self, n=1):
        with self.lock:
            self.damage_clicks += n
    def add_utility_click(self, amount=1):
        with self.lock:
            self.utility_clicks += amount
    def add_flying_gem(self):
        with self.lock:
            self.flying_gems_clicked += 1
            self.last_event = "Flying gem clicked"
    def add_ad_gem(self):
        with self.lock:
            self.ad_gems_collected += 1
            self.last_ad_gem_collect = time.time()
            self.last_event = "Ad gem collected"
            self.detail = "Ad gem collected"
    def add_cycle(self):
        with self.lock:
            self.loop_cycles += 1
    def snapshot(self):
        with self.lock:
            return {
                "phase": self.phase,
                "detail": self.detail,
                "current_tab": self.current_tab,
                "last_event": self.last_event,
                "last_decision": self.last_decision,
                "strategy": self.strategy,
                "health_clicks": self.health_clicks,
                "damage_clicks": self.damage_clicks,
                "utility_clicks": self.utility_clicks,
                "flying_gems_clicked": self.flying_gems_clicked,
                "ad_gems_collected": self.ad_gems_collected,
                "loop_cycles": self.loop_cycles,
                "last_ad_gem_collect": self.last_ad_gem_collect,
                "uptime": time.time() - self.started_at,
                "window_status": self.window_status,
                "game_window_size": self.game_window_size,
                "target_tier": self.target_tier,
                "menu_open": self.menu_open,
                "vision_status": self.vision_status,
                "detected_count": self.detected_count,
                "last_refresh_age": self.last_refresh_age,
            }

BOT_STATE = BotState()

@dataclass
class Detection:
    name: str
    center: tuple[int, int]
    rect: tuple[int, int, int, int]
    score: float = 0.0
    source: str = "vision"

@dataclass
class ClickEffect:
    x: int
    y: int
    created_at: float
    label: str = ""

class RuntimeLocator:
    def __init__(self):
        self.lock = threading.Lock()
        self.points = {}
    def set_points(self, mapping):
        with self.lock:
            self.points = mapping
    def get_point(self, name):
        with self.lock:
            return self.points.get(name)
    def snapshot(self):
        with self.lock:
            return dict(self.points)

class ClickEffectStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.effects = []
    def add(self, x, y, label=""):
        with self.lock:
            self.effects.append(ClickEffect(int(x), int(y), time.time(), label))
    def get_active(self):
        now = time.time()
        with self.lock:
            self.effects = [e for e in self.effects if now - e.created_at <= CLICK_RING_LIFETIME]
            return list(self.effects)

LOCATOR = RuntimeLocator()
CLICK_EFFECTS = ClickEffectStore()

def get_exact_window(title):
    for w in gw.getAllWindows():
        try:
            if w.title.strip() == title:
                return w
        except Exception:
            pass
    return None

def get_phone_link_window(): return get_exact_window(PHONE_LINK_TITLE)
def get_game_window(): return get_exact_window(GAME_TITLE)

def get_active_window_title():
    try:
        active = gw.getActiveWindow()
        return active.title.strip() if active and getattr(active, "title", None) else ""
    except Exception:
        return ""

def focus_window(win, label="window"):
    if not win: return False
    try:
        hwnd = win._hWnd
        ctypes.windll.user32.ShowWindow(hwnd, 9)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.18)
        BOT_STATE.set_window_status(f"Focused {label}")
        return True
    except Exception:
        return False

def maximize_window(win):
    if not win: return False
    try:
        ctypes.windll.user32.ShowWindow(win._hWnd, 3)
        time.sleep(0.10)
        return True
    except Exception:
        return False

def check_running(): return running

def wait_for_exact_window(title, timeout=20.0, poll=0.20):
    start = time.time()
    while time.time() - start < timeout:
        if not check_running():
            return None
        win = get_exact_window(title)
        if win:
            return win
        time.sleep(poll)
    return None

def ensure_active_window(title):
    active = get_active_window_title()
    if active != title:
        BOT_STATE.set_window_status(f"Wrong focus: {active or 'None'}")
        return False
    BOT_STATE.set_window_status(f"Focused {title}")
    return True

def gently_focus_game():
    global last_focus_attempt
    now = time.time()
    if now - last_focus_attempt < FOCUS_RETRY_COOLDOWN:
        return ensure_active_window(GAME_TITLE)
    last_focus_attempt = now
    win = get_game_window()
    if not win:
        BOT_STATE.set_window_status("Game window not found")
        return False
    if ensure_active_window(GAME_TITLE):
        return True
    focus_window(win, "The Tower")
    maximize_window(win)
    time.sleep(0.14)
    return ensure_active_window(GAME_TITLE)

def get_client_rect_screen(win):
    rect = wintypes.RECT()
    ctypes.windll.user32.GetClientRect(win._hWnd, ctypes.byref(rect))
    pt = wintypes.POINT(rect.left, rect.top)
    ctypes.windll.user32.ClientToScreen(win._hWnd, ctypes.byref(pt))
    return pt.x, pt.y, rect.right - rect.left, rect.bottom - rect.top


def game_rect():
    win = get_game_window()
    if not win:
        return None
    left, top, width, height = get_client_rect_screen(win)
    BOT_STATE.set_game_window_size(f"{width} x {height}")
    return left, top, width, height

def abs_from_rel(name):
    rect = game_rect()
    if not rect: return None
    left, top, width, height = rect
    rx, ry = REL[name]
    return int(left + rx * width), int(top + ry * height)

def region_from_rel(rr):
    rect = game_rect()
    if not rect: return None
    left, top, width, height = rect
    rx, ry, rw, rh = rr
    return (int(left + rx * width), int(top + ry * height), int(rw * width), int(rh * height))

def screenshot_game_rgb():
    rect = game_rect()
    if not rect or not PIL_AVAILABLE: return None
    left, top, width, height = rect
    return pyautogui.screenshot(region=(left, top, width, height))

def screenshot_game_bgr():
    if not (PIL_AVAILABLE and NUMPY_AVAILABLE and OPENCV_AVAILABLE): return None
    img = screenshot_game_rgb()
    if img is None: return None
    arr = np.array(img)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

def frame_to_screen(point):
    rect = game_rect()
    if not rect: return None
    left, top, _, _ = rect
    return int(left + point[0]), int(top + point[1])

def rect_to_screen(rect_local):
    rect = game_rect()
    if not rect: return None
    left, top, _, _ = rect
    x, y, w, h = rect_local
    return (int(left + x), int(top + y), int(w), int(h))

def find_tab_bar_buttons(frame):
    h, w = frame.shape[:2]
    y0 = int(h * 0.90)
    roi = frame[y0:h, :]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for c in contours:
        x, y, ww, hh = cv2.boundingRect(c)
        if ww * hh < 900 or hh < 30:
            continue
        rects.append((x + ww // 2, x, y, ww, hh))
    rects.sort(key=lambda r: r[0])
    names = ["attack_tab", "defense_tab", "utility_tab", "ultimate_tab"]
    found = {}
    for name, r in zip(names, rects[:4]):
        cx, x, y, ww, hh = r
        center_screen = frame_to_screen((cx, y0 + y + hh // 2))
        rect_screen = rect_to_screen((x, y0 + y, ww, hh))
        if center_screen and rect_screen:
            found[name] = Detection(name, center_screen, rect_screen, source="tab_bar")
    return found

def find_upgrade_buttons(frame):
    h, w = frame.shape[:2]
    x0 = int(w * 0.08)
    y0 = int(h * 0.58)
    x1 = int(w * 0.92)
    y1 = int(h * 0.975)
    roi = frame[y0:y1, x0:x1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, (75, 18, 25), (125, 255, 255))
    mask2 = cv2.inRange(hsv, (0, 0, 115), (180, 75, 255))
    mask = cv2.bitwise_or(mask1, mask2)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    for c in contours:
        x, y, ww, hh = cv2.boundingRect(c)
        area = ww * hh
        if area < 1400 or ww < 55 or hh < 26:
            continue
        if ww > int((x1 - x0) * 0.24) or hh > int((y1 - y0) * 0.14):
            continue
        cx = x + ww // 2
        cy = y + hh // 2
        candidates.append((cy, cx, x, y, ww, hh, area))
    candidates.sort(key=lambda r: (r[0], r[1]))
    rows = []
    for item in candidates:
        cy = item[0]
        matched = False
        for row in rows:
            if abs(row["y"] - cy) < 34:
                row["items"].append(item)
                row["y"] = int((row["y"] + cy) / 2)
                matched = True
                break
        if not matched:
            rows.append({"y": cy, "items": [item]})
    rows.sort(key=lambda r: r["y"])
    rows = rows[:3]
    row_names = [("health", "health_regen"), ("def_percent", "def_abs"), ("thorns", "lifesteal")]
    found = {}
    for row_names_pair, row in zip(row_names, rows):
        items = sorted(row["items"], key=lambda r: r[1])
        if len(items) < 2:
            continue
        pair = [items[0], items[-1]]
        for name, item in zip(row_names_pair, pair):
            cy, cx, x, y, ww, hh, area = item
            click_x = x0 + x + int(ww * 0.74)
            click_y = y0 + y + hh // 2
            center_screen = frame_to_screen((click_x, click_y))
            rect_screen = rect_to_screen((x0 + x, y0 + y, ww, hh))
            if center_screen and rect_screen:
                found[name] = Detection(name, center_screen, rect_screen, score=float(area), source="upgrade_box")
    return found

def detect_runtime_points(force=False):
    global last_locator_refresh
    if not FLAGS.get("live_locator"): return LOCATOR.snapshot()
    if not OPENCV_AVAILABLE or not NUMPY_AVAILABLE or not PIL_AVAILABLE:
        BOT_STATE.set_vision("Missing OpenCV/Numpy/PIL", 0, 0.0)
        return LOCATOR.snapshot()
    now = time.time()
    if not force and now - last_locator_refresh < VISION_REFRESH_INTERVAL:
        snap = BOT_STATE.snapshot()
        BOT_STATE.set_vision(snap["vision_status"], snap["detected_count"], now - last_locator_refresh)
        return LOCATOR.snapshot()
    last_locator_refresh = now
    frame = screenshot_game_bgr()
    if frame is None:
        BOT_STATE.set_vision("No frame", 0, 0.0)
        return LOCATOR.snapshot()
    found = {}
    found.update(find_tab_bar_buttons(frame))
    found.update(find_upgrade_buttons(frame))
    for name in ["menu_btn", "resume_btn", "resume_battle_btn", "tier_minus", "tier_plus", "start_battle", "retry", "home"]:
        pt = abs_from_rel(name)
        if pt and name not in found:
            found[name] = Detection(name, pt, (pt[0]-10, pt[1]-10, 20, 20), source="fallback")
    LOCATOR.set_points(found)
    BOT_STATE.set_vision("Live", len(found), 0.0)
    maybe_save_locator_snapshot(frame)
    return found

def get_point(name):
    det = LOCATOR.get_point(name)
    if det: return det.center
    return abs_from_rel(name)

def maybe_save_locator_snapshot(frame=None):
    global last_debug_snapshot
    if not FLAGS.get("auto_debug_snapshots"): return
    now = time.time()
    if now - last_debug_snapshot < AUTO_DEBUG_SNAPSHOT_INTERVAL: return
    last_debug_snapshot = now
    save_locator_overlay(frame)

def save_locator_overlay(frame=None):
    if not PIL_AVAILABLE: return
    rect = game_rect()
    if not rect: return
    if frame is None:
        img = screenshot_game_rgb()
    else:
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if img is None: return
    draw = ImageDraw.Draw(img)
    left, top, _, _ = rect
    for name, det in LOCATOR.snapshot().items():
        x, y = det.center
        x -= left
        y -= top
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), outline="#ff4d6d", width=2)
        draw.text((x + 8, y - 8), name, fill="#ffe066")
    out = DEBUG_DIR / f"locator_{int(time.time() * 1000)}.png"
    img.save(out)
    BOT_STATE.event(f"Saved {out.name}")

@dataclass
class ScreenState:
    resume_visible: bool = False
    death_visible: bool = False
    tier_9_visible: bool = False
    ad_gem_visible: bool = False
    flying_gem_visible: bool = False
    game_window_ready: bool = False

class ScreenReader:
    def template_exists(self, path: Path) -> bool:
        return OPENCV_AVAILABLE and path.exists()
    def locate(self, path: Path, region=None, confidence=TEMPLATE_CONFIDENCE):
        if not self.template_exists(path): return None
        try:
            return pyautogui.locateOnScreen(str(path), region=region, confidence=confidence)
        except Exception:
            return None
    def visible(self, path: Path, region=None, confidence=TEMPLATE_CONFIDENCE):
        return self.locate(path, region=region, confidence=confidence) is not None
    def locate_ad_gem(self):
        region = region_from_rel(AD_GEM_REGION)
        box = self.locate(AD_GEM_TEMPLATE, region=region, confidence=0.58)
        if box: return box
        frame = screenshot_game_bgr()
        rect = game_rect()
        if frame is None or rect is None or region is None: return None
        left, top, _, _ = rect
        x, y, w, h = region
        roi = frame[y - top:y - top + h, x - left:x - left + w]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (85, 35, 55), (130, 255, 255))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        best = None
        best_area = 0
        for c in contours:
            bx, by, bw, bh = cv2.boundingRect(c)
            area = bw * bh
            if area > best_area and bw > 20 and bh > 12:
                best = (bx, by, bw, bh)
                best_area = area
        if best:
            bx, by, bw, bh = best
            return (x + bx, y + by, bw, bh)
        return None
    def locate_resume_button(self):
        return self.locate(RESUME_TEMPLATE, region=region_from_rel(RESUME_REGION), confidence=0.72)

    def locate_flying_gem(self):
        return self.locate(FLYING_GEM_TEMPLATE, region=region_from_rel(FLYING_GEM_REGION), confidence=0.58)
    def scan(self):
        return ScreenState(
            resume_visible=self.visible(RESUME_TEMPLATE, region=region_from_rel(RESUME_REGION), confidence=0.72),
            death_visible=self.visible(DEATH_TEMPLATE, confidence=0.72),
            tier_9_visible=self.visible(TIER_9_TEMPLATE, region=region_from_rel(TIER_LABEL_REGION), confidence=0.66),
            ad_gem_visible=self.locate_ad_gem() is not None,
            flying_gem_visible=self.locate_flying_gem() is not None,
            game_window_ready=get_game_window() is not None,
        )

SCREEN = ScreenReader()

def stop_bot(reason="Stopped"):
    global running
    running = False
    BOT_STATE.set_phase("Stopped", reason)
    BOT_STATE.event(reason)

def start_bot():
    global running, worker_thread
    if worker_thread and worker_thread.is_alive():
        BOT_STATE.event("Bot already running")
        return
    BOT_STATE.reset_run_stats()
    running = True
    BOT_STATE.set_phase("Starting", "Launching bot")
    worker_thread = threading.Thread(target=main, daemon=True)
    worker_thread.start()

def resume_from_button():
    global running, worker_thread
    if worker_thread and worker_thread.is_alive():
        BOT_STATE.event("Bot already running")
        return
    BOT_STATE.reset_run_stats()
    running = True
    BOT_STATE.set_phase("Resuming", "Trying to return to game")
    worker_thread = threading.Thread(target=resume_or_restart_flow, daemon=True)
    worker_thread.start()

def stop_listener():
    keyboard.wait(STOP_KEY)
    stop_bot("F8 pressed")

def menu_listener():
    keyboard.wait(MENU_TOGGLE_KEY)
    toggle_game_menu()

def refresh_listener():
    keyboard.wait(REFRESH_VISION_KEY)
    detect_runtime_points(force=True)
    save_locator_overlay()

def click(point, wait=0.3, label=None):
    if running is False and label not in {"Toggle game menu"}:
        return
    if label:
        BOT_STATE.event(label)
    if FLAGS.get("show_click_highlights"):
        CLICK_EFFECTS.add(point[0], point[1], label or "")
    pyautogui.click(point[0], point[1])
    time.sleep(wait)

def safe_phone_link_click_abs(point, wait=0.4, label=None):
    win = get_phone_link_window()
    if not win:
        BOT_STATE.event("Phone Link window missing")
        return False
    if not ensure_active_window(PHONE_LINK_TITLE):
        focus_window(win, "Phone Link")
        maximize_window(win)
        if not ensure_active_window(PHONE_LINK_TITLE):
            BOT_STATE.event("Phone Link not focused")
            return False
    click(point, wait=wait, label=label)
    return True

def safe_game_click_abs(point, wait=0.3, label=None):
    if not gently_focus_game():
        BOT_STATE.event("Game not focused")
        return False
    click(point, wait=wait, label=label)
    return True

def point_in_game_rect(point):
    rect = game_rect()
    if not rect or point is None:
        return False
    left, top, width, height = rect
    x, y = point
    return left <= x <= left + width and top <= y <= top + height


def safe_game_click(name, wait=0.3, label=None):
    detect_runtime_points(force=False)
    point = get_point(name)
    if point is None:
        BOT_STATE.event(f"No point for {name}")
        return False
    if not point_in_game_rect(point):
        BOT_STATE.event(f"Point outside game rect for {name}: {point}")
        return False
    return safe_game_click_abs(point, wait=wait, label=label)

def drag_rel(start_rx, start_ry, end_rx, end_ry, duration=DRAG_TIME):
    rect = game_rect()
    if not rect or not gently_focus_game():
        return False
    left, top, width, height = rect
    sx = int(left + start_rx * width)
    sy = int(top + start_ry * height)
    ex = int(left + end_rx * width)
    ey = int(top + end_ry * height)
    if FLAGS.get("show_click_highlights"):
        CLICK_EFFECTS.add(sx, sy, "drag start")
        CLICK_EFFECTS.add(ex, ey, "drag end")
    pyautogui.moveTo(sx, sy)
    pyautogui.mouseDown()
    pyautogui.moveTo(ex, ey, duration=duration)
    pyautogui.mouseUp()
    time.sleep(0.16)
    return True

def scroll_game_ui(start_rx, start_ry, end_rx, end_ry):
    BOT_STATE.decision("Scroll game UI")
    return drag_rel(start_rx, start_ry, end_rx, end_ry)

def open_tab(tab_name):
    mapping = {"Attack": "attack_tab", "Defense": "defense_tab", "Utility": "utility_tab", "Ultimate": "ultimate_tab"}
    if safe_game_click(mapping[tab_name], wait=TAB_WAIT, label=f"{tab_name} tab"):
        BOT_STATE.set_tab(tab_name)
        return True
    return False

def toggle_game_menu():
    if safe_game_click("menu_btn", wait=0.20, label="Toggle game menu"):
        snap = BOT_STATE.snapshot()
        BOT_STATE.set_menu_open(not snap["menu_open"])
        return True
    return False

def ad_gem_ready():
    if last_ad_gem_collect == 0:
        return True
    return (time.time() - last_ad_gem_collect) >= AD_GEM_COOLDOWN_SECONDS

def decide_next_action(screen: ScreenState):
    if FLAGS.get("auto_resume"):
        if screen.death_visible:
            return "death_home"
        if screen.resume_visible:
            return "resume_popup"
    if FLAGS.get("auto_ad_gems") and screen.ad_gem_visible and ad_gem_ready():
        return "collect_ad_gem"
    if FLAGS.get("auto_flying_gems") and screen.flying_gem_visible:
        return "collect_flying_gem"
    if FLAGS.get("auto_buy"):
        return "upgrade_cycle"
    return "idle"

def ensure_game_window_ready():
    win = get_game_window()
    if not win:
        BOT_STATE.set_window_status("Game window not found")
        stop_bot("Game window missing")
        return None
    if getattr(win, "isMinimized", False):
        BOT_STATE.set_window_status("Game minimized")
        stop_bot("Game minimized")
        return None
    if not gently_focus_game():
        stop_bot("Game lost focus")
        return None
    BOT_STATE.set_window_status("Focused and active")
    return win

def handle_resume():
    BOT_STATE.set_phase("Resuming Run", "Resume detected")
    BOT_STATE.decision("Click popup Resume")
    box = SCREEN.locate_resume_button()
    if box:
        center = pyautogui.center(box)
        safe_game_click_abs((center.x, center.y), wait=0.08, label="Popup Resume")
        time.sleep(RESUME_TRANSITION_TIME)
        BOT_STATE.event("Resume completed")
        return True

    for _ in range(6):
        if not check_running():
            return False
        safe_game_click("resume_btn", wait=0.10, label="Fallback Resume")
    time.sleep(RESUME_TRANSITION_TIME)
    BOT_STATE.event("Resume completed")
    return True

def handle_home_resume_battle():
    BOT_STATE.set_phase("Resuming Run", "Trying home Resume Battle")
    BOT_STATE.decision("Click Resume Battle")
    safe_game_click("resume_battle_btn", wait=0.80, label="Clicking Resume Battle")
    time.sleep(RESUME_TRANSITION_TIME)
    return True

def handle_death_screen():
    BOT_STATE.set_phase("Death Screen", "Run ended, returning home")
    BOT_STATE.decision("Return home from death screen")
    safe_game_click("home", wait=HOME_TRANSITION_TIME, label="Clicking Home")
    return True

def try_collect_home_ad_gem():
    BOT_STATE.event("Checking home ad gem")
    box = SCREEN.locate_ad_gem()
    if box:
        x, y, w, h = box
        safe_game_click_abs((x + w // 2, y + h // 2), wait=0.12, label="Home ad gem")

def ensure_tier_selected(max_attempts=18):
    target = BOT_STATE.snapshot()["target_tier"]
    if target == 9 and not SCREEN.template_exists(TIER_9_TEMPLATE):
        BOT_STATE.set_phase("Error", "tier-9.png missing")
        return False
    BOT_STATE.set_phase("Selecting Tier", f"Verifying Tier {target}")
    BOT_STATE.decision(f"Verify Tier {target}")
    for _ in range(max_attempts):
        if not check_running():
            return False
        if target == 9 and SCREEN.visible(TIER_9_TEMPLATE, region=region_from_rel(TIER_LABEL_REGION), confidence=0.66):
            BOT_STATE.event("Tier 9 confirmed")
            return True
        safe_game_click("tier_plus", wait=TIER_CLICK_WAIT)
    BOT_STATE.set_phase("Error", f"Could not verify Tier {target}")
    return False

def start_target_run():
    target = BOT_STATE.snapshot()["target_tier"]
    BOT_STATE.set_phase("Starting Run", f"Preparing Tier {target}")
    BOT_STATE.decision(f"Start fresh Tier {target} run")
    try_collect_home_ad_gem()
    if not ensure_tier_selected():
        return False
    safe_game_click("start_battle", wait=1.20, label="Starting battle")
    BOT_STATE.event(f"Tier {target} battle started")
    return True

def resume_or_start_tier_inner():
    screen = SCREEN.scan()
    if screen.death_visible:
        handle_death_screen()
        return start_target_run()
    if screen.resume_visible:
        return handle_resume()
    handle_home_resume_battle()
    time.sleep(0.7)
    screen = SCREEN.scan()
    if screen.resume_visible:
        return handle_resume()
    if get_game_window() and not screen.death_visible:
        BOT_STATE.event("Continuing active run")
        return True
    return start_target_run()

def try_collect_ad_gem():
    global last_ad_gem_check, last_ad_gem_collect
    now = time.time()
    if now - last_ad_gem_check < AD_GEM_CHECK_INTERVAL: return False
    last_ad_gem_check = now
    if last_ad_gem_collect and (now - last_ad_gem_collect) < AD_GEM_COOLDOWN_SECONDS: return False
    box = SCREEN.locate_ad_gem()
    if box:
        x, y, w, h = box
        BOT_STATE.decision("Collect ad gem")
        if safe_game_click_abs((x + w // 2, y + h // 2), wait=0.12, label="Ad gem detected"):
            last_ad_gem_collect = now
            BOT_STATE.add_ad_gem()
            return True
    return False

def try_collect_flying_gem():
    global last_flying_gem_check
    now = time.time()
    if now - last_flying_gem_check < FLYING_GEM_CHECK_INTERVAL: return False
    last_flying_gem_check = now
    box = SCREEN.locate_flying_gem()
    if box:
        center = pyautogui.center(box)
        BOT_STATE.decision("Track and click flying gem")
        if safe_game_click_abs((center.x, center.y), wait=0.02, label="Flying gem"):
            BOT_STATE.add_flying_gem()
            return True
    return False

def opportunistic_gem_checks():
    if not check_running(): return
    if FLAGS.get("auto_flying_gems"): try_collect_flying_gem()
    if FLAGS.get("auto_ad_gems"): try_collect_ad_gem()

def click_slot_multiple(name, count, wait=UPGRADE_CLICK_WAIT):
    for _ in range(count):
        if not check_running() or not ensure_game_window_ready():
            return False
        safe_game_click(name, wait=wait, label=name)
    return True

def early_game_upgrade_pass():
    BOT_STATE.set_strategy("Vision Guided Early")
    if open_tab("Defense"):
        BOT_STATE.decision("Cheap defense first")
        click_slot_multiple("health_regen", 3)
        click_slot_multiple("def_abs", 3)
        click_slot_multiple("health", 2)
        BOT_STATE.add_utility_click(6)
        BOT_STATE.add_health_click(2)
    opportunistic_gem_checks()
    return True

def core_upgrade_pass():
    BOT_STATE.set_strategy("Vision Guided Core")
    if open_tab("Defense"):
        BOT_STATE.decision("Health focus")
        click_slot_multiple("health", 3)
        BOT_STATE.add_health_click(3)
    opportunistic_gem_checks()
    return True

def upgrade_cycle():
    cycle = BOT_STATE.snapshot()["loop_cycles"]
    return early_game_upgrade_pass() if cycle < 30 else core_upgrade_pass()

def launch_phone_link_if_needed():
    win = get_phone_link_window()
    if win:
        focus_window(win, "Phone Link")
        maximize_window(win)
        return True
    BOT_STATE.decision("Launch Phone Link")
    subprocess.Popen(r'explorer.exe shell:AppsFolder\Microsoft.YourPhone_8wekyb3d8bbwe!App', shell=True)
    win = wait_for_exact_window(PHONE_LINK_TITLE, timeout=20.0)
    if not win:
        BOT_STATE.set_phase("Error", "Phone Link not found")
        return False
    focus_window(win, "Phone Link")
    maximize_window(win)
    time.sleep(PHONE_LINK_LOAD_TIME)
    return True

def open_game_from_phone_link():
    BOT_STATE.set_phase("Launching", "Opening game from Phone Link")
    if not launch_phone_link_if_needed(): return False
    if not safe_phone_link_click_abs((587, 62), wait=0.8, label="Clicking Apps"): return False
    if not safe_phone_link_click_abs((2255, 155), wait=0.45, label="Clicking search bar"): return False
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.06)
    pyautogui.press("backspace")
    time.sleep(0.08)
    BOT_STATE.decision("Search for The Tower")
    pyautogui.write("The Tower", interval=0.02)
    time.sleep(SEARCH_RESULTS_LOAD_TIME)
    pyautogui.press("enter")
    time.sleep(1.5)
    if not get_game_window():
        if not safe_phone_link_click_abs((2238, 199), wait=1.0, label="Clicking first result"): return False
    return True

def wait_for_game_ready():
    BOT_STATE.set_phase("Launching", "Waiting for game window")
    game = wait_for_exact_window(GAME_TITLE, timeout=25.0, poll=0.25)
    if not game:
        BOT_STATE.set_phase("Error", "Game not found")
        return False
    focus_window(game, "The Tower")
    maximize_window(game)
    time.sleep(GAME_LOAD_TIME)
    detect_runtime_points(force=True)
    return True

def smart_startup():
    BOT_STATE.set_phase("Launching", "Smart startup running")
    game = get_game_window()
    if game:
        focus_window(game, "The Tower")
        maximize_window(game)
        time.sleep(0.4)
        detect_runtime_points(force=True)
        screen = SCREEN.scan()
        if screen.resume_visible or screen.death_visible or screen.game_window_ready:
            BOT_STATE.decision("Game already open, entering directly")
            return resume_or_start_tier_inner()
    if not open_game_from_phone_link(): return False
    if not wait_for_game_ready(): return False
    return resume_or_start_tier_inner()

def upgrade_loop():
    BOT_STATE.set_phase("Running", "Decision engine active")
    while check_running():
        if not ensure_game_window_ready(): return
        detect_runtime_points(force=False)
        BOT_STATE.add_cycle()
        screen = SCREEN.scan()
        action = decide_next_action(screen)
        BOT_STATE.decision(action)
        if action == "death_home":
            handle_death_screen()
            if not start_target_run():
                stop_bot("Could not restart target tier")
                return
            continue
        if action == "resume_popup":
            handle_resume(); continue
        if action == "collect_ad_gem":
            try_collect_ad_gem(); continue
        if action == "collect_flying_gem":
            try_collect_flying_gem(); continue
        if action == "idle":
            time.sleep(0.12); continue
        if not upgrade_cycle():
            time.sleep(0.10); continue

def main():
    BOT_STATE.set_phase("Starting", "Booting bot")
    if not smart_startup():
        stop_bot("Startup failed")
        return
    upgrade_loop()

def resume_or_restart_flow():
    BOT_STATE.set_phase("Resuming", "Trying to return to game")
    win = get_game_window()
    if win:
        focus_window(win, "The Tower")
        maximize_window(win)
        time.sleep(0.5)
        detect_runtime_points(force=True)
        if resume_or_start_tier_inner():
            upgrade_loop()
            return
    BOT_STATE.event("Game not ready, running startup flow")
    if not smart_startup():
        stop_bot("Resume failed")
        return
    upgrade_loop()

class GameOverlay:
    def __init__(self, root):
        self.root = root
        self.win = tk.Toplevel(root)
        self.win.withdraw()
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=OVERLAY_BG)
        try:
            self.win.wm_attributes("-transparentcolor", OVERLAY_BG)
        except Exception:
            pass
        self.canvas = tk.Canvas(self.win, bg=OVERLAY_BG, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self._make_clickthrough()
    def _make_clickthrough(self):
        try:
            self.win.update_idletasks()
            hwnd = self.win.winfo_id()
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            current = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, current | WS_EX_LAYERED | WS_EX_TRANSPARENT)
        except Exception:
            pass
    def update(self):
        if not FLAGS.get("show_game_overlay"):
            self.win.withdraw()
            return
        rect = game_rect()
        if not rect:
            self.win.withdraw()
            return
        left, top, width, height = rect
        self.win.geometry(f"{width}x{height}+{left}+{top}")
        self.win.deiconify()
        self.canvas.config(width=width, height=height)
        self.canvas.delete("all")
        for name, det in LOCATOR.snapshot().items():
            x = det.center[0] - left
            y = det.center[1] - top
            self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6, outline=LOCATOR_RING_COLOR, width=2)
            self.canvas.create_text(x + 10, y - 10, text=name, fill=LOCATOR_TEXT_COLOR, anchor="w", font=("Segoe UI", 8, "bold"))
        if FLAGS.get("show_click_highlights"):
            now = time.time()
            for effect in CLICK_EFFECTS.get_active():
                age = now - effect.created_at
                progress = min(max(age / CLICK_RING_LIFETIME, 0.0), 1.0)
                radius = 8 + int(CLICK_RING_MAX_RADIUS * progress)
                x = effect.x - left
                y = effect.y - top
                if 0 <= x <= width and 0 <= y <= height:
                    self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline=CLICK_RING_COLOR, width=3)

class ScrollableFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        canvas = tk.Canvas(self, bg="#07111f", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        window_id = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int(e.delta / 120), "units"))

class StatusGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(BOT_WINDOW_TITLE)
        self.root.geometry("560x980+1380+20")
        self.root.resizable(False, False)
        self.root.configure(bg="#07111f")
        self.root.attributes("-topmost", True)
        self.overlay = GameOverlay(self.root)
        self._build_styles()
        self._build_layout()
        self._tick()
    def _build_styles(self):
        style = ttk.Style()
        try: style.theme_use("clam")
        except Exception: pass
        style.configure("Card.TFrame", background="#0f1f38")
        style.configure("Title.TLabel", background="#07111f", foreground="#f7fbff", font=("Segoe UI", 24, "bold"))
        style.configure("Muted.TLabel", background="#07111f", foreground="#9cb6d6", font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background="#0f1f38", foreground="#7ecbff", font=("Segoe UI", 10, "bold"))
        style.configure("Value.TLabel", background="#0f1f38", foreground="#ffffff", font=("Segoe UI", 16, "bold"))
        style.configure("SmallValue.TLabel", background="#0f1f38", foreground="#e7f0ff", font=("Segoe UI", 12, "bold"))
        style.configure("Accent.TLabel", background="#0f1f38", foreground="#62b0ff", font=("Segoe UI", 13, "bold"))
    def _card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=14)
        card.pack(fill="x", padx=14, pady=8)
        return card
    def _toggle(self, parent, text, attr):
        var = tk.BooleanVar(value=FLAGS.get(attr))
        def on_change():
            FLAGS.set_flag(attr, var.get())
            BOT_STATE.event(f"{text}: {'On' if var.get() else 'Off'}")
        cb = tk.Checkbutton(parent, text=text, variable=var, command=on_change, bg="#0f1f38", fg="#e7f0ff", activebackground="#0f1f38", activeforeground="#ffffff", selectcolor="#1c3157", font=("Segoe UI", 10, "bold"), relief="flat", anchor="w")
        cb.pack(fill="x", pady=2)
    def _build_layout(self):
        header = tk.Frame(self.root, bg="#07111f")
        header.pack(fill="x", padx=14, pady=(14, 6))
        ttk.Label(header, text="The Tower Bot", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Client-rect clicks, popup resume priority, overlay off by default", style="Muted.TLabel").pack(anchor="w", pady=(2, 0))
        scroll = ScrollableFrame(self.root)
        scroll.pack(fill="both", expand=True)
        body = scroll.scrollable_frame

        hero = self._card(body)
        ttk.Label(hero, text="SYSTEM", style="CardTitle.TLabel").pack(anchor="w")
        self.hero_status = ttk.Label(hero, text="Idle", style="Value.TLabel")
        self.hero_status.pack(anchor="w", pady=(8, 2))
        self.hero_detail = ttk.Label(hero, text="Press Start in the GUI", style="Muted.TLabel")
        self.hero_detail.pack(anchor="w")

        controls = self._card(body)
        ttk.Label(controls, text="CONTROLS", style="CardTitle.TLabel").pack(anchor="w")
        btn_row = tk.Frame(controls, bg="#0f1f38"); btn_row.pack(fill="x", pady=(10, 0))
        ttk.Button(btn_row, text="Start", command=start_bot).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ttk.Button(btn_row, text="Resume", command=resume_from_button).pack(side="left", expand=True, fill="x", padx=6)
        ttk.Button(btn_row, text="Stop", command=lambda: stop_bot("Stopped from GUI")).pack(side="left", expand=True, fill="x", padx=(6, 0))

        extra = tk.Frame(controls, bg="#0f1f38"); extra.pack(fill="x", pady=(8, 0))
        ttk.Button(extra, text="Toggle Menu", command=toggle_game_menu).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ttk.Button(extra, text="Refresh Vision", command=lambda: [detect_runtime_points(force=True), save_locator_overlay()]).pack(side="left", expand=True, fill="x", padx=6)
        ttk.Button(extra, text="Overlay", command=save_locator_overlay).pack(side="left", expand=True, fill="x", padx=(6, 0))

        tier_card = self._card(body)
        ttk.Label(tier_card, text="TARGET TIER", style="CardTitle.TLabel").pack(anchor="w")
        self.tier_var = tk.IntVar(value=BOT_STATE.snapshot()["target_tier"])
        self.tier_value_label = ttk.Label(tier_card, text=f"Tier {self.tier_var.get()}", style="SmallValue.TLabel")
        self.tier_value_label.pack(anchor="w", pady=(8, 6))
        tier_slider = tk.Scale(tier_card, from_=1, to=25, orient="horizontal", variable=self.tier_var, resolution=1, showvalue=False, length=340, command=lambda _v: self._on_tier_slider_change(), bg="#0f1f38", fg="#e7f0ff", troughcolor="#1c3157", highlightthickness=0, activebackground="#62b0ff", font=("Segoe UI", 10, "bold"))
        tier_slider.pack(anchor="w", pady=(0, 6))
        ttk.Button(tier_card, text="Apply Tier", command=lambda: BOT_STATE.set_target_tier(self.tier_var.get())).pack(anchor="w")

        features = self._card(body)
        ttk.Label(features, text="FEATURES", style="CardTitle.TLabel").pack(anchor="w")
        for text, attr in [
            ("Auto Buy Upgrades", "auto_buy"),
            ("Auto Ad Gems", "auto_ad_gems"),
            ("Auto Flying Gems", "auto_flying_gems"),
            ("Auto Resume / Restart", "auto_resume"),
            ("Live Locator", "live_locator"),
            ("Auto Debug Snapshots", "auto_debug_snapshots"),
            ("Show Game Overlay", "show_game_overlay"),
            ("Show Click Highlights", "show_click_highlights"),
        ]:
            self._toggle(features, text, attr)

        vision = self._card(body)
        ttk.Label(vision, text="VISION", style="CardTitle.TLabel").pack(anchor="w")
        self.vision_value = ttk.Label(vision, text="Waiting", style="Value.TLabel")
        self.vision_value.pack(anchor="w", pady=(8, 2))
        self.detected_value = ttk.Label(vision, text="Detections: 0", style="SmallValue.TLabel"); self.detected_value.pack(anchor="w")
        self.refresh_value = ttk.Label(vision, text="Refresh age: 0.00s", style="SmallValue.TLabel"); self.refresh_value.pack(anchor="w", pady=(2, 0))

        status = self._card(body)
        ttk.Label(status, text="STATUS", style="CardTitle.TLabel").pack(anchor="w")
        self.window_value = ttk.Label(status, text="Unknown", style="Accent.TLabel"); self.window_value.pack(anchor="w", pady=(8, 2))
        self.window_size_value = ttk.Label(status, text="Window: Unknown", style="SmallValue.TLabel"); self.window_size_value.pack(anchor="w")
        self.strategy_value = ttk.Label(status, text="Strategy: Vision Guided", style="SmallValue.TLabel"); self.strategy_value.pack(anchor="w")
        self.tab_value = ttk.Label(status, text="Tab: None", style="SmallValue.TLabel"); self.tab_value.pack(anchor="w", pady=(2, 0))

        gems = self._card(body)
        ttk.Label(gems, text="GEMS", style="CardTitle.TLabel").pack(anchor="w")
        self.ad_cd_value = ttk.Label(gems, text="Ad Gem: Ready", style="Accent.TLabel"); self.ad_cd_value.pack(anchor="w", pady=(8, 2))
        self.fly_cd_value = ttk.Label(gems, text="Flying Scan: 0.08s", style="SmallValue.TLabel"); self.fly_cd_value.pack(anchor="w")

        stats = self._card(body)
        ttk.Label(stats, text="COUNTERS", style="CardTitle.TLabel").pack(anchor="w")
        self.health_value = ttk.Label(stats, text="Health clicks: 0", style="SmallValue.TLabel"); self.health_value.pack(anchor="w", pady=(8, 2))
        self.damage_value = ttk.Label(stats, text="Damage clicks: 0", style="SmallValue.TLabel"); self.damage_value.pack(anchor="w")
        self.utility_value = ttk.Label(stats, text="Utility clicks: 0", style="SmallValue.TLabel"); self.utility_value.pack(anchor="w")
        self.ad_value = ttk.Label(stats, text="Ad gems: 0", style="SmallValue.TLabel"); self.ad_value.pack(anchor="w")
        self.fly_value = ttk.Label(stats, text="Flying gems: 0", style="SmallValue.TLabel"); self.fly_value.pack(anchor="w")

        event_card = self._card(body)
        ttk.Label(event_card, text="LAST EVENT", style="CardTitle.TLabel").pack(anchor="w")
        self.event_value = ttk.Label(event_card, text="None", style="SmallValue.TLabel"); self.event_value.pack(anchor="w", pady=(8, 0))

        footer = tk.Frame(body, bg="#07111f"); footer.pack(fill="both", expand=True, padx=14, pady=(8, 16))
        self.uptime_value = ttk.Label(footer, text="Uptime: 00:00:00", style="Muted.TLabel"); self.uptime_value.pack(anchor="w")
        ttk.Label(footer, text="Hotkeys: F8 stop | F7 menu | F6 refresh vision", style="Muted.TLabel").pack(anchor="w", pady=(4, 0))
    def _on_tier_slider_change(self):
        self.tier_value_label.config(text=f"Tier {self.tier_var.get()}")
    def _format_seconds(self, seconds):
        seconds = max(0, int(seconds))
        h = seconds // 3600; m = (seconds % 3600) // 60; s = seconds % 60
        return f"{h:02}:{m:02}:{s:02}"
    def _tick(self):
        snap = BOT_STATE.snapshot()
        self.hero_status.config(text=snap["phase"])
        self.hero_detail.config(text=snap["detail"])
        self.window_value.config(text=snap["window_status"])
        self.window_size_value.config(text=f"Window: {snap['game_window_size']}")
        self.strategy_value.config(text=f"Strategy: {snap['strategy']}")
        self.tab_value.config(text=f"Tab: {snap['current_tab']}")
        self.vision_value.config(text=snap["vision_status"])
        self.detected_value.config(text=f"Detections: {snap['detected_count']}")
        self.refresh_value.config(text=f"Refresh age: {snap['last_refresh_age']:.2f}s")
        self.health_value.config(text=f"Health clicks: {snap['health_clicks']}")
        self.damage_value.config(text=f"Damage clicks: {snap['damage_clicks']}")
        self.utility_value.config(text=f"Utility clicks: {snap['utility_clicks']}")
        self.ad_value.config(text=f"Ad gems: {snap['ad_gems_collected']}")
        self.fly_value.config(text=f"Flying gems: {snap['flying_gems_clicked']}")
        self.event_value.config(text=snap["last_event"])
        self.uptime_value.config(text=f"Uptime: {self._format_seconds(snap['uptime'])}")
        if snap["last_ad_gem_collect"] > 0:
            ready_in = AD_GEM_COOLDOWN_SECONDS - (time.time() - snap["last_ad_gem_collect"])
            self.ad_cd_value.config(text="Ad Gem: Ready" if ready_in <= 0 else f"Ad Gem: {self._format_seconds(ready_in)}")
        else:
            self.ad_cd_value.config(text="Ad Gem: Ready")
        self.fly_cd_value.config(text=f"Flying Scan: {FLYING_GEM_CHECK_INTERVAL:.2f}s")
        self.overlay.update()
        self.root.after(100, self._tick)
    def run(self):
        self.root.mainloop()

def start_gui():
    global GUI
    GUI = StatusGUI()
    GUI.run()

if __name__ == "__main__":
    threading.Thread(target=stop_listener, daemon=True).start()
    threading.Thread(target=menu_listener, daemon=True).start()
    threading.Thread(target=refresh_listener, daemon=True).start()
    start_gui()
