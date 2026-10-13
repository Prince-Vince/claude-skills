"""Screenshot every screen of the Python desktop app (the UI/UX reference), using a throwaway database with the demo
client. Run from the Python repo: python -B py_shots.py <outDir>"""
import os
import sys
import tempfile
import time
from pathlib import Path

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
home = Path(tempfile.mkdtemp(prefix="tracker-shots-"))
os.environ["NOVENTECH_TRACKER_HOME"] = str(home)
sys.path.insert(0, os.getcwd())


from app.database.db import Database  # noqa: E402
from app.services import app_tour, seed  # noqa: E402
from app.services.catalog import load_catalog  # noqa: E402
from app.ui.app_window import AppWindow  # noqa: E402
from app.ui.workspace import TABS  # noqa: E402

db = Database(home / "tracker.db")
cat = load_catalog()
cid = seed.seed_demo(db, cat)
db.set_setting(app_tour.SEEN_SETTING, "1")
db.set_setting("technician_name", "Screen Shots")

win = AppWindow(db, cat)


def settle(secs=0.8):
    end = time.time() + secs
    while time.time() < end:
        win.update()
        time.sleep(0.02)


settle(0.5)
win.state("zoomed")
win.attributes("-topmost", True)
settle(1.0)


import ctypes  # noqa: E402
from ctypes import wintypes  # noqa: E402

from PIL import Image  # noqa: E402

user32, gdi32 = ctypes.windll.user32, ctypes.windll.gdi32


def window_image():
    """The app window's own pixels via PrintWindow: nothing else on the screen can end up in the picture."""
    hwnd = user32.GetParent(win.winfo_id()) or win.winfo_id()
    rect = wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    w, h = rect.right, rect.bottom
    hdc = user32.GetDC(hwnd)
    mem = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(mem, bmp)
    user32.PrintWindow(hwnd, mem, 3)  # PW_CLIENTONLY | PW_RENDERFULLCONTENT

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG), ("biHeight", wintypes.LONG),
                    ("biPlanes", wintypes.WORD), ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
                    ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG), ("biYPelsPerMeter", wintypes.LONG),
                    ("biClrUsed", wintypes.DWORD), ("biClrImportant", wintypes.DWORD)]

    header = BITMAPINFOHEADER(ctypes.sizeof(BITMAPINFOHEADER), w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(mem, bmp, 0, h, buf, ctypes.byref(header), 0)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mem)
    user32.ReleaseDC(hwnd, hdc)
    return Image.frombuffer("RGB", (w, h), buf, "raw", "BGRX", 0, 1)


def grab(name):
    settle()
    window_image().save(out / f"{name}.png")
    print(name)


for key, name in [("dashboard", "01-dashboard"), ("clients", "02-clients"), ("checklist", "03-checklist-picker"),
                  ("queue", "04-approval-queue"), ("findings", "05-all-findings"), ("risks", "06-all-risks"),
                  ("access", "07-all-access-reviews"), ("vendors", "30-vendors"), ("knowledge", "31-knowledge"),
                  ("scope", "32-scope"), ("reports", "33-reports"), ("settings", "35-settings")]:
    win.navigate(key)
    grab(name)

for i, tab in enumerate(TABS):
    win.navigate("workspace", client_id=cid, tab=tab)
    grab(f"1{i:02d}-{tab.lower().replace(' & ', '-').replace(' ', '-')}")

win.destroy()
db.close()
