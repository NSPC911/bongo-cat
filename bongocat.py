import tkinter as tk
from PIL import ImageTk
from PIL.Image import Image
import win32gui
from random import randint
from pynput import keyboard, mouse
from pynput.keyboard import Key
import threading
import pystray
from funcy import load_image, get_config, is_fullscreen_app_active, dump_config
import time
import os
import sys

config = get_config()

taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
left, top, right, bottom = win32gui.GetWindowRect(taskbar)

x = right - config["width"] - config["offset_from_right"]
y = top - config["height"] + 62 - config["offset_from_bottom"]

root = tk.Tk()
root.attributes("-topmost", True)
root.overrideredirect(True)
root.wm_attributes("-transparentcolor", "white")

idle_image: Image = load_image(config["cats"]["idle"])
leftpaw_image = load_image(config["cats"]["leftpaw"])
rightpaw_image = load_image(config["cats"]["rightpaw"])
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
    os.startfile(
        os.path.join(
            os.path.dirname(sys.executable if hasattr(sys, "_MEIPASS") else __file__),
            "config",
        )
    )


def reload_config(icon, item):
    listeners("stop")
    global config, x, y, left, top, right, bottom
    config = get_config()
    left, top, right, bottom = win32gui.GetWindowRect(taskbar)

    x = right - config["width"] - config["offset_from_right"]
    y = top - config["height"] + 62 - config["offset_from_bottom"]

    root.geometry(f"{config['width']}x{config['height']}+{x}+{y}")

    global \
        idle_image, \
        leftpaw_image, \
        rightpaw_image, \
        idle_photo, \
        leftpaw_photo, \
        rightpaw_photo
    idle_image = load_image(config["cats"]["idle"])
    leftpaw_image = load_image(config["cats"]["left"])
    rightpaw_image = load_image(config["cats"]["right"])
    idle_photo = ImageTk.PhotoImage(idle_image)
    leftpaw_photo = ImageTk.PhotoImage(leftpaw_image)
    rightpaw_photo = ImageTk.PhotoImage(rightpaw_image)

    label.config(image=idle_photo)
    label.image = idle_photo
    listeners("start")


def toggle_config(key, icon, item):
    config[key] = not config[key]
    dump_config(config)
    reload_config(icon, item)


def setup_tray_icon():
    tray_image = idle_image.copy().resize((64, 64))  # use idle image for tray icon
    menu = pystray.Menu(
        pystray.MenuItem("Quit", quit_app),
        pystray.MenuItem("Launch Config", launch_config),
        pystray.MenuItem("Reload Config", reload_config),
        pystray.MenuItem(
            "Pawcurate Keys",
            lambda icon, item: toggle_config("pawcurate", icon, item),
            checked=lambda item: config["pawcurate"],
        ),
        pystray.MenuItem(
            "React to",
            pystray.Menu(
                pystray.MenuItem(
                    "Click",
                    lambda icon, item: toggle_config("use_click", icon, item),
                    checked=lambda item: config["use_click"],
                ),
                pystray.MenuItem(
                    "Keyboard",
                    lambda icon, item: toggle_config("use_keyboard", icon, item),
                    checked=lambda item: config["use_keyboard"],
                ),
            ),
        ),
    )
    icon = pystray.Icon("BongoCat", tray_image, "Bongo Cat", menu)
    threading.Thread(target=icon.run, daemon=True).start()


setup_tray_icon()


def show_paw(image):
    label.config(image=image)
    label.image = image
    root.update()


animation_lock = threading.Lock()
key_pressed = False

LEFT_KEYS = {
    "char": [
        "q",
        "w",
        "e",
        "r",
        "t",
        "a",
        "s",
        "d",
        "f",
        "g",
        "z",
        "x",
        "c",
        "v",
        "b",
        "`",
        "~",
        "1",
        "2",
        "3",
        "4",
        "5",
        "!",
        "@",
        "#",
        "$",
        "%",
    ],
    "special": [
        Key.shift_l,
        Key.ctrl_l,
        Key.alt_l,
        Key.cmd_l,
        Key.caps_lock,
        Key.tab,
        Key.f1,
        Key.f2,
        Key.f3,
        Key.f4,
        Key.f5,
        Key.esc,
    ],
}
RIGHT_KEYS = {
    "char": [
        "y",
        "u",
        "i",
        "o",
        "p",
        "h",
        "j",
        "k",
        "l",
        "n",
        "m",
        "6",
        "7",
        "8",
        "9",
        "0",
        "^",
        "&",
        "*",
        "(",
        ")",
        "-",
        "_",
        "+",
        "=",
        "[",
        "]",
        "{",
        "}",
        ";",
        ":",
        "'",
        '"',
        ",",
        ".",
        "<",
        "<",
        "/",
        "?",
        "|",
        "\\",
    ],
    "special": [
        Key.shift_r,
        Key.ctrl_r,
        Key.alt_r,
        Key.cmd_r,
        Key.backspace,
        Key.delete,
        Key.enter,
        Key.f6,
        Key.f7,
        Key.f8,
        Key.f9,
        Key.f10,
    ],
}


def thread_trigger_animation(key=None):
    def run():
        with animation_lock:
            if config["pawcurate"] and key is not None:
                if (hasattr(key, "char") and key.char in LEFT_KEYS["char"]) or (
                    key in LEFT_KEYS["special"]
                ):
                    show_paw(leftpaw_photo)
                elif (hasattr(key, "char") and key.char in RIGHT_KEYS["char"]) or (
                    key in RIGHT_KEYS["special"]
                ):
                    show_paw(rightpaw_photo)
                elif key == Key.space:
                    if randint(0, 1) == 0:
                        show_paw(leftpaw_photo)
                    else:
                        show_paw(rightpaw_photo)
                else:
                    if randint(0, 1) == 0:
                        show_paw(leftpaw_photo)
                    else:
                        show_paw(rightpaw_photo)
            else:
                if randint(0, 1) == 0:
                    show_paw(leftpaw_photo)
                else:
                    show_paw(rightpaw_photo)
            time.sleep(config["delay"])
            show_paw(idle_photo)

    global key_pressed
    if not key_pressed:
        key_pressed = True
        threading.Thread(target=run, daemon=True).start()


def key_release():
    global key_pressed
    key_pressed = False


def listeners(startorstop):
    global keyboard_listener, mouse_listener
    if startorstop == "stop":
        if keyboard_listener is not None:
            keyboard_listener.stop()
        if mouse_listener is not None:
            mouse_listener.stop()
    else:
        if config["use_keyboard"]:
            keyboard_listener = keyboard.Listener(
                on_press=lambda key: thread_trigger_animation(key),
                on_release=lambda key: key_release(),
            )
            keyboard_listener.start()
        if config["use_click"]:
            mouse_listener = mouse.Listener(
                on_click=lambda x, y, button, pressed: thread_trigger_animation()
                if pressed
                else key_release()
            )
            mouse_listener.start()


listeners("start")


def monitor_fullscreen_app():
    if config["hide_on_fullscreen"] and is_fullscreen_app_active():
        root.withdraw()
    else:
        if is_fullscreen_app_active():
            y_fullscreen = (
                top - config["height"] + 62 - config["offset_from_bottom_on_fullscreen"]
            )
            root.geometry(f"{config['width']}x{config['height']}+{x}+{y_fullscreen}")
        else:
            root.geometry(f"{config['width']}x{config['height']}+{x}+{y}")
        root.deiconify()
    root.after(1000, monitor_fullscreen_app)


monitor_fullscreen_app()

root.mainloop()
