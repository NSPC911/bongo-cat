import tkinter as tk
from PIL import ImageTk
import win32gui
from random import randint
from pynput import keyboard, mouse
import threading
import time
import pystray
from funcy import load_image, get_config

config = get_config()

taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
left, top, right, bottom = win32gui.GetWindowRect(taskbar)

x = right - config["width"] + config["offset_from_right"]
y = top - config["height"] + config["offset_from_bottom"]

root = tk.Tk()
root.attributes("-topmost", True)
root.overrideredirect(True)
root.wm_attributes("-transparentcolor", "white")

idle_image = load_image("idle.png")
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

def setup_tray_icon():
    tray_image = idle_image.copy().resize((64, 64)) # use idle image for tray icon
    menu = pystray.Menu(
        pystray.MenuItem("Quit", quit_app)
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
    time.sleep(config["delay"])
    show_paw(idle_photo)

def thread_trigger_animation():
    threading.Thread(target=trigger_animation).start()

# screw the extra variables, just lambda it
if config["use_keyboard"]:
    keyboard.Listener(on_press=lambda key: thread_trigger_animation()).start()
if config["use_click"]:
    mouse.Listener(on_click=lambda x, y, button, pressed: thread_trigger_animation() if pressed else None).start()

root.mainloop()
