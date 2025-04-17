import os
import sys
from PIL import Image
import ujson
import win32gui
import win32api
import win32con

def get_config():
    config_dir = os.path.join(
        os.getenv("APPDATA") if os.name == "nt" else os.path.expanduser("~/.config"),
        "bongo-cat",
    )
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.json")
    default_config = {
        "use_click": True,
        "use_keyboard": True,
        "delay": 0.1,
        "width": 174,
        "height": 105,
        "offset_from_bottom": 0,
        "offset_from_right": 0,
        "hide_on_fullscreen": True,
        "offset_from_bottom_on_fullscreen": -60,
    }
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write(ujson.dumps(default_config, indent=4))
            file = default_config
            original_config = default_config
    with open(config_path, "r") as f:
        file = ujson.load(f)
        original_config = file.copy()
        for i in default_config:
            if i not in file:
                file[i] = default_config[i]
    if original_config != file:
        with open(config_path, "w") as f:
            f.write(ujson.dumps(file, indent=4))
    return file


config = get_config()


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.getcwd(), relative_path)


def load_image(path):
    img = Image.open(resource_path(path)).convert("RGBA")
    img = img.resize((config["width"], config["height"]), Image.NEAREST)
    datas = img.getdata()
    newData = [
        (255, 255, 255, 0) if all(v > 240 for v in pixel[:3]) else pixel
        for pixel in datas
    ]
    img.putdata(newData)
    return img


def is_fullscreen_app_active():
    foreground_window = win32gui.GetForegroundWindow()
    if not foreground_window:
        return False

    # Exclude the desktop window
    desktop_window = win32gui.FindWindow("Progman", None)
    workerw_window = win32gui.FindWindow("WorkerW", None)
    if foreground_window == desktop_window or foreground_window == workerw_window:
        return False

    # Get the dimensions of the foreground window
    left, top, right, bottom = win32gui.GetWindowRect(foreground_window)

    # Get the screen dimensions
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    # Check if the window is full-screen
    return (right - left == screen_width) and (bottom - top == screen_height)