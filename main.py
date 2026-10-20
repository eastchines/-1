import sys
import os
import tkinter as tk
from PIL import Image, ImageTk
import pynput.keyboard
import threading
import time

# ========== 资源路径函数 ==========
def get_res_path(file_name):
    if hasattr(sys, "_MEIPASS"):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "skin", file_name)

# ========== 配置 ==========
IDLE_TIME = 2.5       # 多久没按键切待机
ANIM_SPEED = 0.15     # 打字动画切换速度

# 图片列表
GIRL_IDLE = "girl_idle.png"
GIRL_TYPE = [
    "girl_type_01.png",
    "girl_type_02.png",
    "girl_type_03.png",
    "girl_type_04.png"
]
ANIMAL_IDLE = "animal_idle.png"
ANIMAL_TYPE = [
    "animal_type_01.png",
    "animal_type_02.png",
    "animal_type_03.png",
    "animal_type_04.png"
]

# 加载图片
def load_img(name):
    return Image.open(get_res_path(name)).convert("RGBA")

# 预加载全部图片
girl_idle_img = load_img(GIRL_IDLE)
girl_type_imgs = [load_img(f) for f in GIRL_TYPE]
animal_idle_img = load_img(ANIMAL_IDLE)
animal_type_imgs = [load_img(f) for f in ANIMAL_TYPE]

# 窗口
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-transparentcolor", "white")
root.attributes("-topmost", True)

label = tk.Label(root, bg="white")
label.pack()

is_girl = True
last_key_time = time.time()
anim_index = 0
is_typing = False

# 键盘监听
def key_listen():
    global last_key_time, is_typing
    def on_press(key):
        last_key_time = time.time()
        is_typing = True
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()

threading.Thread(target=key_listen, daemon=True).start()

# 更新画面
def update():
    global anim_index, is_typing
    now = time.time()
    # 超过时间没按键，待机
    if now - last_key_time > IDLE_TIME:
        is_typing = False
        if is_girl:
            show_img = girl_idle_img
        else:
            show_img = animal_idle_img
    else:
        is_typing = True
        if is_girl:
            show_img = girl_type_imgs[anim_index]
        else:
            show_img = animal_type_imgs[anim_index]
        anim_index = (anim_index + 1) % 4

    tk_show = ImageTk.PhotoImage(show_img)
    label.config(image=tk_show)
    label.image = tk_show

    w, h = show_img.size
    # 固定在右下角，你也可以改成移动逻辑
    x = root.winfo_screenwidth() - w - 20
    y = root.winfo_screenheight() - h - 60
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.after(int(ANIM_SPEED * 1000), update)

update()
root.mainloop()
