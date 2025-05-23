import tkinter as tk
from PIL import ImageTk
from PIL.Image import Image
import win32gui
from random import randint
from pynput import keyboard, mouse
from pynput.keyboard import Key
import threading
import pystray
from funcy import (
    load_image,
    get_config,
    is_fullscreen_app_active,
    dump_config,
    update_available,
)
import time
import os
import sys
import webbrowser

config = get_config()

taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
left, top, right, bottom = win32gui.GetWindowRect(taskbar)

x = right - config["width"] - config["offset_from_right"]
y = top - config["height"] + 68 - config["offset_from_bottom"]

root = tk.Tk()
root.attributes("-topmost", True)
root.overrideredirect(True)
root.wm_attributes("-transparentcolor", "white")

idle_image: Image = load_image(config["cat_states"]["idle"])
leftpaw_image = load_image(config["cat_states"]["leftpaw"])
rightpaw_image = load_image(config["cat_states"]["rightpaw"])
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
    taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
    left, top, right, bottom = win32gui.GetWindowRect(taskbar)

    x = right - config["width"] - config["offset_from_right"]
    y = top - config["height"] + 68 - config["offset_from_bottom"]

    root.geometry(f"{config['width']}x{config['height']}+{x}+{y}")

    global \
        idle_image, \
        leftpaw_image, \
        rightpaw_image, \
        idle_photo, \
        leftpaw_photo, \
        rightpaw_photo
    idle_image = load_image(config["cat_states"]["idle"])
    leftpaw_image = load_image(config["cat_states"]["leftpaw"])
    rightpaw_image = load_image(config["cat_states"]["rightpaw"])
    idle_photo = ImageTk.PhotoImage(idle_image)
    leftpaw_photo = ImageTk.PhotoImage(leftpaw_image)
    rightpaw_photo = ImageTk.PhotoImage(rightpaw_image)

    label.config(image=idle_photo)
    label.image = idle_photo
    listeners("start")


def toggle_config(key, icon, item, outer_key=None):
    if outer_key is not None:
        config[outer_key][key] = not config[outer_key][key]
        print(f"{outer_key}-{key} <===> {config[outer_key][key]}")
    else:
        config[key] = not config[key]
        print(f"{key} <===> {config[key]}")
    dump_config(config)
    reload_config(icon, item)


def setup_tray_icon():
    tray_image = idle_image.copy().resize((64, 64))
    menu = pystray.Menu(
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
                    "Mouse Clicks",
                    lambda icon, item: toggle_config("use_mouse", icon, item),
                    checked=lambda item: config["use_mouse"],
                ),
                pystray.MenuItem(
                    "Keyboard",
                    lambda icon, item: toggle_config("use_keyboard", icon, item),
                    checked=lambda item: config["use_keyboard"],
                ),
            ),
        ),
        pystray.MenuItem(
            "Fullscreen Mode",
            pystray.Menu(
                pystray.MenuItem(
                    "Show on Full Screen",
                    lambda icon, item: toggle_config("show", icon, item, "fullscreen"),
                    checked=lambda item: config["fullscreen"]["show"],
                ),
                pystray.MenuItem(
                    "Use Custom Offset from Bottom",
                    lambda icon, item: toggle_config(
                        "use_offset_from_bottom", icon, item, "fullscreen"
                    ),
                    checked=lambda item: config["fullscreen"]["use_offset_from_bottom"],
                    enabled=lambda item: config["fullscreen"]["show"],
                ),
                pystray.MenuItem(
                    "Use Custom Image on Full Screen",
                    lambda icon, item: toggle_config(
                        "use_custom_cats", icon, item, "fullscreen"
                    ),
                    checked=lambda item: config["fullscreen"]["use_custom_cats"],
                    enabled=lambda item: config["fullscreen"]["show"],
                ),
            ),
        ),
        pystray.MenuItem(
            f"Update {update_available()[1]} Available!"
            if update_available()[0]
            else "No Updates",
            lambda icon, item: webbrowser.open(
                "https://github.com/NSPC911/bongo-cat/releases"
            ),
            enabled=update_available()[0],
        ),
        pystray.MenuItem("Quit", quit_app),
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
        Key.left,
        Key.right,
        Key.up,
        Key.down,
    ],
}


