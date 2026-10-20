import sys
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pynput.keyboard
import threading
import time
import ctypes

# ========== 资源路径函数（外置图片专用，重点） ==========
def get_res_path(file_name):
    if hasattr(sys, "_MEIPASS"):
        # 打包exe后：读取exe所在文件夹
        base_path = os.path.dirname(sys.executable)
    else:
        # 本地直接运行py：读取脚本所在文件夹
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, file_name)

# ========== 配置参数 ==========
HUNGER_TIME = 3600    # 饥饿时间 3600秒 = 1小时
IDLE_TIME = 30        # 闲置多少秒变兽态
PET_SPEED = 2         # 绕圈移动速度

# 图片文件
IMG_NORMAL_BODY = "girl_body.png"
IMG_BEAST_BODY = "beast_0.png"

# ========== 加载皮肤 ==========
def load_skin(is_girl):
    raw_images = []
    if is_girl:
        img_path = get_res_path(os.path.join("skin", IMG_NORMAL_BODY))
    else:
        img_path = get_res_path(os.path.join("skin", IMG_BEAST_BODY))
    im = Image.open(img_path).convert("RGBA")
    raw_images.append(im)
    return raw_images

# ========== 窗口初始化 ==========
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-transparentcolor", "white")
root.attributes("-topmost", True)

# 初始加载女孩形态
IS_GIRL = True
raw_images = load_skin(IS_GIRL)
tk_img = ImageTk.PhotoImage(raw_images[0])
label = tk.Label(root, image=tk_img, bg="white")
label.pack()

# 屏幕宽高
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x, y = screen_w // 2, screen_h // 2

# 移动逻辑
dx, dy = PET_SPEED, PET_SPEED
last_active = time.time()

# 键盘监听线程
def keyboard_listen():
    global last_active
    def on_press(key):
        nonlocal last_active
        last_active = time.time()
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()

threading.Thread(target=keyboard_listen, daemon=True).start()

# 循环更新
def update():
    global x, y, dx, dy, IS_GIRL, raw_images, tk_img
    now = time.time()
    # 闲置超时切换兽态
    if now - last_active > IDLE_TIME and IS_GIRL:
        IS_GIRL = False
        raw_images = load_skin(IS_GIRL)
        tk_img = ImageTk.PhotoImage(raw_images[0])
        label.config(image=tk_img)
    elif now - last_active <= IDLE_TIME and not IS_GIRL:
        IS_GIRL = True
        raw_images = load_skin(IS_GIRL)
        tk_img = ImageTk.PhotoImage(raw_images[0])
        label.config(image=tk_img)

    # 边界反弹
    w, h = raw_images[0].size
    x += dx
    y += dy
    if x <= 0 or x + w >= screen_w:
        dx = -dx
    if y <= 0 or y + h >= screen_h:
        dy = -dy
    root.geometry(f"+{x}+{y}")
    root.after(20, update)

update()
root.mainloop()
