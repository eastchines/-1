import tkinter as tk
from PIL import Image, ImageTk
from pynput.keyboard import Listener
import os

# ===================== 配置区（在这里改参数）=====================
SCALE = 1.0                # 初始缩放
SCALE_STEP = 0.1           # 滚轮每次缩放幅度
MIN_SCALE = 0.3            # 最小缩放
MAX_SCALE = 3.0            # 最大缩放
IS_GIRL = False            # False=兽形态，True=少女形态
IMG_COUNT = 5              # 每套皮肤5张图
SKIN_FOLDER = "skin"
ANIM_DELAY = 80            # 动画帧间隔(ms)
KEY_ANIM_TICK = 12         # 按键动画持续帧数
# =================================================================

# 动画状态变量
anim_frame = 0
is_pressing_key = False
press_anim_timer = 0

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-transparentcolor", "white")  #白色变成透明
root.attributes("-topmost", True)
root.title("KeyboardPet")

# 拖拽记录
drag_x = 0
drag_y = 0

# 加载皮肤图片函数
def load_skin(is_girl_mode: bool):
    prefix = "girl_" if is_girl_mode else "beast_"
    img_list = []
    for i in range(IMG_COUNT):
        img_path = os.path.join(SKIN_FOLDER, f"{prefix}{i}.png")
        im = Image.open(img_path).convert("RGBA")
        img_list.append(im)
    return img_list

raw_images = load_skin(IS_GIRL)
current_tk_img = None
label = tk.Label(root, bg="white")
label.pack()

# 刷新画面
def refresh_image():
    global current_tk_img
    w = int(raw_images[anim_frame].width * SCALE)
    h = int(raw_images[anim_frame].height * SCALE)
    img = raw_images[anim_frame].resize((w, h), Image.Resampling.LANCZOS)
    current_tk_img = ImageTk.PhotoImage(img)
    label.config(image=current_tk_img)

# 主动画循环
def animate_loop():
    global anim_frame, press_anim_timer, is_pressing_key
    if is_pressing_key:
        press_anim_timer -= 1
        if press_anim_timer > 0:
            if anim_frame < 4:
                anim_frame += 1
        else:
            is_pressing_key = False
            anim_frame = 0
    else:
        # 待机循环：0、1两帧循环
        anim_frame = (anim_frame + 1) % 2
    refresh_image()
    root.after(ANIM_DELAY, animate_loop)

# ========== 鼠标事件 ==========
def on_mouse_down(event):
    global drag_x, drag_y
    if event.num == 1:
        # 左键按下，准备拖拽
        drag_x = event.x
        drag_y = event.y
    elif event.num == 3:
        # 右键关闭宠物
        root.destroy()

def on_mouse_move(event):
    # 拖动窗口
    new_x = root.winfo_x() + event.x - drag_x
    new_y = root.winfo_y() + event.y - drag_y
    root.geometry(f"+{new_x}+{new_y}")

def on_mouse_wheel(event):
    global SCALE
    if event.delta > 0:
        SCALE += SCALE_STEP
    else:
        SCALE -= SCALE_STEP
    SCALE = max(MIN_SCALE, min(MAX_SCALE, SCALE))
    refresh_image()

# 绑定鼠标事件
label.bind("<ButtonPress-1>", on_mouse_down)
label.bind("<B1-Motion>", on_mouse_move)
label.bind("<Button-3>", on_mouse_down)
label.bind("<MouseWheel>", on_mouse_wheel)

# ========== 全局键盘监听 ==========
def on_key_press(key):
    global is_pressing_key, press_anim_timer
    if not is_pressing_key:
        is_pressing_key = True
        press_anim_timer = KEY_ANIM_TICK

listener = Listener(on_press=on_key_press)
listener.start()

# ========== F1 切换皮肤（兽 ↔ 少女） ==========
def toggle_skin(event):
    global IS_GIRL, raw_images, anim_frame
    IS_GIRL = not IS_GIRL
    raw_images = load_skin(IS_GIRL)
    anim_frame = 0
    refresh_image()

root.bind("<F1>", toggle_skin)

# 启动
refresh_image()
animate_loop()
root.mainloop()
listener.stop()