def thread_trigger_animation(key=None):
    def run():
        with animation_lock:
            print(key)
            if config["pawcurate"] and key is not None:
                if (hasattr(key, "char") and key.char in LEFT_KEYS["char"]) or (
                    key in LEFT_KEYS["special"]
                ):
                    show_paw(leftpaw_photo)
                elif (
                    (hasattr(key, "char") and key.char in RIGHT_KEYS["char"])
                    or (key in RIGHT_KEYS["special"])
                    or (key == "mouse")
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
        # try except for the off chance that you didnt define it
        try:
            if keyboard_listener is not None:
                keyboard_listener.stop()
        except NameError:
            pass
        try:
            if mouse_listener is not None:
                mouse_listener.stop()
        except NameError:
            pass
    else:
        if config["use_keyboard"]:
            keyboard_listener = keyboard.Listener(
                on_press=lambda key: thread_trigger_animation(key),
                on_release=lambda key: key_release(),
            )
            keyboard_listener.start()
        if config["use_mouse"]:
            mouse_listener = mouse.Listener(
                on_click=lambda x, y, button, pressed: thread_trigger_animation("mouse")
                if pressed
                else key_release()
            )
            mouse_listener.start()


listeners("start")


def monitor_fullscreen_app():
    if (not config["fullscreen"]["show"]) and is_fullscreen_app_active():
        root.withdraw()
    else:
        if is_fullscreen_app_active():
            if config["fullscreen"]["use_offset_from_bottom"]:
                y_fullscreen = (
                    top
                    - config["height"]
                    + 68
                    - config["fullscreen"]["offset_from_bottom"]
                )
                root.geometry(
                    f"{config['width']}x{config['height']}+{x}+{y_fullscreen}"
                )
            else:
                root.geometry(f"{config['width']}x{config['height']}+{x}+{y}")
            global \
                idle_image, \
                leftpaw_image, \
                rightpaw_image, \
                idle_photo, \
                leftpaw_photo, \
                rightpaw_photo
            if config["fullscreen"]["use_custom_cats"]:
                idle_image = load_image(config["fullscreen"]["cat_states"]["idle"])
                leftpaw_image = load_image(
                    config["fullscreen"]["cat_states"]["leftpaw"]
                )
                rightpaw_image = load_image(
                    config["fullscreen"]["cat_states"]["rightpaw"]
                )
                idle_photo = ImageTk.PhotoImage(idle_image)
                leftpaw_photo = ImageTk.PhotoImage(leftpaw_image)
                rightpaw_photo = ImageTk.PhotoImage(rightpaw_image)
                label.config(image=idle_photo)
                label.image = idle_photo
            else:
                idle_image = load_image(config["cat_states"]["idle"])
                leftpaw_image = load_image(config["cat_states"]["leftpaw"])
                rightpaw_image = load_image(config["cat_states"]["rightpaw"])
                idle_photo = ImageTk.PhotoImage(idle_image)
                leftpaw_photo = ImageTk.PhotoImage(leftpaw_image)
                rightpaw_photo = ImageTk.PhotoImage(rightpaw_image)
                label.config(image=idle_photo)
                label.image = idle_photo
            label.update()
        else:
            root.geometry(f"{config['width']}x{config['height']}+{x}+{y}")
            idle_image = load_image(config["cat_states"]["idle"])
            leftpaw_image = load_image(config["cat_states"]["leftpaw"])
            rightpaw_image = load_image(config["cat_states"]["rightpaw"])
            idle_photo = ImageTk.PhotoImage(idle_image)
            leftpaw_photo = ImageTk.PhotoImage(leftpaw_image)
            rightpaw_photo = ImageTk.PhotoImage(rightpaw_image)
            label.config(image=idle_photo)
            label.image = idle_photo
            label.update()
        root.deiconify()
    root.after(1000, monitor_fullscreen_app)


monitor_fullscreen_app()

root.mainloop()
