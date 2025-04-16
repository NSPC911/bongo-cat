import os
import sys
from PIL import Image
import ujson


def get_config():
    config_dir = os.path.join(
        os.getenv("APPDATA") if os.name == "nt" else os.path.expanduser("~/.config"),
        "bongo-cat",
    )
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.json")

    if not os.path.exists(config_path):
        default_config = {
            "use_click": True,
            "use_keyboard": True,
            "delay": 0.1,
            "width": 174,
            "height": 105,
            "offset_from_bottom": 60,
            "offset_from_right": 0,
        }
        with open(config_path, "w") as f:
            f.write(ujson.dumps(default_config, indent=4))
    with open(config_path, "r") as f:
        return ujson.load(f)


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
