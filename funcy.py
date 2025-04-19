import os
import sys
import shutil
import stat
from PIL import Image
import ujson
import win32gui
import win32api
import win32con
import requests

# get default cats
cat_dir = os.path.join(
    os.path.dirname(sys.executable if hasattr(sys, "_MEIPASS") else __file__),
    "config",
    "cats",
)
os.makedirs(cat_dir, exist_ok=True)
cat_urls = [
    "https://raw.githubusercontent.com/NSPC911/bongo-cat/refs/heads/main/idle.png",
    "https://raw.githubusercontent.com/NSPC911/bongo-cat/refs/heads/main/leftpaw.png",
    "https://raw.githubusercontent.com/NSPC911/bongo-cat/refs/heads/main/rightpaw.png",
]


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def get_config():
    for url in cat_urls:
        filename = os.path.join(cat_dir, "default_" + os.path.basename(url))
        if not os.path.exists(filename):
            response = requests.get(url)
            with open(filename, "wb") as f:
                f.write(response.content)
    if hasattr(sys, "_MEIPASS"):
        config_dir = os.path.join(os.path.dirname(sys.executable), "config")
    else:
        config_dir = os.path.join(os.path.dirname(__file__), "config")
    os.makedirs(config_dir, exist_ok=True)
    # check for old version
    old_config_dir = os.path.join(
        os.getenv("APPDATA") if os.name == "nt" else os.path.expanduser("~/.config"),
        "bongo-cat",
    )
    if os.path.exists(old_config_dir):
        for file in os.listdir(old_config_dir):
            shutil.move(
                os.path.join(old_config_dir, file),
                os.path.join(config_dir, file),
            )
        shutil.rmtree(old_config_dir, onerror=remove_readonly)
    config_path = os.path.join(config_dir, "config.json")
    default_config = {
        "use_click": True,
        "use_keyboard": True,
        "pawcurate": False,
        "delay": 0.1,
        "width": 174,
        "height": 105,
        "offset_from_bottom": 0,
        "offset_from_right": 0,
        "hide_on_fullscreen": True,
        "offset_from_bottom_on_fullscreen": -60,
        "cats": {
            "idle": os.path.join(cat_dir, "default_idle.png"),
            "leftpaw": os.path.join(cat_dir, "default_leftpaw.png"),
            "rightpaw": os.path.join(cat_dir, "default_rightpaw.png"),
        },
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


def dump_config(dictionary):
    config_path = os.path.join(
        os.path.dirname(sys.executable if hasattr(sys, "_MEIPASS") else __file__),
        "config",
    )
    with open(os.path.join(config_path, "config.json"), "w") as f:
        f.write(ujson.dumps(dictionary, indent=4))


config = get_config()


def load_image(path):
    img = Image.open(path).convert("RGBA")
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
