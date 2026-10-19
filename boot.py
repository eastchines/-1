import os
import sys
import ctypes

# 获取exe所在文件夹路径
exe_path = os.path.abspath(sys.executable)
base_dir = os.path.dirname(exe_path)
script_file = os.path.join(base_dir, "main.py")

if not os.path.exists(script_file):
    ctypes.windll.user32.MessageBoxW(0, f"在程序目录找不到 main.py\n路径：{script_file}", "错误", 0x10)
    sys.exit(1)
else:
    try:
        with open(script_file, encoding="utf-8") as f:
            code = f.read()
        exec(code)
    except Exception as e:
        # main.py运行出错时弹出系统弹窗
        err_msg = f"main.py执行发生异常：\n{str(e)}"
        ctypes.windll.user32.MessageBoxW(0, err_msg, "main.py代码错误", 0x10)
