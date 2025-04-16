import tkinter as tk
from PIL import ImageTk
from PIL.Image import Image
import win32gui
from random import randint
from pynput import keyboard, mouse
import threading
import pystray
from funcy import load_image, get_config
import time
import os

config = get_config()

taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
left, top, right, bottom = win32gui.GetWindowRect(taskbar)

x = right - config["width"] + config["offset_from_right"]
y = top - config["height"] + config["offset_from_bottom"]

root = tk.Tk()
root.attributes("-topmost", True)
root.overrideredirect(True)
root.wm_attributes("-transparentcolor", "white")

idle_image: Image = load_image("idle.png")
leftpaw_image = load_image("leftpaw.png")
rightpaw_image = load_image("rightpaw.png")
idle_photo = ImageTk.PhotoImage(idle_image)
leftpaw_photo = ImageTk.PhotoImage(leftpaw_image)
rightpaw_photo = ImageTk.PhotoImage(rightpaw_image)


label = tk.Label(root, image=idle_photo, bg="white")
label.pack()
root.geometry(f"+{x}+{y}")


# more funcys :3
def quit_app(icon, item):
    icon.stop()
    root.quit()


def launch_config(icon, item):
    os.startfile(config["config_path"])


def reload_config(icon, item):
    global config
    config = get_config()


def setup_tray_icon():
    tray_image = idle_image.copy().resize((64, 64))  # use idle image for tray icon
    menu = pystray.Menu(
        pystray.MenuItem("Quit", quit_app),
        pystray.MenuItem("Launch Config", launch_config),
        pystray.MenuItem("Reload Config", reload_config),
    )
    icon = pystray.Icon("BongoCat", tray_image, "Bongo Cat", menu)
    threading.Thread(target=icon.run, daemon=True).start()


setup_tray_icon()


def show_paw(image):
    label.config(image=image)
    label.image = image
    root.update()


def trigger_animation():
    if randint(0, 1) == 0:
        show_paw(leftpaw_photo)
    else:
        show_paw(rightpaw_photo)

    root.after(int(config["delay"] * 1000), lambda: show_paw(idle_photo))


animation_lock = threading.Lock()


def thread_trigger_animation():
    if animation_lock.locked():
        return

    def run():
        with animation_lock:
            trigger_animation()
            time.sleep(config["delay"])

    threading.Thread(target=run, daemon=True).start()


def key_release():
    global key_pressed
    key_pressed = False


# screw the extra variables, just lambda it
if config["use_keyboard"]:
    keyboard.Listener(
        on_press=lambda key: thread_trigger_animation(),
        on_release=lambda key: key_release(),
    ).start()
if config["use_click"]:
    mouse.Listener(
        on_click=lambda x, y, button, pressed: thread_trigger_animation()
        if pressed
        else None
    ).start()

root.mainloop()
